import os
import subprocess

from google.genai import types



def run_python_file(working_directory, file_path, args=None):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common = os.path.commonpath([abs_working_dir, abs_file_path])



    
    if common != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", abs_file_path]
    if args:
        command.extend(args)


    import subprocess
    try:
        result = subprocess.run(
            command,
            cwd=working_directory,      # set the working directory
            capture_output=True,        # captures stdout and stderr
            text=True,                  # decode output as strings
            timeout=30                  # prevent infinite execution
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if not stdout and not stderr:
            output_parts.append("No output produced")
        else:
            if stdout:
                output_parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                output_parts.append(f"STDERR:\n{stderr}")

        output = "\n".join(output_parts)
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
    



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory and returns its output, with security checks to prevent unauthorized access",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of string arguments to pass to the Python file when executing",
            ),
        },
    ),
)