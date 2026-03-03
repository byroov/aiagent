from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


working_directory = "./calculator"


function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        # Special case: functions that require working_directory as first arg
        if function_name in ["get_files_info", "get_file_content", "run_python_file", "write_file"]:
            result = function_map[function_name](working_directory, **args)
        else:
            result = function_map[function_name](**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"content": result} if not isinstance(result, dict) else result,
                )
            ],
        )

    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )