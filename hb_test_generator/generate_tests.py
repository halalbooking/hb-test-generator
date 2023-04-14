import os
import sys
import openai
import json
from pathlib import Path

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def get_prompt_file():
    prompt_file_name = 'test_generator_prompt.txt'
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    default_prompt_file = script_dir / prompt_file_name
    local_prompt_file = Path.cwd() / prompt_file_name

    if local_prompt_file.exists():
        prompt_file = local_prompt_file
    else:
        prompt_file = default_prompt_file

    return prompt_file


def get_openai_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Please set the OPENAI_API_KEY environment variable.")
        print("To obtain an API key, visit: https://platform.openai.com/account/api-keys")
        sys.exit(1)
    return api_key

def send_to_chatgpt(prompt, file_content):
    openai.api_key = get_openai_api_key()

    prompt = f"{prompt}\n{file_content}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def get_tests_file_info(base_prompt, file_path):
    prompt = f"Origin file path is {file_path}. What should be the path and filename of the tests file? Response shouldn't include any text except path and filename of the tests file. If below prompt has any information about tests file, like format/path/name/directory, take it into account: \n\n {base_prompt}."
    return send_to_chatgpt(prompt, "")

def save_tests_to_file(test_code, test_file_path):
    test_file_path = Path(test_file_path)
    test_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(test_file_path, "w") as test_file:
        test_file.write(test_code)

    return os.path.relpath(test_file_path, Path.cwd())

def main():
    if len(sys.argv) < 2:
        print("Usage: hb_generate_tests <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    prompt_file = get_prompt_file()
    base_prompt = read_file(prompt_file).strip()

    file_content = read_file(file_path)
    test_file_info = get_tests_file_info(base_prompt, file_path)
    print(f"Tests will be saved into file: {test_file_info}")

    test_code = send_to_chatgpt(base_prompt, file_content)
    test_file_path = save_tests_to_file(test_code, test_file_info)

    print("Done!")

if __name__ == "__main__":
    main()
