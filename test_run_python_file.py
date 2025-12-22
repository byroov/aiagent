from functions.run_python_file import run_python_file 


#Run calculator main.py without arguments (should print usage instructions)
print("Test 1:")
print(run_python_file("calculator", "main.py"))
print("-" * 50)

#Run calculator main.py with an argument (should calculate "3 + 5")
print("Test 2:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("-" * 50)

#Run calculator tests.py (should run tests successfully)
print("Test 3:")
print(run_python_file("calculator", "tests.py"))
print("-" * 50)

#ry to run a file outside the working directory (should return an error)
print("Test 4:")
print(run_python_file("calculator", "../main.py"))
print("-" * 50)

#Try to run a non-existent file (should return an error)
print("Test 5:")
print(run_python_file("calculator", "nonexistent.py"))
print("-" * 50)

#Try to run a non-Python file (should return an error)
print("Test 6:")
print(run_python_file("calculator", "lorem.txt"))
print("-" * 50)
