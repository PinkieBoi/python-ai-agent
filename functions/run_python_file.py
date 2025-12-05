import os
import subprocess
from google.genai import types
from prompts import system_prompt


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if abs_working_dir not in abs_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        res = subprocess.run(
            ['python', abs_file_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode != 0:
            return f'Process exited with code {res.returncode}'
        if not res.output and not res.stderr:
            return 'No output was produced.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    finally:
        return f'STDOUT: {res.stdout}\nSTDERR: {res.stderr}'
 

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to be run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
 
available_functions = types.Tool(
    function_declarations=[schema_run_python_file],
) 

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
