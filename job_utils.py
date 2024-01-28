from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
import subprocess
import os
import json
import shutil 
import sys

session = PromptSession(history=FileHistory('.command_history'))


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.ENDC}")

class EnhancedPathCompleter(Completer):
    def __init__(self, file_extension=None):
        self.file_extension = file_extension

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        directory, partial = os.path.split(text)
        if not directory:
            directory = '.'
        for name in os.listdir(directory):
            if name.startswith(partial):
                path = os.path.join(directory, name)
                if os.path.isdir(path) or (self.file_extension and name.endswith(self.file_extension)):
                    yield Completion(name, start_position=-len(partial))

def fzf_file_search(file_extension):
    home_dir = os.path.expanduser('~')
    try:
        find_command = f"find {home_dir} -name '*{file_extension}'"
        fzf_command = 'fzf'
        command = f"{find_command} | {fzf_command}"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        selected_file = result.stdout.strip()
        if selected_file:
            return selected_file
        else:
            return None
    except Exception as e:
        print(f"Error during fzf search: {e}")
        return None

def select_directory_with_fzf():
    home_dir = os.path.expanduser('~')  # Get the user's home directory
    try:
        # Start the find command from the home directory and return absolute paths
        command = f"find {home_dir} -type d -not -path '*/.*' | fzf"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        selected_dir = result.stdout.strip()
        if selected_dir:
            # Convert to absolute path if it's not already
            return os.path.abspath(selected_dir) 
        else:
            return None
    except Exception as e:
        print(f"Error during fzf directory selection: {e}")
        return None

def get_output_file_path():
    selected_dir = select_directory_with_fzf()
    if not selected_dir:
        print("No directory selected.")
        return None

    # Convert to absolute path
    selected_dir = os.path.abspath(selected_dir)

    output_file_name = get_non_path_input("Enter output file name: ")
    return os.path.join(selected_dir, output_file_name)



def get_path_from_config(var_name):
    with open('config.json') as f:
        config = json.load(f)
    return config.get(var_name)


def get_path_input(prompt_text, file_extension=None):
    completer = EnhancedPathCompleter(file_extension=file_extension) if file_extension else None
    return session.prompt(prompt_text, completer=completer)

def get_non_path_input(prompt_text, color=Colors.OKBLUE):
    return input(color + prompt_text + Colors.ENDC)

def get_non_path_input_centered(prompt_text, color=Colors.OKBLUE):
    prompt_text_centered = center_text(prompt_text)
    return input(color + prompt_text_centered + Colors.ENDC)

# Function to center text based on the console's width
def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    return text.center(terminal_width)

def print_centered(message, color):
    centered_message = center_text(message)
    print(f"{color}{centered_message}{Colors.ENDC}")


def run_command(command):
    # Set to user's home directory. Change if different working directory is needed.
    home_dir = os.path.expanduser('~')

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=os.environ, cwd=home_dir)
        print("Command Output:\n", result.stdout)
        print("Error (if any):\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Stderr:\n", e.stderr)
