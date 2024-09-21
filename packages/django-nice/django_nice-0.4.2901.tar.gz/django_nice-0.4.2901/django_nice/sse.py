from django.http import StreamingHttpResponse
from queue import Queue
import time

class SSEManager:
    _listeners = {}

    @classmethod
    def register_listener(cls, model_name, object_id, field_name):
        if model_name not in cls._listeners:
            cls._listeners[model_name] = {}
        if object_id not in cls._listeners[model_name]:
            cls._listeners[model_name][object_id] = {}
        if field_name not in cls._listeners[model_name][object_id]:
            cls._listeners[model_name][object_id][field_name] = []
        return cls._listeners[model_name][object_id][field_name]

    @classmethod
    def notify_listeners(cls, model_name, object_id, field_name, new_value):
        listeners = cls._listeners.get(model_name, {}).get(object_id, {}).get(field_name, [])
        print(f"Notifying {len(listeners)} listeners for {model_name} {object_id} {field_name} with new value {new_value}")
        for listener in listeners:
            listener.put(new_value)  # Send the new value to the listener's queue

    @classmethod
    def stream_updates(cls, request, app_label, model_name, object_id, field_name):
        # Create an event stream function to yield events to the client
        def event_stream():
            listeners = cls.register_listener(model_name, object_id, field_name)

            from django.apps import apps
            model = apps.get_model(app_label, model_name)
            try:
                instance = model.objects.get(pk=object_id)
                last_value = getattr(instance, field_name)
            except model.DoesNotExist:
                last_value = None

            queue = Queue()  # A queue to hold updates for this client

            # Listener that pushes updates to the queue
            def listener_callback(new_value):
                queue.put(new_value)

            print(f"Appending listener for {model_name} {object_id} {field_name}")
            listeners.append(listener_callback)

            # Send the initial value if it exists
            if last_value is not None:
                yield f"data: {last_value}\n\n"

            # Continuously yield updates from the queue
            try:
                while True:
                    try:
                        # Wait for new data to appear in the queue (blocking call)
                        new_value = queue.get(timeout=10)  # Timeout prevents infinite blocking
                        print(f"Sending SSE update: {new_value}")
                        yield f"data: {new_value}\n\n"
                    except Exception:
                        # In case no new value is received, send a comment to keep the connection alive
                        yield ":\n\n"
                        time.sleep(1)  # Avoid busy waiting
            except GeneratorExit:
                # Client disconnected, remove the listener
                print(f"Removing listener for {model_name} {object_id} {field_name}")
                listeners.remove(listener_callback)
                raise

        # Return the event stream as a StreamingHttpResponse
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
