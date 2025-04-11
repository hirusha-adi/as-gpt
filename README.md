# 🧠 Chat as GPT

A windows utility to chat anywhere like a pro.

## 📁 Project Structure

```bash
chat-as-gpt/
│
├── chat-as-gpt.py       # Main Python script
├── chat-as-gpt.ahk      # AutoHotkey script to launch with a hotkey
└── prompts/
    ├── work_friend.txt  # Example prompt template
    └── ...              # Add your custom `.txt` prompts here
```

## 🔧 Setup

### Dependencies

Ensure Python 3 is installed and the following Python packages:

```bash
pip install g4f[all] clipboard
```

Or, install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

You’ll also need [AutoHotkey](https://www.autohotkey.com/) installed if you plan to use the hotkey launcher.

### Prompt Templates

Create your prompt templates as `.txt` files inside the `prompts/` folder. Each prompt must include `{source_text}` as a placeholder. 

Example: `prompts/work_friend.txt`


```
You are a friendly colleague. Help me rephrase the following professionally:

{source_text}
```

## 🖱️ Basic Usage

1. Edit the script and it's paths. Check the [configuration section](#️-configuration) for more information.
2. Copy some text to your clipboard.
3. Run the script from a terminal:
    ```bash
    python chat-as-gpt.py work_friend
    ```
4. The script:
    - Loads the chosen prompt.
    - Inserts your copied text.
    - Sends it to GPT-4o-mini.
    - Copies the AI's response back to your clipboard.

## ⚡ Using the Hotkey (Windows Only)

Your AutoHotkey script binds this action to `Ctrl + Shift + Alt + A` by default.

#### 1. Make sure `chat-as-gpt.ahk` contains:

```ahk
^+!a::
    Run, python "D:\Documents\GH\as-gpt\chat-as-gpt.py" "work_friend"
return
```

> 💡 Update the path if your script is in a different location.

#### 2. Run the AHK script (double-click it), and then:

- Select and copy some text.
- Press `Ctrl + Shift + Alt + A`
- Your clipboard will be updated with the AI’s response within a few seconds.

## ⚙️ Configuration

The script has a `CONFIG` dictionary at the top. Make sure to update the `work_directory` before starting the script.

```python
CONFIG = {
    "work_directory": r"D:\path\to\script",
    "window_timeout": 3,      # Seconds to wait before auto-exiting on errors
    "ai_timeout": 8,          # Max time to wait for a response
    "exit_after_timeout": True
}
```

## 🧪 Tips

- Add new prompt files inside prompts/ and call them with:
    ```python
    python chat-as-gpt.py your_prompt_name
    ```
- The script automatically detects if your clipboard is empty and exits cleanly with a helpful message.

## 🛠️ Troubleshooting

- **Clipboard is empty**: Ensure you’ve copied text before triggering.
- **Prompt not found**: Double-check the prompt file name (without `.txt`) in the `prompts/` folder.
- **Slow response**: Increase `ai_timeout` if your AI provider is taking longer.
