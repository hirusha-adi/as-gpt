from g4f.client import Client
import clipboard
import tkinter as tk
from tkinter import messagebox
import threading


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

    @staticmethod
    def show_loading_overlay():
        root = tk.Tk()
        root.overrideredirect(True)  # Hide title bar
        root.attributes('-topmost', True)
        root.configure(bg="black")

        # Set dimensions
        width, height = 250, 80
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = screen_width - width - 20  # 20px padding from right
        y = 20  # 20px padding from top

        root.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(root, text="⏳ Loading...", font=(
            "Helvetica", 16), fg="white", bg="black")
        label.pack(expand=True, fill="both")

        return root


def do_the_work(SELECTED_TEXT, loading_overlay):
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPTS["work_friend"].format(
                source_text=SELECTED_TEXT)}],
            web_search=False
        )

        print(response.choices[0].message.content)
    except Exception as e:
        Utils.show_error_popup(f"Error while generating response: {e}")
    finally:
        loading_overlay.destroy()  # Close loading screen


def main():
    # get text from clipboard
    # ----------------------------------------
    SELECTED_TEXT = clipboard.paste().strip()
    if not isinstance(SELECTED_TEXT, str) or not SELECTED_TEXT:
        Utils.show_error_popup("Clipboard does not contain valid text.")
        return

    # documentation: https://github.com/xtekky/gpt4free?tab=readme-ov-file#-text-generation
    # Show fullscreen overlay
    loading_overlay = Utils.show_loading_overlay()

    # Run the heavy task in a separate thread to avoid freezing the GUI
    thread = threading.Thread(
        target=do_the_work, args=(SELECTED_TEXT, loading_overlay))
    thread.start()

    # Start tkinter mainloop to display the overlay
    loading_overlay.mainloop()


if __name__ == "__main__":
    main()
