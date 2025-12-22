import os
from config import MAX_CHARS


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