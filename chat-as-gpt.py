import typing as t
from g4f.client import Client
import clipboard
import time
import os


CONFIG = {
    "work_directory": "F:\\Documents\\GitHub\\as-gpt",
    "window_timeout": 3
}
print(f"* Loaded config: {CONFIG}")

print("* Loading prompts...")
PROMPTS: t.Dict[str, str] = {}
for file in os.listdir(os.path.join(CONFIG.get("work_directory"), "prompts")):
    if file.endswith(".txt"):
        try:
            with open(os.path.join(CONFIG.get("work_directory"), "prompts", file), "r") as f:
                PROMPTS[file.split(".")[0]] = f.read()
        except Exception as e:
            print(f"Error while reading '{file}': {e}")

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
