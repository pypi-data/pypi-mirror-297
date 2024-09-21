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
            listener(new_value)  # Send the new value to the listener's SSE stream

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

            # Send the initial value if it exists
            if last_value is not None:
                yield f"data: {last_value}\n\n"

            # Continuously yield updates from the listeners
            def listener_callback(new_value):
                yield f"data: {new_value}\n\n"

            listeners.append(listener_callback)

            # Keep the connection open by sending keep-alive pings
            try:
                while True:
                    yield ":\n\n"  # Send keep-alive to prevent connection timeout
            except GeneratorExit:
                listeners.remove(listener_callback)  # Remove the listener on client disconnect

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

