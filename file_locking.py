import subprocess
import shutil
import os
def is_file_open(file_name):
    # Executing the WMIC command and capturing its output
    process = subprocess.Popen(['WMIC', 'path', 'win32_process', 'get', 'CommandLine'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # Checking if the file is in the command line of any process
    for line in stdout.splitlines():
        if file_name in line:
            return True
    return False


def create_backup(file_path: str, backup_directory: str) -> str:
    # Ensure backup directory exists
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    backup_file_name = os.path.basename(file_path)
    backup_file_path = os.path.join(backup_directory, backup_file_name)

    shutil.copy(file_path, backup_file_path)
    return backup_file_path

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
           # print(content)
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")