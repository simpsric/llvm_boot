import os, sys
from dotenv import load_dotenv
from google.genai import types, Client
from functions import get_files_info, get_file_content, write_file, run_python


MAX_LOOPS = 20

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of files
- Write content to files
- Run Python code in the working directory

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

function_dict = {
    "get_files_info": get_files_info.get_files_info,
    "get_file_content": get_file_content.get_file_content,
    "write_file": write_file.write_file,
    "run_python_file": run_python.run_python_file,
}

def call_function(function_call_part, verbose=False):
    """
    Calls the specified function with the provided arguments.
    
    Args:
        function_call_part (types.Part): The part containing the function call details.
        verbose (bool): If True, prints additional information about the function call.
        
    Returns:
        str: The result of the function call.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name} with args: {function_call_part.args}")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    print(f" - Arguments: {function_call_part.args}")
    
    # If the name is not in the dict, return an error message
    if function_call_part.name not in function_dict:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
        )
    else:
        function_result = function_dict[function_call_part.name](
        working_directory="calculator",
        **function_call_part.args
        )
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

schema_excute_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_excute_python,
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

param_count = len(sys.argv)

if param_count < 2:
    print("Usage: python main.py <prompt>")
    sys.exit(1)

prompt = sys.argv[1]

if param_count >= 3 and sys.argv[2] == "--verbose":
    b_verbose_set = True
else:
    b_verbose_set = False

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

# Load environment variables from .env file
load_dotenv()
# Get the value of the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

client = Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=config
)

for i in range(1,MAX_LOOPS):
    if response.candidates:
        for candidate in response.candidates:
            if b_verbose_set:
                print(f"Candidate {i}: {candidate.text}")
            messages.append(candidate.content)
        if response.function_calls and i < MAX_LOOPS:
            for function_call in response.function_calls:
                if b_verbose_set:
                    print(f"Function call detected: {function_call.name}")
                call_result = call_function(function_call, verbose=b_verbose_set)
                if call_result.parts[0].function_response.response:
                    if b_verbose_set:
                        print(f"-> {call_result.parts[0].function_response.response}")
                    messages.append(call_result)
                else:
                    raise ValueError(
                        f"Function {function_call.name} did not return a valid response."
                    )
        else:
            # If no function calls or at max loops, break the loop
            break
    else:
        # If no candidates, break the loop
        break
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config
    )
    
print(response.text)
if b_verbose_set:
    print(f"User prompt: {prompt}")
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    