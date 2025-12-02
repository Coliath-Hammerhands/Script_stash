import subprocess


def fetch_ip():
    command = "curl ipaddress.ai"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())
    return result.stdout.strip()
