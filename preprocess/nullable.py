import json
import argparse


def remove_nullable(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    def remove_nullable_recursive(d):
        if isinstance(d, dict):
            d.pop('nullable', None)
            for key, value in d.items():
                remove_nullable_recursive(value)
        elif isinstance(d, list):
            for item in d:
                remove_nullable_recursive(item)

    remove_nullable_recursive(data)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove 'nullable' fields from a JSON file.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    remove_nullable(args.input_file, args.output_file)
    print(f"Processed {args.input_file} and saved as {args.output_file}.")