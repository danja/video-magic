import subprocess
import sys
import argparse


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def install_package(package):
    print(f"\nAttempting to install {package}")
    returncode, stdout, stderr = run_command(f"pip install {package}")

    if returncode != 0:
        print(f"Failed to install {package}. Error:\n{stderr}")
        print(f"Attempting to update hash for {package}")

        hashin_code, hashin_out, hashin_err = run_command(
            f"hashin -v {package}")

        if hashin_code != 0:
            print(f"Failed to update hash for {package}. Error:\n{hashin_err}")
            return False

        print(f"Hash updated for {package}. Retrying installation.")

        returncode, stdout, stderr = run_command(f"pip install {package}")

        if returncode != 0:
            print(f"Failed to install {
                  package} after hash update. Error:\n{stderr}")
            return False

    print(f"Successfully installed {package}")
    return True


def main(requirements_file):
    try:
        with open(requirements_file, 'r') as file:
            packages = file.readlines()
    except FileNotFoundError:
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

    packages = [pkg.strip() for pkg in packages if pkg.strip()
                and not pkg.startswith('#')]

    for package in packages:
        success = install_package(package)
        if not success:
            print(f"Warning: Failed to install {package}")

    print("\nInstallation process completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install packages from a requirements file.")
    parser.add_argument("requirements_file",
                        help="Path to the requirements.txt file")
    args = parser.parse_args()

    main(args.requirements_file)
