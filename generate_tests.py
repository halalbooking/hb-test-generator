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

    prompt = f"write tests for this code:\n{file_content}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def save_tests_to_file(test_code):
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)

    test_file_path = tests_dir / "generated_tests.py"
    with open(test_file_path, "w") as test_file:
        test_file.write(test_code)

    return test_file_path.relative_to(Path.cwd())

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_content = read_file(file_path)
    test_code = send_to_chatgpt(file_content)
    test_file_path = save_tests_to_file(test_code)

    print(f"Tests created: {test_file_path}")

if __name__ == "__main__":
    main()
