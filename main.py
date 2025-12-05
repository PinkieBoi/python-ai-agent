import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
# contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."


all_available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ],
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    res = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[all_available_functions],
            system_instruction=system_prompt,
        )
    )
    metadata = res.usage_metadata
    if args.verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
        # if res.function_calls is not None:
        #     for function_call in res.function_calls:
        #         result = call_function(function_call, verbose=True)
        #         print(result)
    
    # if res.function_calls is not None:
    #     for function_call in res.function_calls:
    #         print(f"Calling function: {function_call.name}({function_call.args})")
    # else:
    #     print(res.text)
    if res.function_calls is not None:
        res_parts = []
        for function_call in res.function_calls:
            result = call_function(function_call, verbose=True)
            try:
                res_parts.append(result.parts[0].function_response.response)
            except Exception as e:
                print(f"Error: {e}")
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
        


if __name__ == "__main__":
    main()
