; Hotkey: Ctrl + Shift + Alt + A
; Description:
;   This hotkey runs the Python script `chat-as-gpt.py` with the argument "work_friend".
;   The argument "work_friend" is the name of the promtpt.
;   Refer to the documentation for additional information.

^+!a::
    Run, python "D:\Documents\GH\as-gpt\chat-as-gpt.py" "work_friend"
return
