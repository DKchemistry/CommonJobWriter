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
