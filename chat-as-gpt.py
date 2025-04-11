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
print("* Imported basic dependencies...")

from g4f.client import Client
print("* Imported gpt4free.")


CONFIG = {
    "work_directory": r"D:\Documents\GH\as-gpt",
    "window_timeout": 3
}
print(f"* Loaded config: {CONFIG}")

print("* Loading prompts...")
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

time.sleep(10)


def lookup_ai(source_text: str):
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user", 
                    "content": PROMPTS["work_friend"].format(source_text=source_text)
                }
            ],
            web_search=False
        )
        result = response.choices[0].message.content
        print(f"+ Result: {result}")
        clipboard.copy(result)

    except Exception as e:
        print(f"! Error in `lookup_ai`: {e}")


def main():
    SELECTED_TEXT = clipboard.paste().strip()
    if not isinstance(SELECTED_TEXT, str) or not SELECTED_TEXT:
        print(f"! Clipboard does not contain valid text.")
        return

    print(f"* Clipboard contains text: {SELECTED_TEXT}")
    lookup_ai(source_text=SELECTED_TEXT)


if __name__ == "__main__":
    main()
