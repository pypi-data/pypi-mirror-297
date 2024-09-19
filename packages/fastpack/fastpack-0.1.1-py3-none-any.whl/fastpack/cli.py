import os
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"
PYPROJECT_PATH = TEMPLATE_DIR / "pyproject.toml"


def main():

    with open(PYPROJECT_PATH) as f:
        pyproject = f.read()

    try:
        name_index = sys.argv.index("--name")
        package_name = sys.argv[name_index + 1]
    except ValueError:
        package_name = None

    try:
        description_index = sys.argv.index("--description")
        package_description = sys.argv[description_index + 1]
    except ValueError:
        package_description = None

    if len(sys.argv) == 3 and package_name is None and package_description is None:
        package_name = sys.argv[1]
        package_description = sys.argv[2]

    if package_name is None:
        package_name = input("Enter package name: ")

    if package_description is None:
        package_description = input("Enter package description: ")

    # set the package name
    pyproject = pyproject.replace("PACKAGE_NAME", package_name)

    # Define package directory paths
    package_root_dir = Path(package_name.replace("-", "_"))
    package_modules_dir = package_root_dir / package_name.replace("-", "_")
    package_docs_dir = package_root_dir / "docs"
    package_tests_dir = package_root_dir / "tests"

    # Define package file paths
    package_init = package_modules_dir / "__init__.py"
    pyproject_path = package_root_dir / "pyproject.toml"
    flake8_path = package_root_dir / ".flake8"
    precommit_path = package_root_dir / ".pre-commit-config.yaml"
    readme_path = package_root_dir / "README.md"
    gitignore_path = package_root_dir / ".gitignore"

    # set the package description
    pyproject = pyproject.replace("PACKAGE_DESCRIPTION", package_description)

    # Get the package author
    user = subprocess.check_output(["git", "config", "user.name"]).strip().decode("utf-8")
    if not user:
        user = input("Enter your name: ")
    pyproject = pyproject.replace("AUTHOR_NAME", user)

    # Get the package author email
    email = subprocess.check_output(["git", "config", "user.email"]).strip().decode("utf-8")
    if not email:
        email = input("Enter your email: ")
    pyproject = pyproject.replace("AUTHOR@EMAIL", email)

    # Make package directories
    package_root_dir.mkdir()
    package_modules_dir.mkdir()
    package_docs_dir.mkdir()
    package_tests_dir.mkdir()

    # Make blank init file
    package_init.touch()

    # Write pyproject.toml
    with open(pyproject_path, "w") as f:
        f.write(pyproject)

    # Copy template files
    shutil.copy(TEMPLATE_DIR / ".flake8", flake8_path)
    shutil.copy(TEMPLATE_DIR / ".pre-commit-config.yaml", precommit_path)
    shutil.copy(TEMPLATE_DIR / "README.md", readme_path)
    shutil.copy(TEMPLATE_DIR / ".gitignore", gitignore_path)

    # change to the package root directory
    os.chdir(package_root_dir)

    # Create a virtual environment
    py_cmd = sys.executable
    subprocess.run([py_cmd, "-m", "venv", "venv"], check=True)

    # Install dev dependencies
    subprocess.run(["venv/bin/pip", "install", "-U", "pip", ".[dev]"], check=True)

    # Initialize git
    subprocess.run(["git", "init"], check=True)

    # Initialize pre-commit
    subprocess.run(["venv/bin/pre-commit", "install"], check=True)

    # Make initial commit
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
