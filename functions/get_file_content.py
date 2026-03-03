import os
from wsgiref import types
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        # Ensure target is inside working directory
        if os.path.commonpath([abs_working, abs_target]) != abs_working:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it’s a regular file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS and detect truncation
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            extra_char = f.read(1)
            if extra_char:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a maximum character limit and security checks to prevent unauthorized access",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required =["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),

)





schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

