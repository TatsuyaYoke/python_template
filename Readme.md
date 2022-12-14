### Tools

1. Python3.8
2. VScode
3. Git, Git bash

Reference is below
https://zenn.dev/jdbtisk/articles/e6ed54b38b6a45

### Python Library

1. poetry (virtual environment)
2. flake8 (linter)
3. mypy (linter)
4. black (formatter)
5. isort (formatter)
6. taskipy (task runner)
7. sphinx (documentation)
8. pytest (test, optional)
9. pyinstaller (build exe file)
10. pre-commit (check before commit)

### Python

#### Preparation

1. Install Python 3.8 into global
2. Go to VScode Preparation
3. pip install poetry (use PowerShell on administrator mode)
4. Make project directory
5. Open VScode and choose the above project directory
6. Copy and paste template into the above project directory (you can skip No.7, 8, 10 and 12 to 14 if you use the template)
7. Make src directory and main.py and \_\_init\_\_.py in src directory
8. Make common and engine directory in src and \_\_init\_\_.py in common and engine directory for original modules
9. Open Git bash terminal in VScode
10. Go to Git Preparation
11. Make virtual environment by poetry

```bash
poetry init # pyproject.toml output, you can skip if you have pyproject.toml
poetry install # poetry.lock output and make virtual environment as .venv
```

##### Make virtualenv in same directory as project

```bash
poetry config --list
poetry config virtualenvs.in-project true
```

##### Delete virtualenv

```bash
poetry env list
# poetry-xx-py3.6
poetry env remove poetry-xx-py3.6
```

12. Install development library

```bash
poetry add -D flake8
poetry add -D mypy
poetry add -D black
poetry add -D isort
poetry add -D taskipy
poetry add -D Sphinx sphinx-rtd-theme sphinx-pyproject
poetry add -D pyinstaller
poetry add -D lxml # for mypyreport output
```

13. Install flake8 plugin

```bash
poetry add -D pyproject-flake8
poetry add -D flake8-isort
poetry add -D flake8-bugbear
poetry add -D flake8-builtins
poetry add -D flake8-eradicate
poetry add -D flake8-unused-arguments
poetry add -D pep8-naming
```

14. Go to Setting

### Setting

#### taskipy

1. pyproject.toml setting

```
[tool.taskipy.tasks]
dev = "python src/main.py"
fmt-lint = "task fmt && task lint"
fmt-lint-strictest = "task fmt && task lint-strictest"
fmt = "task fmt-black && task fmt-isort"
fmt-black = "black src"
fmt-isort = "isort src"
lint = "task lint-black && task lint-flake8 && task lint-mypy"
lint-strictest = "task lint-black && task lint-flake8 && task lint-mypy-strictest"
lint-flake8 = "pflake8 src"
lint-mypy = "mypy --strict src"
lint-mypy-report = "mypy --strict src --html-report mypyreport --any-exprs-report mypyreport"
lint-mypy-strictest = "mypy --strict src --disallow-any-expr"
lint-mypy-strictest-report = "mypy --strict src --disallow-any-expr --html-report mypyreport --any-exprs-report mypyreport"
lint-black = "black --check src"
docs = "task clean-docs && sphinx-apidoc -F -o docs/source src && sphinx-build docs/source docs/build"
clean-docs = "rm -rf docs/build && cd docs/source && rm -rf *.rst make.bat Makefile _build _static _templates && cd ../.."
build = "pyinstaller src/main.py --onefile"
test = "pytest -s -vv --cov=. --cov-branch --cov-report=html"
```

2. Command

```bash
poetry run task dev # execute src/main.py
poetry run task fmt # format
poetry run task lint # linter
```

#### flake8

1. install pyproject-flake8 to use pyproject.toml as a setting file

```bash
poetry add -D pyproject-flake8
```

2. pyproject.toml setting

```bash
[tool.flake8]
max-line-length = 160
extend-ignore = "E203, W503" # to avoid black conflict
```

3. setup.cfg setting for pre-commit (optional)

```bash
[flake8]
ignore = E203,W503
max-line-length = 160
```

4. Command

```bash
poetry run pflake8 src # not use flake8 src to use pyproject setting
poetry run task lint-flake8 # can use task command if you set taskipy
```

#### black

1. pyproject.toml setting

```bash
[tool.black]
line-length = 160
```

2. Command

```bash
poetry run black src
poetry run black --check src # not format, only check
poetry run task fmt-black # can use task command if you set taskipy
```

#### isort

1. pyproject.toml setting

```bash
[tool.isort]
profile = "black" # to avoid to black conflict
```

2. Command

```bash
poetry run isort src
poetry run task fmt-isort # can use task command if you set taskipy
```

#### mypy

1. pyproject.toml setting

```bash
[tool.mypy]
ignore_missing_imports = true
```

2. Command

```bash
mypy --strict src
poetry run task lint-mypy # can use task command if you set taskipy
```

#### sphinx

1. pyproject.toml setting

```bash
[project]
name = "python-template"
version = "0.1.0"
description = "Template for python project"
readme = "README.md"

[[project.authors]]
name = "Yoke"

[tool.sphinx-pyproject]
project = "python-template"
copyright = "2022, Yoke"
language = "en"
package_root = "python-template"
html_theme = "sphinx_rtd_theme"
todo_include_todos = true
templates_path = ["_templates"]
html_static_path = ["_static"]
extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.viewcode",
  "sphinx.ext.todo",
  "sphinx.ext.napoleon",
]
```

2. Configuration setting
   Make docs/source/conf.py

```python
import os
import sys

from sphinx_pyproject import SphinxConfig

sys.path.append(
    os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

config = SphinxConfig("../../pyproject.toml", globalns=globals())

```

3. Command

```bash
poetry run sphinx-apidoc -F -o docs/source src
poetry run sphinx-build docs/source docs/build
poetry run task docs  # can use task command if you set taskipy
```

##### Docstring

1. Parameters (Required)
2. Returns (Required)
3. Examples (Recommended)
4. Errors (Optional)
5. Notes (Optional)

If you install autoDocstring of VScode extension, you can use shortcut key (Ctrl + Shift + 2) to output template.

Refer to below
https://qiita.com/simonritchie/items/49e0813508cad4876b5a

### Optional setting

#### pyinstaller

- Command

```bash
poetry run pyinstaller src/main.py --onefile
poetry run pyinstaller src/main.py --onefile --noconsole # if no standard output
poetry run task build
```

#### pytest

1. Make directory tests and conftest.py in tests directory as below

```python
import os
import sys

sys.path.append(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/../src/"))

```

2. Install library

```bash
poetry add -D pytest pytest-mock pytest-cov
```

3. Make test file (file name prefix needs to be test\_)

4. Command

```bash
poetry run pytest -s -vv --cov=. --cov-branch --cov-report=html
poetry run task test # can use task command if you set taskipy
```

5. Set taskipy command

```bash
[tool.taskipy.tasks]
test = "pytest -s -vv --cov=. --cov-branch --cov-report=html"
```

6. Test report

- Can see test results on terminal
- Coverage results is in htmlcov directory

#### pre-commit

1. Make .pre-commit-config.yaml as below

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.2.0
    hooks:
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]
      - id: end-of-file-fixer
      - id: mixed-line-ending
        args: [--fix=lf]
      - id: check-added-large-files
      - id: check-toml
      - id: check-yaml
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.942
    hooks:
      - id: mypy
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://gitlab.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        additional_dependencies:
          - flake8-isort
          - flake8-bugbear
          - flake8-builtins
          - flake8-eradicate
          - flake8-pytest-style
          - flake8-unused-arguments
          - pep8-naming
```

2. Install Library and settings

```bash
poetry add -D pre-commit
poetry run pre-commit install
```

### VScode

#### Preparation

1. Install VScode
2. Install Git and bash
3. Set Git bash as a default terminal
4. Install extension

#### Extension

- Python
- Pylance
- Code Spell Checker

### Git

#### Preparation

1. git init on terminal
2. Make .gitignore file
3. Copy and paste the below Python.gitignore template into .gitignore
   https://github.com/github/gitignore/blob/main/Python.gitignore
4. Copy and paste User setting as below into .gitignore

```bash
# User
mypyreport/
```

#### Setting

1. Make .vscode directory and settings.json in .vscode
2. Copy and paste below

```json
{
  "editor.formatOnSave": true,
  "python.analysis.extraPaths": ["./src"],
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "${workspaceFolder}/.venv/Scripts/black.exe",
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Path": "${workspaceFolder}/.venv/Scripts/pflake8.exe",
  "python.linting.mypyEnabled": true,
  "python.linting.mypyPath": "${workspaceFolder}/.venv/Scripts/mypy.exe",
  "python.linting.mypyArgs": ["--strict", "--ignore-missing-imports"],
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "autoDocstring.docstringFormat": "numpy",
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "strict",
  "cSpell.words": [
    "Yoke
  ]
}
```

#### Recommended Extensions

Recommended extensions are as below and this file is put in .vscode directory.

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "njpwerner.autodocstring",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### Neo Vim

https://wonwon-eater.com/vscode-nvim/

1. Chocolately install

- Use PowerShell Administrator mode and install
  Do you want to run the script -> All Yes

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

Check to complete installing successfully

```bash
choco list -l
# Chocolatey v0.10.15
# chocolatey 0.10.15
# 1 packages installed.
```

2. Neo Vim install

- Use PowerShell Administrator mode and install

```bash
choco install neovim --pre
```

- Check to complete installing successfully

```bash
nvim
```

- Check path of nvim app

```bash
gcm nvim
```

4. VSCode Neovim extension

- VSCode Neovim install
- Open settings (Ctrl + ,)
- Search Neovim Executable Paths: Win32
- Copy and paste nvim path
- VScode restart
