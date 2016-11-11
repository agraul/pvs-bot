#!/usr/bin/python3
import subprocess
import pyperclip
import shlex

''' What happens:
    printed: <function _pasteXclip at 0x..> inside python
    new shell output/python session: link
    stuck inside python
'''
command_line = 'pastebinit -a PvS-Bot -b pastebin.com -i testfile.txt'
args = shlex.split(command_line)
p = subprocess.Popen(args)
link = pyperclip.paste
#print(link)
