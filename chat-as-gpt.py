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
    def show_error_popup(message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Clipboard Error", message)
        root.destroy()

    @staticmethod
    def show_top_right_loading():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True)

        width, height = 250, 80
        screen_width = root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        root.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(root, text="⏳ Loading...", font=("Helvetica", 16),
                         fg="white", bg="black")
        label.pack(expand=True, fill="both")

        return root, label

    @staticmethod
    def update_to_success(root, label):
        label.config(text="✅ Success!", bg="green", fg="white")
        root.after(2000, root.destroy)  # auto-close after 2 seconds


def do_the_work(SELECTED_TEXT, root, label):
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPTS["work_friend"].format(
                source_text=SELECTED_TEXT)}],
            web_search=False
        )
        print(response.choices[0].message.content)

        # Switch to success message
        Utils.update_to_success(root, label)

    except Exception as e:
        root.destroy()
        Utils.show_error_popup(f"Error while generating response: {e}")


def main():
    SELECTED_TEXT = clipboard.paste().strip()
    if not isinstance(SELECTED_TEXT, str) or not SELECTED_TEXT:
        Utils.show_error_popup("Clipboard does not contain valid text.")
        return

    print("Clipboard contains text.")

    # Show overlay
    root, label = Utils.show_top_right_loading()

    # Run GPT call in background
    thread = threading.Thread(
        target=do_the_work, args=(SELECTED_TEXT, root, label))
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
