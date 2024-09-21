from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
            listener(new_value)

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

            # Keep the connection alive by sending keep-alive pings
            try:
                while True:
                    yield ":\n\n"  # Send keep-alive to prevent connection timeout
            except GeneratorExit:
                listeners.remove(listener_callback)  # Remove the listener on client disconnect

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

    @classmethod
    @csrf_exempt
    def handle_post(cls, request, app_label, model_name, object_id, field_name):
        """
        Handle POST request to manually trigger the SSE update.
        """
        try:
            body = json.loads(request.body)
            new_value = body.get('new_value')

            if new_value is not None:
                # Trigger the update for all listeners
                cls.notify_listeners(model_name, object_id, field_name, new_value)
                return JsonResponse({'status': 'success', 'message': f'Updated {field_name} with {new_value}'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No new value provided'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
