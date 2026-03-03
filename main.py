import os
import sys
import argparse


from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from call_functions import available_functions
from call_functions import call_function

def main():

  
    #Parse arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Load Environment and create client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)
    
    #Print prompt if verbose
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    #Create content and get response
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages, args.verbose)

def generate_content(client, messages, verbose):
    MAX_ITERATIONS = 20

    for iteration in range(MAX_ITERATIONS):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if not response:
            raise RuntimeError("Gemini API returned no response.")

        if not response.candidates:
            raise RuntimeError("No candidates returned from Gemini.")

        # ✅ Add all model responses to conversation history
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        # If no function calls → we are done
        if not response.function_calls:
            # Print final text response
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            print(part.text)
            break

        if verbose:
            print("Function calls:")

        function_responses = []

        # Execute all function calls
        for function_call in response.function_calls:
            if verbose:
                print(f"Calling function: {function_call.name}({function_call.args})")

            result = call_function(function_call, verbose=False)

            if not result:
                raise RuntimeError(
                    f"Function call {function_call.name} returned no result."
                )

            # Collect tool response parts
            function_responses.extend(result.parts)

        # ✅ Append tool results so model can see them next iteration
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

        if verbose:
            print(f"Iteration {iteration + 1} complete.\n")

    else:
        # If we exit loop normally (no break)
        print("Max iterations reached without final response.")
        exit(1)

    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
