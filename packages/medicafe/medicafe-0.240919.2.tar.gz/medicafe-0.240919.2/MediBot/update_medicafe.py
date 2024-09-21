import subprocess, sys, requests

def get_installed_version(package):
    try:
        import pkg_resources
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return None

def get_latest_version(package):
    try:
        response = requests.get("https://pypi.org/pypi/{}/json".format(package), timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.RequestException as e:
        print("Error fetching latest version: {}".format(e))
        return None

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def compare_versions(version1, version2):
    v1_parts = list(map(int, version1.split(".")))
    v2_parts = list(map(int, version2.split(".")))
    return (v1_parts > v2_parts) - (v1_parts < v2_parts)

def upgrade_package(package):
    try:
        if not check_internet_connection():
            print("Error: No internet connection detected. Please check your internet connection and try again.")
            sys.exit(1)
        
        print("Attempting to upgrade {}...".format(package))
        process = subprocess.Popen([sys.executable, '-m', 'pip', 'install', '--upgrade', package, '--no-cache-dir', '--disable-pip-version-check'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Stream output with progress
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print("Error: Upgrade failed.")
            print("stderr:", stderr.decode())
            sys.exit(1)
        
        print("Upgrade completed successfully.")
    except Exception as e:
        print("Error during upgrade:", e)
        sys.exit(1)

def main():
    package = "medicafe"
    
    current_version = get_installed_version(package)
    if not current_version:
        print("{} is not installed.".format(package))
        sys.exit(1)
    
    latest_version = get_latest_version(package)
    if not latest_version:
        print("Could not retrieve the latest version information.")
        sys.exit(1)
    
    print("Current version of {}: {}".format(package, current_version))
    print("Latest version of {}: {}".format(package, latest_version))
    
    if compare_versions(latest_version, current_version) > 0:
        print("A newer version is available. Proceeding with upgrade.")
        upgrade_package(package)
        
        # Verify upgrade
        new_version = get_installed_version(package)
        if compare_versions(new_version, latest_version) >= 0:
            print("Upgrade successful. New version: {}".format(new_version))
        else:
            print("Upgrade failed. Current version remains: {}".format(new_version))
            sys.exit(1)
    else:
        print("You already have the latest version installed.")

if __name__ == "__main__":
    main()
