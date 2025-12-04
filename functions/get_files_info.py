import os
from google.genai import types
from prompts import system_prompt


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if abs_working_dir not in abs_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(abs_target_dir)
    files_info = []
    for file_name in files:
        file_path = os.path.join(abs_target_dir, file_name)
        files_info.append(f"- {file_name}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
    return "\n".join(files_info)


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

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
