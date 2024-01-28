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

## Future Plans

I have several enhancements planned for CommonJobWriter to make it more versatile and user-friendly. Here are some of the key features I am planning to implement:

1. **Portability**: I aim to make the tool portable to other servers. This will allow users to use CommonJobWriter on any server they have access to, increasing its utility and flexibility.

2. **Directory Independence**: I plan to test and ensure the ability to run the tool from different directories. This will make it easier for users to integrate CommonJobWriter into their existing workflows.

3. **Input Presentation**: I will be working on cleaning up the presentation of input commands to make the tool more intuitive and user-friendly.

4. **Additional Tasks**: I plan to add more common tasks to the tool. Some of the tasks I am considering include:
   - Running a Glide job with a premade `.in` file
   - Integrating other scripts that handle file transfer to local machines
   - Adding future Deep Docking related tasks
