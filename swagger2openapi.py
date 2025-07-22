import os
import json
import yaml

def convert_swagger2_to_openapi3(spec_location):
    try:
        with open(spec_location, 'r') as file:
            if spec_location.endswith('.json'):
                data = json.load(file)
                syntax = 'json'
            elif spec_location.endswith('.yaml') or spec_location.endswith('.yml'):
                data = yaml.safe_load(file)
                syntax = 'json'
            else:
                print("Unsupported file format. Please use JSON or YAML.")
                return

        # Check if it's Swagger 2.0
        if 'swagger' in data and data['swagger'] == "2.0":
            # Form the command
            command = f"api-spec-converter --from=swagger_2 --to=openapi_3 --syntax={syntax} --order=alpha {spec_location} > swagger2openapi/new_spec.{syntax}"

            # Run the command
            os.system(command)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Use the function
convert_swagger2_to_openapi3("casdoor\swagger.json")