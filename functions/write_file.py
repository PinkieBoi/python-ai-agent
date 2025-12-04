import os
from google.genai import types
from prompts import system_prompt


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if abs_working_dir not in abs_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))
    with open(abs_file_path, 'w') as file:
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to file"
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[schema_write_file],
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
