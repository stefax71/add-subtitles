# Add subtitles

## Description

This is an example that I made **for my own needs**, hence it has some hardcoded things, such as the Vosk model to be used, which is the italian one.

If you want to customize the vosk model, you can do it by changing the `vosk_model` variable in the `add_subtitles.py` file.


## Installation

Update dependencies with

```python
pip install -r .\requirements.txt
```

Set the PYTHONPATH environment variable:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/src
```

or, on Windows:

```bash
set PYTHONPATH=%PYTHONPATH%;C:\path\to\src
```

If you are using a venv in powershell, you can use the following command to set the PYTHONPATH:

```bash
$env:PYTHONPATH = "$env:PYTHONPATH;C:\path\to\src"
```