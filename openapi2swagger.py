import os
import json
import yaml

def convert_openapi3_to_swagger2(spec_location):
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

        # Check if it's OpenAPI 3.0
        if 'openapi' in data and data['openapi'].startswith("3.0"):
            # Form the command
            command = f"api-spec-converter --from=openapi_3 --to=swagger_2 --syntax={syntax} --order=alpha {spec_location} > openapi2swagger/new_spec.{syntax}"

            # Run the command
            os.system(command)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Use the function
convert_openapi3_to_swagger2("oas\jellyfin-openapi-10.7.1.json")