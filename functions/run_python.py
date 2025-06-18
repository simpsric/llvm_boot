import os, subprocess

def run_python_file(working_directory, file_path):
    """
    Run a Python file in the specified working directory.
    
    Args:
        working_directory (str): The base directory where the Python file is located.
        file_path (str): The relative path of the Python file to run.
        
    Returns:
        str: The output of the Python script or an error message.
    """
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        # Set up the subprocess to run the Python file
        result = subprocess.run(
            ['python', file_path],
            cwd=abs_working_dir,
            capture_output=True,
            timeout=30,
            text=True
        )
        output = []
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append(f"Error: {result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Script exited with code {result.returncode}")
        if not output:
            output.append("No output from the script.")
        output.append(f'Successfully executed "{file_path}"')
        return "\n".join(output)
    except Exception as e:
        return f"Error executing file: {e}"