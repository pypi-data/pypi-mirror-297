import requests

def list_templates():
    # Example function to list templates from langchainhub
    response = requests.get("https://api.langchainhub.com/templates")
    return response.json()

def get_template(template_name):
    # Example function to get a specific template from langchainhub
    response = requests.get(f"https://api.langchainhub.com/templates/{template_name}")
    return response.json()