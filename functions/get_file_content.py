import os
from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    
    full_path = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_path)
    

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) != "":
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return "Error: " + str(e)

