from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import sys
from job_utils import *


def stereo_enum_task():
    print_colored(
        "Running Stereochemical Enumeration (Unassigned Stereocenter Only) \n",
        Colors.HEADER,
    )

    mct_path = get_path_from_config("mct_path")
    conda_path = get_path_from_config("conda_path")

    print_colored(f"MCT Path via config: {mct_path}", Colors.OKGREEN)
    print_colored(f"Conda path via config: {conda_path}\n", Colors.OKGREEN)

    print_colored(
        "Choose input method for input file (*.smi):\n"
        + "1. Manual Filepath Input\n"
        + "2. fzf File Search\n",
        Colors.HEADER,
    )

    input_choice = get_non_path_input("Enter choice (1 or 2) for input file: \n")

    if input_choice == "1":
        input_file = get_path_input("Enter input file path: ", file_extension=".smi")
        print(f"Input file selected: {input_file}\n")

    elif input_choice == "2":
        input_file = fzf_file_search(".smi")
        print(f"Input file selected: {input_file}\n")
        if not input_file:
            print("No file selected.")
            return
    else:
        print("Invalid choice.")
        return

    print_colored(
        "Choose output method:\n"
        + "1. Manual Filepath Input\n"
        + "2. fzf Directory Search\n",
        Colors.HEADER,
    )

    output_choice = get_non_path_input("Enter choice (1 or 2) for output file: ")

    if output_choice == "1":
        output_file = get_path_input("Enter output file path (.smi): ")
        print(f"Output file selected: {output_file}\n")
    elif output_choice == "2":
        output_file = get_output_file_path()
        print(f"Output file selected: {output_file}\n")
        if not output_file:
            print("No output path specified.")
            return
    else:
        print("Invalid choice.")
        return

    command = f"{conda_path} {mct_path}/RDKitEnumerateStereoisomers.py -i {input_file} -d no -m UnassignedOnly -o {output_file}"
    print(f"Running command: {command}")

    confirm_choice = get_non_path_input("Confirm (y/n): ")
    if confirm_choice == "y":
        run_command(command)
    else:
        print("Aborting.")
        sys.exit()


def ligprep_task():
    schrodinger_path = get_path_from_config("schrodinger_path")
    ligprep_inp = get_path_from_config("ligprep_inp")

    print(f"Schrodinger Path: {schrodinger_path}")
    print(f"Ligprep Input File: {ligprep_inp}")

    print_centered(
        "Choose input method:\n" + "1. Manual Filepath Input\n" + "2. fzf File Search",
        Colors.HEADER,
    )

    input_choice = get_non_path_input("Enter choice (1 or 2): ")

    if input_choice == "1":
        input_file = get_path_input("Enter input file path: ", file_extension=".smi")
        print(f"Input file selected: {input_file}\n")
    elif input_choice == "2":
        input_file = fzf_file_search(".smi")
        print(f"Input file selected: {input_file}\n")
        if not input_file:
            print("No file selected.")
            return
    else:
        print("Invalid choice.")
        return

    output_sdf = get_path_input("Enter output .sdf path: ", file_extension=".sdf")
    print(f"Output file selected: {output_sdf}\n")
    cpus = get_non_path_input("Enter the number of CPUs to use: ")
    njobs = get_non_path_input("Enter the number of jobs to run: ")
    job_name = get_non_path_input("Enter the job name: ")
    command = f"{schrodinger_path}/ligprep -inp {ligprep_inp} -ismi {input_file} -osd {output_sdf} -HOST localhost:{cpus} -NJOBS {njobs} -JOBNAME {job_name}"

    print(f"Running command: {command}")

    confirm_choice = get_non_path_input("Confirm (y/n): ")
    if confirm_choice == "y":
        run_command(command)
    else:
        print("Aborting.")
        sys.exit()


def glide_docking_task():
    schrodinger_path = get_path_from_config("schrodinger_path")
    print(f"Schrodinger Path: {schrodinger_path}")

    print_colored(
        "Choose output directory method:\n"
        + "1. Manual Filepath Input\n"
        + "2. fzf Directory Search",
        Colors.HEADER,
    )

    output_choice = get_non_path_input("Enter choice (1 or 2) for output directory: ")

    if output_choice == "1":
        output_dir = get_path_input("Enter output directory path: ")
    elif output_choice == "2":
        output_dir = select_directory_with_fzf()
        if not output_dir:
            print("No directory selected.")
            return
    else:
        print("Invalid choice.")
        return

    print(f"Output directory selected: {output_dir}\n")
    input("Press 'Enter' to begin searching for a grid file (.zip)")
    grid_file = fzf_file_search(".zip")
    print(f"Grid file selected: {grid_file}\n")

    input("Press 'Enter' to begin searching for a ligand file (.sdf)")
    ligand_file = fzf_file_search(".sdf")
    print(f"Ligand file selected: {ligand_file}\n")

    in_file_name = get_non_path_input("Enter .in file name (must end with `.in`): ")
    in_file_path = os.path.join(output_dir, in_file_name)

    write_in_file(in_file_path, grid_file, ligand_file, output_dir)
    print_in_file(in_file_path)

    cpus = get_non_path_input("Enter the number of CPUs to use: ")
    njobs = get_non_path_input("Enter the number of jobs to run: ")
    job_name = get_non_path_input("Enter the job name: ")
    command = f"{schrodinger_path}/glide -HOST localhost:{cpus} -NJOBS {njobs} -JOBNAME {job_name} {in_file_path}"

    print(f"Running command: {command}")

    confirm_choice = get_non_path_input("Confirm (y/n): ")
    if confirm_choice == "y":
        run_command(command)
    else:
        print("Aborting.")
        sys.exit()


# Task registration dictionary
tasks = {
    "stereo_enum": stereo_enum_task,
    "ligprep": ligprep_task,
    "glide_docking": glide_docking_task,
    # Add new tasks here as you create them
}

# Task descriptions
task_descriptions = {
    "stereo_enum": "Stereochemical Enumeration (Unenumerated Stereocenter Only)",
    "ligprep": "Ligprep (SMILES to SDF, no epik, uses ligprep.inp)",
    "glide_docking": "Glide Docking (SDF to SDF, makes glide.in)",
    # Add descriptions for new tasks here
}


def main():
    print(Colors.OKGREEN + Colors.BOLD + "\nTask Options:\n" + Colors.ENDC)
    for idx, key in enumerate(tasks, start=1):
        task_name = task_descriptions.get(key, "Unknown Task")
        print(f"{idx}. {Colors.BOLD}{task_name}{Colors.ENDC}")
    print("\n")

    choice = int(get_non_path_input("Enter Task: ")) - 1
    print("\n")
    task_keys = list(tasks.keys())
    if 0 <= choice < len(task_keys):
        task_function = tasks[task_keys[choice]]
        task_function()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
