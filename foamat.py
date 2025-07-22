import os
import json
import yaml

def convert_openapi_to_openapi(spec_location, target_version="3.1"):
    try:
        with open(spec_location, 'r') as file:
            if spec_location.endswith('.json'):
                data = json.load(file)
                syntax = 'json'
            elif spec_location.endswith('.yaml') or spec_location.endswith('.yml'):
                data = yaml.safe_load(file)
                syntax = 'yaml'
            else:
                print("Unsupported file format. Please use JSON or YAML.")
                return

        # Check if it's OpenAPI
        if 'openapi' in data:
            current_version = data['openapi']
            print(f"Current OpenAPI version: {current_version}")

            # Form the command
            command = f"api-spec-converter --from=openapi_{current_version.split('.')[0]}_{current_version.split('.')[1]} --to=openapi_{target_version.replace('.', '_')} --syntax={syntax} --order=alpha {spec_location} > new_spec.{syntax}"

            # Run the command
            os.system(command)
            print(f"Converted OpenAPI {current_version} to OpenAPI {target_version} and saved to new_spec.{syntax}")
        else:
            print("The input file is not a valid OpenAPI specification.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Use the function
convert_openapi_to_openapi("oas\language-tool.json", target_version="3.1")