from nicegui import ui
import requests
from .config import Config

def bind_element_to_model(element, app_label, model_name, object_id, field_name, element_id, property_name='value'):
    host = Config.get_host()
    api_endpoint = Config.get_api_endpoint()

    # Fetch initial data from the model
    def fetch_initial_data():
        url = f'{host}{api_endpoint}/{app_label}/{model_name}/{object_id}/{field_name}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get(field_name, '')
        return ''

    # Update the model when the value changes in the frontend
    def update_data(value):
        if value is None or value == '':
            pass
        else:
            url = f'{host}{api_endpoint}/{app_label}/{model_name}/{object_id}/{field_name}/'
            response = requests.post(url, json={field_name: value})

    # Set the element's initial value and bind the value between frontend and backend
    setattr(element, property_name, fetch_initial_data())

    # Determine the appropriate event listener based on the element type
    if isinstance(element, ui.input):
        listener_event = 'update:model-value'
    elif isinstance(element, ui.checkbox):
        listener_event = 'update:model-checked'
    elif isinstance(element, ui.slider):
        listener_event = 'update:model-value'
    elif isinstance(element, ui.button):
        listener_event = 'click'
    else:
        listener_event = f'update:model-{property_name}'

    # Bind the element's value to backend model changes
    def on_frontend_change(e):
        new_value = ''.join(e.args)
        update_data(new_value)

    # Define the event listener for the frontend change
    element.on(listener_event, on_frontend_change)
    element.props(f'id={element_id}')

    # Define a callback that can be used in the injected JavaScript
    def set_value_in_element(new_value):
        element.set_value(new_value)

    # Inject JavaScript to listen to SSE updates and use the Python callback
    sse_url = f'{host}{api_endpoint}/sse/{app_label}/{model_name}/{object_id}/{field_name}/'
    ui.add_body_html(f"""
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                let eventSource = new EventSource("{sse_url}");

                eventSource.onmessage = function(event) {{
                    const newValue = event.data;
                    console.log("Received new message from SSE:", newValue);

                    // Use NiceGUI's Python-side callback to set the new value
                    window.nicegui.run({set_value_in_element.__name__}, newValue);
                }};

                eventSource.onerror = function(error) {{
                    console.error("SSE connection error:", error);
                }};

                // Cleanup: Close the EventSource connection when the page is closed or navigated away from
                window.addEventListener('beforeunload', function() {{
                    if (eventSource) {{
                        eventSource.close();
                    }}
                }});
            }});
        </script>
    """)