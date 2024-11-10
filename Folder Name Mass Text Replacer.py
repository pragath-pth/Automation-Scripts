import os

# Specify the path to the directory containing the folders
directory_path = r'E:\Tamil\2011 - 2020'

# Text to remove from folder names
text_to_remove = "(Original Motion Picture Soundtrack)"

# List all items in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Remove the specified text from the folder name
        new_folder_name = folder_name.replace(text_to_remove, "").strip()
        new_folder_path = os.path.join(directory_path, new_folder_name)
        
        # Rename the folder
        os.rename(folder_path, new_folder_path)
        print(f'Renamed folder: "{folder_name}" to "{new_folder_name}"')
