import pathlib
from .Config import Config
from .inquisition import inquisition
from .pyproject_toml import can_generate as can_generate_toml, generate as generate_toml
from .env_my_info import generate as generate_env, generate_contents
from .src import scaffold
from .files import generate as generate_files
from .tree import tree


def interactive_init():
    if not can_generate_toml():
        print("Cannot write pyproject.toml. The file may exist or this location may not be writable.")
        exit(1)

    config: Config = inquisition()

    print("\nWell, that was a lot. One last question:")
    if input("Would you like to generate an environment file to save some of these answers for later? [y/N]: ").lower().startswith("y"):
        try:
            generate_env(config)
            print("I have created a file called .env.my_info in the current directory.")
            print("Rename it to .env and place it above your projects directories to re-use common answers\n"
                  "to these prompts in the future.")
        except:
            print("Too bad. It didn't work. Here's what I would have made:")
            print("-" * 80)
            generate_contents(config)
            print("-" * 80)
            print("I'll still try the rest, though... Onward!")

    print("\nNow on to scaffolding out your project...\n")

    try:
        generate_toml(config)
    except Exception as e:
        print(f"Failed to generate pyproject.toml: {e}")
        print("Bummer. Looks like I can't really help you. Clear that up and come back.")
        exit(1)

    print("Made the pyproject.toml file...")

    scaffold(config)
    print("Scaffolded the src directory...")

    generate_files(config)
    print("Generated the file structure...")

    print(tree())

    print("Done!")


