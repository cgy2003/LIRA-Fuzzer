import json
import copy
import argparse


def convert_security_to_parameters(openapi_spec):
    new_spec = copy.deepcopy(openapi_spec)
    security_schemes = new_spec.get('components', {}).get('securitySchemes', {})

    def security_to_parameter(scheme_name, scheme):
        if scheme['type'] == 'apiKey':
            return {
                'name': scheme['name'],
                'in': scheme['in'],
                'required': True,
                'description': scheme.get('description', ''),
                'schema': {
                    'type': 'string',
                    'example': scheme.get('x-appwrite', {}).get('demo', '')
                }
            }
        return None

    for path, methods in new_spec.get('paths', {}).items():
        for method, operation in methods.items():
            if 'security' in operation:
                parameters = operation.get('parameters', [])

                for security in operation['security']:
                    for scheme_name in security.keys():
                        scheme = security_schemes.get(scheme_name)
                        if scheme:
                            param = security_to_parameter(scheme_name, scheme)
                            if param:
                                parameters.append(param)

                operation['parameters'] = parameters
                del operation['security']

    if 'security' in new_spec:
        del new_spec['security']

    return new_spec


def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        openapi_spec = json.load(file)

    new_spec = convert_security_to_parameters(openapi_spec)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(new_spec, file, indent=2, ensure_ascii=False)

    print(f"Security definitions have been converted to parameters and saved to {output_file}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert OpenAPI security definitions to parameters.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    main(args.input_file, args.output_file)