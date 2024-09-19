from nicegui import ui
import requests
from .config import Config 

def bind_element_to_model(element, app_label, model_name, object_id, field_name, element_id):
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
        url = f'{host}{api_endpoint}/{app_label}/{model_name}/{object_id}/{field_name}/'
        requests.post(url, json={field_name: value})

    # Set the element's initial value and bind the value between frontend and backend
    element.value = fetch_initial_data()

    # Bind the element's value to backend model changes
    def on_frontend_change(e):
        new_value = e.value  # Extract the new value
        update_data(new_value)  # Send updated value to the backend

    # Use the appropriate event listener for this specific element
    element.on('input', on_frontend_change)  # Use 'input' for input fields, adjust if necessary for other elements

    # Inject JavaScript to listen to SSE updates and update the element's value
    sse_url = f'{host}{api_endpoint}/sse/{app_label}/{model_name}/{object_id}/{field_name}/'
    ui.add_body_html(f"""
    <script>
        const eventSource = new EventSource('{sse_url}');
        eventSource.onmessage = function(event) {{
            const newValue = event.data;

            // Update the NiceGUI element directly via the framework
            window.element = nicegui.elements['{element_id}'];
            if (window.element) {{
                window.element.value = newValue;
            }}
        }};
    </script>
    """)

    # Add ID to the element for proper access from the injected JavaScript
    element.props(f'id={element_id}')
