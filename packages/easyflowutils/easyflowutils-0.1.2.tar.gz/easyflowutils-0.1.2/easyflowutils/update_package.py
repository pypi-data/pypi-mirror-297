import re
import subprocess
import sys
from pathlib import Path


def update_version(version_type='patch'):
    setup_file = Path('../setup.py')
    setup_content = setup_file.read_text()

    version_match = re.search(r'version="(\d+)\.(\d+)\.(\d+)"', setup_content)
    if not version_match:
        raise ValueError("Couldn't find version string in setup.py")

    major, minor, patch = map(int, version_match.groups())

    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f'{major}.{minor}.{patch}'

    new_setup_content = re.sub(
        r'version="[\d\.]+"',
        f'version="{new_version}"',
        setup_content
    )
    setup_file.write_text(new_setup_content)

    print(f"Updated version to {new_version}")
    return new_version


def build_and_upload():
    subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
    subprocess.run(["twine", "upload", "dist/*"], check=True)


def main(version_type):
    new_version = update_version(version_type)

    build_and_upload()

    print(f"Successfully updated and uploaded version {new_version}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        version_type = sys.argv[1].lower()
    else:
        version_type = input("Enter version type to bump (major/minor/patch): ").lower()

    if version_type not in ['major', 'minor', 'patch']:
        version_type = 'patch'

    main(version_type)
