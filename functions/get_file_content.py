import os
from google.genai import types
from prompts import system_prompt


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if abs_working_dir not in abs_target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(abs_target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"' 
    try:
        with open(abs_target_path, "r") as file:
            content = file.read()
            if len(content) > 10000:
                content = file.read(10000) + '[...File "{file_path}" truncated at {MAX_LENGTH} characters]'
    except Exception as e:
        return f'Error: {str(e)}'
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, truncated to 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list contents from."
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[schema_get_file_content],
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
