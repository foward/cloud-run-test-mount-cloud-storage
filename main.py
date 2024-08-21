import os
import logging
from flask import Flask

# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

mount_path = os.getenv('DATA_FILE_PATH', '/mnt/data')

def create_folder(folder_name):
    """Create a folder in the mounted directory."""
    directory_path = os.path.join(mount_path, folder_name)

    try:
        # Use exist_ok=True to avoid raising an error if the folder already exists
        os.makedirs(directory_path, exist_ok=True)
        logging.info("Folder '%s' created successfully.", directory_path)
        return f"Folder '{folder_name}' created successfully in /mnt/data."
    except Exception as e:
        logging.error("Failed to create folder '%s': %s", directory_path, str(e))
        return f"Failed to create folder '{folder_name}': {str(e)}"

def test_file_mount():
    directory_path = mount_path
    content_list = []

    try:
        # List all files and directories in the specified path
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                content_list.append(f"Directory: {item}")
            else:
                content_list.append(f"File: {item}")
        logging.info("Contents of %s: %s", directory_path, ', '.join(content_list))
        return content_list
    except Exception as e:
        logging.error("An error occurred while accessing %s: %s", directory_path, str(e))
        print(f"An error occurred while accessing {directory_path}: {str(e)}")
        return []


@app.route("/")
def hello_world():
    """Example route to display contents of /mnt/data."""
    create_folder("FranciscoFolder")
    contents = test_file_mount()
    content_str = "<br>".join(contents)  # Join the list into a single string for HTML display
    return f"Contents of /mnt/data:<br>{content_str}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))