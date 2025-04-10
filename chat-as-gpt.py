from g4f.client import Client
import clipboard
import tkinter as tk
from tkinter import messagebox
import threading
import time


class Prompts:
    work_friend = "You are a helpful assistant that improves the grammar, tone, and flow of user-written messages. Your goal is to make messages sound human, slightly professional, and polished - without removing the original personality or wording too much. Use the user's exact words as much as possible, fixing only what's necessary to improve clarity, correctness, and tone. The end result should still feel like the user wrote it - just cleaner and more natural. Here is the original message. Rewrite it accordingly. Original message: {source_text}"


PROMPTS = {
    "work_friend": Prompts.work_friend
}


class Utils:
    @staticmethod
    def show_error_popup(message: str) -> None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Clipboard Error", message)
        root.destroy()

    @staticmethod
    def show_top_right_loading():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True)

        # place window at top right corner
        width, height = 250, 80
        screen_width = root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        root.geometry(f"{width}x{height}+{x}+{y}")

        # text label
        label = tk.Label(root, text="⏳ Loading...", font=("Helvetica", 16), fg="white", bg="black")
        label.pack(expand=True, fill="both")

        return root, label

    @staticmethod
    def update_to_success(root: tk.Tk, label: tk.Label):
        label.config(text="✅ Success!", bg="green", fg="white")
        root.after(2000, root.destroy)

    @staticmethod
    def update_to_error(root: tk.Tk, label: tk.Label):
        label.config(text="\u274E Error!", bg="red", fg="white")
        root.after(2000, root.destroy)


def handle_output(result: str) -> None:
    clipboard.copy(result)


def lookup_ai(SELECTED_TEXT: str, root: tk.Tk, label: tk.Label):
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user", 
                    "content": PROMPTS["work_friend"].format(source_text=SELECTED_TEXT)
                }
            ],
            web_search=False
        )
        result = response.choices[0].message.content
        handle_output(result=result)

        Utils.update_to_success(root=root, label=label)

    except Exception as e:
        root.destroy()
        Utils.show_error_popup(f"Error while generating response: {e}")


def main():
    SELECTED_TEXT = clipboard.paste().strip()
    if not isinstance(SELECTED_TEXT, str) or not SELECTED_TEXT:
        Utils.show_error_popup("Clipboard does not contain valid text.")
        return

    print("Clipboard contains text.")

    # overlay
    root, label = Utils.show_top_right_loading()

    # use ai with a seperate thread
    thread = threading.Thread(target=lookup_ai, args=(SELECTED_TEXT, root, label))
    thread.start()

    # show window after the thread is started
    root.mainloop()


if __name__ == "__main__":
    main()
