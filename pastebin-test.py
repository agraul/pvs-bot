#!/usr/bin/python3
import subprocess
import pyperclip
import shlex


'''
command_line = 'pastebinit -a PvS-Bot -b pastebin.com -i testfile.txt'
args = shlex.split(command_line)
p = subprocess.Popen(args)
link = pyperclip.paste
'''
p = subprocess.run(["pastebinit", "-a", "PvS-Bot", "-b",
 "pastebin.com", "-i", "testfile.txt"])
p_result = p.CompletedProcess.stdout()
print(p_result)
