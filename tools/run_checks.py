import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n--- {description} ---")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error Output:\n{result.stderr}")
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    print(f"--- {description} Succeeded ---")
    return True

def main():
    # Determine the path to the virtual environment's python executable
    venv_python = os.path.join(".venv", "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(".venv", "bin", "python")
    
    # Ensure the virtual environment is activated for subsequent commands
    # This is more robust than relying on shell activation scripts
    # We'll prepend the venv_python to the commands directly

    print("Running code quality checks...")
    all_passed = True

    # Run black (check only)
    if not run_command(f"{venv_python} -m black --check src/", "Running Black (code formatter check)"):
        all_passed = False

    # Run flake8
    if not run_command(f"{venv_python} -m flake8 src/", "Running Flake8 (linter)"):
        all_passed = False

    # Run mypy
    if not run_command(f"{venv_python} -m mypy src/", "Running Mypy (static type checker)"):
        all_passed = False

    if all_passed:
        print("\nAll code quality checks passed successfully!")
        sys.exit(0)
    else:
        print("\nSome code quality checks failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    # Change to the pynntt.sub directory
    script_dir = os.path.dirname(__file__)
    pynntt_sub_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    os.chdir(pynntt_sub_dir)
    
    main()
