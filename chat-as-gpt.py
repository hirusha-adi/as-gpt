# ────────────── 🔧 CONFIGURATION ──────────────
CONFIG = {
    "work_directory": r"D:\Documents\GH\as-gpt",
    "window_timeout": 3,
    "ai_timeout": 8,
    "exit_after_timeout": True
}


# ────────────── ✨ ASCII Header ──────────────
print(r"""
╔═╗┬ ┬┌─┐┌┬┐  ╔═╗┌─┐  ╔═╗╔═╗╔╦╗
║  ├─┤├─┤ │   ╠═╣└─┐  ║ ╦╠═╝ ║ 
╚═╝┴ ┴┴ ┴ ┴   ╩ ╩└─┘  ╚═╝╩   ╩ 
        by @hirushaadi
""")


# ────────────── 📦 DEPENDENCIES ──────────────
import os
import sys
import time
import typing as t
import clipboard
import concurrent.futures
print("* Imported basic dependencies.")

from g4f.client import Client
print("* Imported gpt4free.")


# ────────────── 📦 UTILS ──────────────
def exit_with_timeout():
    time.sleep(CONFIG["window_timeout"])
    exit()

def timeout_function(func, args=(), kwargs={}, timeout=3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        start_time = time.perf_counter()
        future = executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout)
            elapsed = time.perf_counter() - start_time
            print(f"* Function completed in {elapsed:.2f} seconds.")
            return result
        except concurrent.futures.TimeoutError:
            elapsed = time.perf_counter() - start_time
            print(f"! Timed out after {timeout} seconds (elapsed: {elapsed:.2f} seconds).")
            exit()

def load_prompts(directory: str) -> t.Dict[str, str]:
    print("* Loading prompts...")
    prompts = {}
    prompt_dir = os.path.join(directory, "prompts")
    for filename in os.listdir(prompt_dir):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(prompt_dir, filename), "r", encoding="utf-8") as file:
                    prompts[filename.split(".")[0]] = file.read()
            except Exception as e:
                print(f"! Error while reading '{filename}': {e}")
    print(f"* Loaded {len(prompts)} prompt(s): {list(prompts.keys())}")
    return prompts

def generate_result(prompt: str):
    try:
        client = Client()
        print("* Client initialized. Sending prompt to AI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )
        result = response.choices[0].message.content
        print(f"+ Response received: {result}")
        clipboard.copy(result)
        print("+ Result copied to clipboard.")
    except Exception as e:
        print(f"! Error during AI generation: {e}")


# ────────────── 🚀 MAIN ──────────────
def main():
    print("* Initializing...")
    print(f"* Config loaded: {CONFIG}")

    prompts = load_prompts(CONFIG["work_directory"])
    if not prompts:
        print("! No prompts found. Exiting...")
        exit_with_timeout()

    print("* Reading clipboard...")
    selected_text = clipboard.paste().strip()
    if not selected_text:
        print("! Clipboard does not contain valid text.")
        exit_with_timeout()
    print(f"* Clipboard text: {selected_text}")

    try:
        print(f"* Arguments: {sys.argv[:]}")
        prompt_name = sys.argv[1]
    except IndexError:
        print("! Error: You must specify the prompt name as the argument.")
        exit_with_timeout()
    
    if prompt_name:
        if not (prompt_name in prompts):
            print(f"! Prompt '{prompt_name}' not found. Exiting...")
            exit_with_timeout()
        else:
            print(f"* Using prompt: {prompt_name}")
    else:
        print("* Prompt not specified. Using default prompt.")
        prompt_name = "work_friend"
            

    print("* Building prompt from clipboard content...")
    formatted_prompt = prompts[prompt_name].format(source_text=selected_text)

    timeout_function(
        generate_result,
        args=(formatted_prompt,),
        timeout=CONFIG["ai_timeout"]
    )

    print("+ Done. Bye Bye!")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, Exception):
        input("Press [ENTER] to exit.")
        print("\n! Interrupted. Exiting...")
