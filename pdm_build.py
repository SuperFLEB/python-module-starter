import shutil
import pathlib

shutil.rmtree("src/fleb/starter/assets/copy")
shutil.copytree("buildscript", "src/fleb/starter/assets/copy/buildscript")
shutil.copytree(".github", "src/fleb/starter/assets/copy/.github")

for path in pathlib.Path("src/fleb/starter/assets/copy").rglob("*/**/__pycache__"):
    shutil.rmtree(path)
