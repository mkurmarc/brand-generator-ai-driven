import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 12

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)

    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH}.\
            Submitted input is {user_input}"
        )


def validate_length(prompt: str) -> bool:
    return len(prompt) <= 12


def generate_keywords(prompt: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"Generate related branding keywords for the {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text
    keywords_text: str = response["choices"][0]["text"]

    # Split text into an array
    keywords_array = re.split(",|\n|;|-", keywords_text)

    # Removes empty strings. Strip white space and lowercase for the other strings
    keywords_array = [ k.strip().lower() for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")
    return keywords_array


def generate_branding_snippet(prompt: str) -> List[str]:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"Generate up beat branding snipet for {prompt}:"
    print(enriched_prompt)
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text
    branding_text: str = response["choices"][0]["text"]

    # Strip white space and quotation marks
    branding_text = branding_text.strip(' "\'\t\r\n')

    # Add ... to truncated statements
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."

    print(f"Snippet: {branding_text}")
    return branding_text


if __name__ == "__main__":
    main()