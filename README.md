# Python+GitHub Actions Installable Module Starter
https://github.com/SuperFLEB/python-installable-starter | https://superfleb.github.io/python-installable-starter/

This is a template for Python module projects that includes GitHub Actions for publishing the module to a private
static repository on GitHub Pages, allowing for easy installation via pip.

MIT-0 licensed. Do whatever you want, just don't blame me if it all ends in tears.

## What this gives you

- Structure. Stability. Some grounding in life. A safe place to take off from and explore your Python-module dreams.
- GitHub actions that build a Python Wheel package, make a release, and publish a GitHub Pages site that
  allows using `pip install` to install your package from the command line.

## How you use it
- Clone this repo as the starting point for your own project. (Be sure to wipe the .git directory.)
- Do your thing.
- When you've got a version, tag it with a v-prefixed Semver version number.
  ```shell
  git tag v0.1.0
  ```
- Before you run the actions, be sure GitHub Pages is enabled on the repo and set to "GitHub Actions".
- When you've got a releasable version you're happy with, there are two GitHub Actions that will help you:
  1. The `Release` action will build a wheel package, create a Release, and publish all existing releases to the repo's
     GitHub Pages site.
  2. The `Generate pip repository` action will regenerate the GitHub Pages site with all existing releases.

Both actions are manually triggered at the moment. I'll probably get around to adding actual triggers, but not yet.

If you run the Release action without a tag on the latest commit, it will increment the patch version
(e.g. 1.0.1 -> 1.0.2) and publish that as a release. You should probably tag it though.

If you run the Release action on a tagged version that you've force-pushed changes to and already Released once,
it might fail. Known issue, low priority until it bugs me enough to change.

## Things you'll need to customize

- Change the directory name in `src` to your own namespace and package name.
- Update the `pyproject.toml` file with your own information, including the namespaced package name
  to match the directory.
- Swap out this README for your own.
- Swap out the LICENSE file for your own. (This is MIT-0 licensed, so you don't have to worry about my attribution.)
- Write code.

## Things you _might_ need to customize but probably don't

- The Python version in .github/workflows/release.yaml. This might be fine, since it's just for the packager, but if
  you run into problems and you're making something for a newer version of Python, give it a look.
- If GitHub Actions doesn't show any Actions, you might need to make a minor edit to the two .yaml files in the
  `.github/workflows` directory -- just add a newline at the end or something-- to wake GitHub Actions up.

## Inevitable Disclaimer

This was spun off from my first installable Python module. I'm putting this together as I go, so I might not be doing
things exactly right, or Pythonically, or up to best practices. That said... it works on my box! Issues are welcome
if you know more about Python packaging than I do and find I did something wrong or awkwardly.

