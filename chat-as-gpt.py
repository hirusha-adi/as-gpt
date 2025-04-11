print(r"""
╔═╗┬ ┬┌─┐┌┬┐  ╔═╗┌─┐  ╔═╗╔═╗╔╦╗
║  ├─┤├─┤ │   ╠═╣└─┐  ║ ╦╠═╝ ║ 
╚═╝┴ ┴┴ ┴ ┴   ╩ ╩└─┘  ╚═╝╩   ╩ 
        by @hirushaadi
""")


import typing as t
import clipboard
import time
import os
from multiprocessing import Process
print("* Imported basic dependencies.")

from g4f.client import Client
print("* Imported gpt4free.")

def init():
    print("* Initializing stuff...")

    CONFIG = {
        "work_directory": r"D:\Documents\GH\as-gpt",
        "window_timeout": 3
    }
    print(f"* Loaded config: {CONFIG}")

    print("* Loading prompts.")
    PROMPTS: t.Dict[str, str] = {}
    for filename in os.listdir(os.path.join(CONFIG.get("work_directory"), "prompts")):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(CONFIG.get("work_directory"), "prompts", filename), "r") as file:
                    PROMPTS[filename.split(".")[0]] = file.read()
            except Exception as e:
                print(f"Error while reading '{filename}': {e}")

    if len(PROMPTS) == 0:
        print("! No prompts found.")
        time.sleep(CONFIG.get("window_timeout"))
        exit()

    print(f"* Loaded {len(PROMPTS)} prompts: {[k for k in PROMPTS.keys()]}")

    return CONFIG, PROMPTS


def generate_result(prompt: str):
    try:
        client = Client()
        print("* `g4f.client.Client` initialized.")
        print("* Generating the result - please wait...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            web_search=False
        )
        result = response.choices[0].message.content
        print(f"+ Generated the result: {result}")

        clipboard.copy(result)
        print(f"+ Copied the result to clipboard.")

    except Exception as e:
        print(f"! Error in `generate_result`: {e}")


def main():
    CONFIG, PROMPTS = init()
    print("* Initialized.")

    print("* Reading clipboard.")
    SELECTED_TEXT = clipboard.paste().strip()
    if not isinstance(SELECTED_TEXT, str) or not SELECTED_TEXT:
        print(f"! Clipboard does not contain valid text.")
        exit()
    print(f"* Clipboard contains text: {SELECTED_TEXT}")

    print("* Analyzing the text.")
    prompt = PROMPTS.get("work_friend").format(source_text=SELECTED_TEXT)
    generate_result(prompt=prompt)

    print("+ Bye Bye!")


if __name__ == "__main__":
    try:
        main()
        input("Press [ENTER] to exit.")
    except (KeyboardInterrupt, Exception):
        exit()
