import os

MAX_CHARS = 10000  # Limit for file content size

def get_files_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, 'r') as file:
            content = file.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error reading file: {e}"