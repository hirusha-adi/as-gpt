from g4f.client import Client
import clipboard
import tkinter as tk
from tkinter import messagebox


class Prompts:
    work_friend = "You are a helpful assistant that improves the grammar, tone, and flow of user-written messages. Your goal is to make messages sound human, slightly professional, and polished - without removing the original personality or wording too much. Use the user's exact words as much as possible, fixing only what's necessary to improve clarity, correctness, and tone. The end result should still feel like the user wrote it - just cleaner and more natural. Here is the original message. Rewrite it accordingly. Original message: {source_text}"


PROMPTS = {
    "work_friend": Prompts.work_friend
}


class Utils:
    @staticmethod
    def show_error_popup(message):
        root = tk.Tk()
        root.withdraw()  # hide the main tkinter window
        messagebox.showerror("Clipboard Error", message)
        root.destroy()


def main():
    # get text from clipboard
    # ----------------------------------------
    SELECTED_TEXT = clipboard.paste().strip()
    if isinstance(SELECTED_TEXT, str):
        print("Clipboard contains text:")
    else:
        Utils.show_error_popup("Clipboard does not contain valid text.")

    # documentation: https://github.com/xtekky/gpt4free?tab=readme-ov-file#-text-generation
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPTS["work_friend"].format(
            source_text="Hey, what did the boss say bro? will he kick my ass and should i start looking for a new job?")}],
        web_search=False
    )
    print(response.choices[0].message.content)
