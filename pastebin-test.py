#!/usr/bin/python3
import subprocess
import pyperclip
import shlex

command_line = 'pastebinit -b pastebin.com -i testfile.txt'
args = shlex.split(command_line)
p = subprocess.Popen(args)
link = pyperclip.paste
print(link)
