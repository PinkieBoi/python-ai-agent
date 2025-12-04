import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
# contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."


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
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )
    metadata = res.usage_metadata
    if args.verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
    
    if res.function_calls is not None:
        for function_call in res.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(res.text)
        


if __name__ == "__main__":
    main()
