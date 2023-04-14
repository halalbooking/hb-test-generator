import os
import sys
import openai
import json
from pathlib import Path

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def send_to_chatgpt(file_content):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    prompt_file_name = 'test_generator_prompt.txt'
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    default_prompt_file = script_dir / prompt_file_name
    local_prompt_file = Path.cwd() / prompt_file_name

    if local_prompt_file.exists():
        prompt_file = local_prompt_file
    else:
        prompt_file = default_prompt_file

    base_prompt = read_file(prompt_file).strip()

    prompt = f"{base_prompt}\n{file_content}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(response.choices[0].text.strip())

    return response.choices[0].text.strip()

def save_tests_to_file(test_code):
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)

    test_file_path = tests_dir / "generated_tests.js"
    with open(test_file_path, "w") as test_file:
        test_file.write(test_code)

    return os.path.relpath(test_file_path, Path.cwd())

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_content = read_file(file_path)
    test_code = send_to_chatgpt(file_content)
    test_file_path = save_tests_to_file(test_code)

if __name__ == "__main__":
    main()
