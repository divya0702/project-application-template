<<<<<<< HEAD
# Poetry: Python packaging and dependency management made easy

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Stable Version](https://img.shields.io/pypi/v/poetry?label=stable)][PyPI Releases]
[![Pre-release Version](https://img.shields.io/github/v/release/python-poetry/poetry?label=pre-release&include_prereleases&sort=semver)][PyPI Releases]
[![Python Versions](https://img.shields.io/pypi/pyversions/poetry)][PyPI]
[![Download Stats](https://img.shields.io/pypi/dm/poetry)](https://pypistats.org/packages/poetry)
[![Discord](https://img.shields.io/discord/487711540787675139?logo=discord)][Discord]

Poetry helps you declare, manage and install dependencies of Python projects,
ensuring you have the right stack everywhere.

![Poetry Install](https://raw.githubusercontent.com/python-poetry/poetry/main/assets/install.gif)

Poetry replaces `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in` and `Pipfile` with a simple `pyproject.toml`
based project format.

```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = "The description of the package"

license = "MIT"

authors = [
    "Sébastien Eustace <sebastien@eustace.io>"
]

repository = "https://github.com/python-poetry/poetry"
homepage = "https://python-poetry.org"

# README file(s) are used as the package description
readme = ["README.md", "LICENSE"]

# Keywords (translated to tags on the package index)
keywords = ["packaging", "poetry"]

[tool.poetry.dependencies]
# Compatible Python versions
python = ">=3.8"
# Standard dependency with semver constraints
aiohttp = "^3.8.1"
# Dependency with extras
requests = { version = "^2.28", extras = ["security"] }
# Version-specific dependencies with prereleases allowed
tomli = { version = "^2.0.1", python = "<3.11", allow-prereleases = true }
# Git dependencies
cleo = { git = "https://github.com/python-poetry/cleo.git", branch = "main" }
# Optional dependencies (installed by extras)
pendulum = { version = "^2.1.2", optional = true }

# Dependency groups are supported for organizing your dependencies
[tool.poetry.group.dev.dependencies]
pytest = "^7.1.2"
pytest-cov = "^3.0"

# ...and can be installed only when explicitly requested
[tool.poetry.group.docs]
optional = true
[tool.poetry.group.docs.dependencies]
Sphinx = "^5.1.1"

# Python-style entrypoints and scripts are easily expressed
[tool.poetry.scripts]
my-script = "my_package:main"
```

## Installation

Poetry supports multiple installation methods, including a simple script found at [install.python-poetry.org]. For full
installation instructions, including advanced usage of the script, alternate install methods, and CI best practices, see
the full [installation documentation].

## Documentation

[Documentation] for the current version of Poetry (as well as the development branch and recently out of support
versions) is available from the [official website].

## Contribute

Poetry is a large, complex project always in need of contributors. For those new to the project, a list of
[suggested issues] to work on in Poetry and poetry-core is available. The full [contributing documentation] also
provides helpful guidance.

## Resources

* [Releases][PyPI Releases]
* [Official Website]
* [Documentation]
* [Issue Tracker]
* [Discord]

  [PyPI]: https://pypi.org/project/poetry/
  [PyPI Releases]: https://pypi.org/project/poetry/#history
  [Official Website]: https://python-poetry.org
  [Documentation]: https://python-poetry.org/docs/
  [Issue Tracker]: https://github.com/python-poetry/poetry/issues
  [Suggested Issues]: https://github.com/python-poetry/poetry/contribute
  [Contributing Documentation]: https://python-poetry.org/docs/contributing
  [Discord]: https://discord.com/invite/awxPgve
  [install.python-poetry.org]: https://install.python-poetry.org
  [Installation Documentation]: https://python-poetry.org/docs/#installation

## Related Projects

* [poetry-core](https://github.com/python-poetry/poetry-core): PEP 517 build-system for Poetry projects, and
dependency-free core functionality of the Poetry frontend
* [poetry-plugin-export](https://github.com/python-poetry/poetry-plugin-export): Export Poetry projects/lock files to
foreign formats like requirements.txt
* [poetry-plugin-bundle](https://github.com/python-poetry/poetry-plugin-bundle): Install Poetry projects/lock files to
external formats like virtual environments
* [install.python-poetry.org](https://github.com/python-poetry/install.python-poetry.org): The official Poetry
installation script
* [website](https://github.com/python-poetry/website): The official Poetry website and blog

## Supporters

Thanks to [JetBrains](https://www.jetbrains.com) for supporting us with licenses for their tools.

[<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jetbrains.svg" width="150" alt="JetBrains logo." />](https://www.jetbrains.com)
=======
# ENPM611 Project Application Template

This is the template for the ENPM611 class project. Use this template in conjunction with the provided data to implement an application that analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates interesting insights.

This application template implements some of the basic functions:

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration paramters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate intersting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.

## Setup

To get started, your team should create a fork of this repository. Then, every team member should clone your repository to their local computer. 


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```

That will output basic information about the issues to the command line.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.
>>>>>>> 46982520916936dc0d42fbbe0bc8d3249ba9b86a
