import glob
import os
import subprocess


# Function to list all .py files excluding the script itself
def list_py_files(script_name):
    py_files = glob.glob("./tests/*.py")
    print(py_files)
    py_files.remove(script_name)
    return py_files


if __name__ == "__main__":
    self_name = "./tests/" + os.path.basename(__file__)
    py_files = list_py_files(self_name)
    for file in py_files:
        print(f"Running {file}...")
        subprocess.run(["python3", file], check=True)
