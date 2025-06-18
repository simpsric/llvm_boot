import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file in the specified working directory.
    Args:
        working_directory (str): The base directory where the file should be written.
        file_path (str): The relative path of the file to write.
        content (str): The content to write to the file.
    Returns:
        str: A message indicating success or failure.
    """
    # Create an absolute path for the working directory and target file
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the target file is within the working directory
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Try to write the content to the file, creating files and directories as needed
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        # Write the content to the file
        with open(target_file, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"