import subprocess

script = '''tell application "Terminal"
    set bounds of front window to {0, 0, 1440, 900}
end tell

tell application "System Events"
    repeat 14 times
        key code 69 using {command down}
    end repeat
end tell'''

proc = subprocess.Popen(['osascript', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
stdout_output = proc.communicate(script)[0]
