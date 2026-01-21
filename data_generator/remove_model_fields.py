#!/usr/bin/env python3
"""
Script to remove 'model' fields from JSON data files.
"""

import json
import os
from pathlib import Path

def remove_model_fields_from_file(file_path):
    """
    Remove all 'model' fields from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
    """
    print(f"Processing {file_path}...")
    
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove model field from dataset_info if it exists
        if 'dataset_info' in data and 'model' in data['dataset_info']:
            del data['dataset_info']['model']
            print(f"  Removed model from dataset_info")
        
        # Recursively remove model fields from the entire data structure
        def remove_model_recursive(obj):
            if isinstance(obj, dict):
                # Create a list of keys to avoid modifying dict during iteration
                keys_to_remove = [key for key in obj.keys() if key == 'model']
                for key in keys_to_remove:
                    del obj[key]
                    print(f"  Removed model field from nested structure")
                
                # Recursively process nested dictionaries and lists
                for value in obj.values():
                    remove_model_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    remove_model_recursive(item)
        
        remove_model_recursive(data)
        
        # Write the modified data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  Successfully processed {file_path}")
        
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")

def main():
    """Main function to process all JSON files."""
    # Define the files to process
    files_to_process = [
        "data/CN_chat_data.json",
        "data/CN_data.json", 
        "data/EN_chat_data.json",
        "data/EN_data.json"
    ]
    
    # Get the script directory
    script_dir = Path(__file__).parent
    
    # Process each file
    for file_name in files_to_process:
        file_path = script_dir / file_name
        if file_path.exists():
            remove_model_fields_from_file(file_path)
        else:
            print(f"File not found: {file_path}")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()
