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
 "pastebin.com", "-i", "testfile.txt"], stdout=subprocess.PIPE)
p_result = p.stdout()
print(p_result)
