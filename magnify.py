import subprocess
import os
import socket
import requests
from tqdm import tqdm

def install_dependencies():
    print("Installing required packages...")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "lolcat", "cowsay", "figlet", "nmap", "gobuster", "nikto", "enum4linux", "smbclient"])
    print("Packages installed successfully.")

def clone_figlet_fonts():
    print("Cloning figlet-fonts repository...")
    subprocess.run(["git", "clone", "https://github.com/xero/figlet-fonts"])
    print("Repository cloned successfully.")

def move_figlet_fonts():
    print("Moving figlet-fonts contents to /usr/share/figlet...")
    subprocess.run(["sudo", "mv", "figlet-fonts/*", "/usr/share/figlet"])
    print("Contents moved successfully.")
    subprocess.run("figlet -f 3d M46n1fy | lolcat", shell=True)
    subprocess.run("cowsay  -f eyes Lets take a closer look | lolcat", shell=True)

def ping_website(url):
    try:
        ip_address = socket.gethostbyname(url)
        print(f"IP Address for {url}: {ip_address}")
        return ip_address
    except socket.gaierror:
        print("Hostname could not be resolved.")
        return None

def nmap_scan(url):
    print(f"Running Nmap scan on {url}...")
    result = subprocess.run(["sudo", "nmap", "-sV", "-Pn", url], capture_output=True, text=True)
    print(result.stdout)
    save_to_file(result.stdout, "nmap_results.txt")

def gobuster_scan(url):
    print(f"Running Gobuster scan on {url}...")
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    command = f"gobuster dir -u {url} -w {wordlist}"
    try:
        os.system(command)
    except Exception as e:
        print("Error running Gobuster:", e)

def print_common_vulnerabilities():
    print("Common vulnerabilities:")
    print("- Outdated software versions")
    print("- Weak or default credentials")
    print("- Cross-Site Scripting (XSS)")
    print("- Directory Traversal")
    # Add more vulnerabilities as needed

def dig_ip(ip_address):
    print(f"Running dig command on IP address {ip_address}...")
    result = subprocess.run(["dig", ip_address], capture_output=True, text=True)
    print(result.stdout)

def smb_scan(ip_address):
    print(f"Scanning for SMB on {ip_address}...")
    result = subprocess.run(["sudo", "nmap", "-p", "445", "--open", ip_address], capture_output=True, text=True)
    if "445/tcp" in result.stdout:
        print("SMB service found!")
        smb_connect(ip_address)
        enum4linux_scan(ip_address)
    else:
        print("No SMB service found.")

def smb_connect(ip_address):
    print("Connecting to SMB service...")
    subprocess.run(["smbclient", f"//{ip_address}/anonymous", "-U", "anonymous%anonymous"])

def ssh_scan(ip_address):
    print(f"Scanning for SSH on {ip_address}...")
    result = subprocess.run(["sudo", "nmap", "-p", "22", "--open", ip_address], capture_output=True, text=True)
    if "22/tcp" in result.stdout:
        print("SSH service found!")
        ssh_connect(ip_address)
    else:
        print("No SSH service found.")

def ssh_connect(ip_address):
    print("Connecting to SSH service...")
    subprocess.run(["hydra", "-L", "/usr/share/seclists/Usernames/top-usernames-shortlist.txt",
                    "-P", "/usr/share/wordlists/rockyou.txt",
                    "-t", "4", "-v", "-o", "ssh_crack_result.txt",
                    ip_address, "ssh"])

def whois_search(url):
    print(f"Running WHOIS search for {url}...")
    result = subprocess.run(["whois", url], capture_output=True, text=True)
    print(result.stdout)

def enum4linux_scan(ip_address):
    print(f"Running enum4linux scan on {ip_address}...")
    result = subprocess.run(["enum4linux", ip_address], capture_output=True, text=True)
    print(result.stdout)

def download_website(url):
    print(f"Downloading homepage source code from {url}...")
    response = requests.get(url)
    with open("source.html", "w") as f:
        f.write(response.text)
    print("Homepage source code saved to source.html")

def open_editor(filename):
    print(f"Opening {filename} in an editor...")
    subprocess.run(["nano", filename])

def scan_source_code(filename):
    print(f"Scanning website source code for keywords...")
    keywords = ["username", "admin", "administrator", "password"]
    with open(filename, "r") as f:
        source_code = f.read()
        for keyword in keywords:
            if keyword in source_code:
                print(f"Found '{keyword}' in the source code.")

def save_to_file(content, filename):
    with open(filename, "a") as f:
        f.write(content)
        f.write("\n")

def main():
    install_dependencies()
    clone_figlet_fonts()
    move_figlet_fonts()

    website_url = input("Enter the website URL (e.g., example.com): ")

    if website_url.startswith("https://"):
        url_prefix = "https://"
        website_url = website_url[len("https://"):]
    elif website_url.startswith("http://"):
        url_prefix = "http://"
        website_url = website_url[len("http://"):]
    else:
        url_prefix = "http://"

    ip_address = ping_website(website_url)

    if ip_address:
        nmap_scan(website_url)
        gobuster_scan(f"{url_prefix}{website_url}")
        print_common_vulnerabilities()
        dig_ip(ip_address)
        smb_scan(ip_address)
        ssh_scan(ip_address)
        whois_search(website_url)
        enum4linux_scan(ip_address)
        download_website(f"{url_prefix}{website_url}")
        open_editor("source.html")
        scan_source_code("source.html")
        subprocess.run("cowsay -f daemon 'You look surprised' | lolcat", shell=True)
        subprocess.run("echo Well...I guess we should do a little poking around | lolcat", shell=True)

if __name__ == "__main__":
    main()
