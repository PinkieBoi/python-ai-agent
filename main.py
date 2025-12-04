import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
        contents=messages
    )
    metadata = res.usage_metadata
    if args.verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
    print(res.text)


if __name__ == "__main__":
    main()
