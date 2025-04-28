import json
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def find_matches():
    """Compare first item's EN-US name to a manually written term."""
    # Load items_cleaned.json
    items_file = project_root / 'config' / 'items_cleaned.json'
    with open(items_file, 'r', encoding='utf-8') as f:
        items_data = json.load(f)
    
    # Get the first item
    first_item = items_data[0]
    
    # Store its EN-US name
    en_us_name = first_item.get('localizedNames', {}).get('EN-US', '')
    
    # Manually write the term to compare against
    search_term = "Hideout"  # Change this to whatever you want to compare
    
    print(f"\nFirst item's EN-US name: {en_us_name}")
    print(f"Comparing with term: {search_term}")
    
    # Compare and return result
    if search_term in en_us_name:
        print(f"\nMATCH FOUND!")
        print(f"UniqueName: {first_item.get('uniqueName', '')}")
    else:
        print("\nNO MATCH")

if __name__ == "__main__":
    find_matches() 