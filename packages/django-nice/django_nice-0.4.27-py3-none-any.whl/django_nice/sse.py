from django.http import StreamingHttpResponse

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
            listener(new_value)  # Call each listener directly

    @classmethod
    def stream_updates(cls, request, app_label, model_name, object_id, field_name):
        def event_stream():
            listeners = cls.register_listener(model_name, object_id, field_name)

            from django.apps import apps
            model = apps.get_model(app_label, model_name)
            try:
                instance = model.objects.get(pk=object_id)
                last_value = getattr(instance, field_name)
            except model.DoesNotExist:
                last_value = None

            # Function to send updates immediately to the client
            def send_update(new_value):
                nonlocal last_value
                if new_value != last_value:
                    last_value = new_value
                    print(f"Sending SSE update: {new_value}")
                    message = f"data: {new_value}\n\n"
                    return message
                return None

            # Define a listener that sends data directly when notified
            def listener_callback(new_value):
                update_message = send_update(new_value)
                if update_message:
                    try:
                        response.write(update_message)
                        response.flush()
                    except Exception as e:
                        print(f"Error sending SSE update: {e}")

            # Register the listener
            print(f"Appending listener for {model_name} {object_id} {field_name}")
            listeners.append(listener_callback)

            # Create a Django response stream that keeps the connection open
            response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')

            # Send the initial value if it exists
            initial_update = send_update(last_value)
            if initial_update:
                response.write(initial_update)
                response.flush()

            # Keep the connection open and listen for client disconnects
            try:
                while True:
                    if request.META.get('HTTP_CONNECTION', '').lower() == 'close':
                        break
            except GeneratorExit:
                print(f"Removing listener for {model_name} {object_id} {field_name}")
                listeners.remove(listener_callback)
                raise

            return response

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
