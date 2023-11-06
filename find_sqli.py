import subprocess

def find_sqli_vulnerabilities(url):
    command = [
        "python3",
        "sqli_engine/sqlmap.py",
        "-u", url,
        "--forms",
        "--batch",
        "--crawl=2",
        "--level=3",
        "--risk=3",
        "--threads=2"
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    return stdout.decode('utf-8'), stderr.decode('utf-8')

