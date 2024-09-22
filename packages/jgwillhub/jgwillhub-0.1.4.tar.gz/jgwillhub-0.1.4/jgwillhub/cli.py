import argparse
import json
from prompts import list_templates, get_template

def main():
    parser = argparse.ArgumentParser(description="Prompt Template Hub Helper CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List templates command
    list_parser = subparsers.add_parser("list", help="List all available prompt templates")
    
    # Get template command
    get_parser = subparsers.add_parser("get", help="Get a specific prompt template")
    get_parser.add_argument("template_name", type=str, help="Name of the prompt template to retrieve")

    # Describe template command
    describe_parser = subparsers.add_parser("describe", help="Describe a specific prompt template")
    describe_parser.add_argument("template_name", type=str, help="Name of the prompt template to describe")

    args = parser.parse_args()

    if args.command == "list":
        templates = list_templates()
        print(json.dumps(templates, indent=2))
    elif args.command == "get":
        template = get_template(args.template_name)
        print(json.dumps(template, indent=2))
    elif args.command == "describe":
        template = get_template(args.template_name)
        description = template.get("description", "No description available.")
        print(description)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()