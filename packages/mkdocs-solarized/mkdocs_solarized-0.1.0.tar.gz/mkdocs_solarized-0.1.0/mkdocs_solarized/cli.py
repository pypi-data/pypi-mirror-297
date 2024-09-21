
import argparse
import shutil
from pathlib import Path

try:
    # if Python >= 3.7
    from importlib.resources import path as resource_path
except ImportError:
    # backported library for older Python versions
    from importlib_resources import path as resource_path



def gen_mkdocs_yml(force=False):
    
    current_dir = Path.cwd()
    # Path class has overloaded __truediv__ (/)
    mkdocs_yml = current_dir / "mkdocs.yml"
    
    if mkdocs_yml.exists() and not force:
        print(f"mkdocs.yml already exists in current directory: {current_dir}")
        print("Use --force to overwrite it.")
        return False
    else:
        with resource_path("mkdocs_solarized.templates", "mkdocs.yml") as template_path:
            # src: $(template_path) -> dest: $(mkdocs_yml)
            shutil.copyfile(template_path, mkdocs_yml)
            print('mkdocs.yml has been created in the current directory:')
            print(mkdocs_yml)
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize mkdocs.yml for solarized theme"
    )
    parser.add_argument(
        "--force", help="Overwrite current mkdocs.yml if it exists"
    )
    args = parser.parse_args()
    gen_mkdocs_yml(force=args.force)