from django.http import StreamingHttpResponse
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
            listener(new_value)  # Directly call the listener callback with the new value

    @classmethod
    def stream_updates(cls, request, app_label, model_name, object_id, field_name):
        # Event stream function that yields events to the client
        def event_stream():
            listeners = cls.register_listener(model_name, object_id, field_name)

            from django.apps import apps
            model = apps.get_model(app_label, model_name)
            try:
                instance = model.objects.get(pk=object_id)
                last_value = getattr(instance, field_name)
            except model.DoesNotExist:
                last_value = None

            # Listener that sends updates directly to the client
            def listener_callback(new_value):
                print(f"Sending SSE update: {new_value}")
                yield f"data: {new_value}\n\n"

            print(f"Appending listener for {model_name} {object_id} {field_name}")
            listeners.append(listener_callback)

            # Send the initial value if it exists
            if last_value is not None:
                yield f"data: {last_value}\n\n"

            # Keep the connection open for future updates
            try:
                while True:
                    # This keeps the connection alive by sending empty data every 15 seconds
                    yield ":\n\n"
                    time.sleep(15)
            except GeneratorExit:
                # Client disconnected, remove the listener
                print(f"Removing listener for {model_name} {object_id} {field_name}")
                listeners.remove(listener_callback)
                raise

        # Return the event stream as a StreamingHttpResponse
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
