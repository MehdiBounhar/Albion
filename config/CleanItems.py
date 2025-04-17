import json


def load_excluded_items(filename):
    """Load items to exclude from a text file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()


def clean_json_data(input_file, output_file, exclude_file):
    # Load items to exclude
    excluded_items = load_excluded_items(exclude_file)

    # Read the JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Clean each item
    cleaned_data = []
    for item in data:
        # Skip items without UniqueName or if in excluded list
        if not item.get("UniqueName") or item.get("UniqueName") in excluded_items:
            continue

        cleaned_item = {
            "UniqueName": item.get("UniqueName"),
            "Index": item.get("Index"),
        }

        # Safely handle LocalizedNames
        localized_names = item.get("LocalizedNames", {})
        if (
            localized_names
            and isinstance(localized_names, dict)
            and "EN-US" in localized_names
        ):
            cleaned_item["LocalizedNames"] = {"EN-US": localized_names["EN-US"]}

        # Safely handle LocalizedDescriptions
        localized_desc = item.get("LocalizedDescriptions", {})
        if (
            localized_desc
            and isinstance(localized_desc, dict)
            and "EN-US" in localized_desc
        ):
            cleaned_item["LocalizedDescriptions"] = {"EN-US": localized_desc["EN-US"]}

        cleaned_data.append(cleaned_item)

    # Write the cleaned data to a new file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)

    # Print statistics
    print(f"Total items processed: {len(data)}")
    print(f"Items excluded: {len(excluded_items)}")
    print(f"Items in output: {len(cleaned_data)}")


# Usage
input_file = "items.json"
output_file = "items_cleaned.json"
exclude_file = "all_item_ids.txt"
clean_json_data(input_file, output_file, exclude_file)
