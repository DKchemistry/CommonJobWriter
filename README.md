# CommonJobWriter

CommonJobWriter is a command-line interface (CLI) tool designed to streamline and automate the execution of common tasks in research. It is built with Python and uses the `prompt_toolkit` library for user interaction.

## Features

CommonJobWriter provides a simple and intuitive interface for executing tasks such as:

- Stereochemical Enumeration (Unenumerated Stereocenter Only)
- Ligprep (SMILES to SDF, no epik, uses ligprep.inp)
- Glide Docking (SDF to SDF, makes glide.in)

The tool allows you to select tasks from a list, and it guides you through the necessary steps to execute each task. It also provides a mechanism for adding new tasks as needed.

## Usage

To use CommonJobWriter, simply run the `main.py` script from your terminal:

```bash
python main.py
```
You will be presented with a list of tasks. Enter the number corresponding to the task you want to execute. 