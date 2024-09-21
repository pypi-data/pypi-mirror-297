# Description

## Documentation

[docs.dharitri.com](https://docs.dharitri.com/sdk-and-tools/sdk-py/)

## CLI

[CLI](CLI.md)

## Distribution

[drtpy-up](https://docs.dharitri.com/sdk-and-tools/sdk-py/installing-drtpy/) and [PyPi](https://pypi.org/project/drt-sdk-cli/#history)

## Development setup

Clone this repository and cd into it:

```
git clone https://github.com/DharitriOne/drt-sdk-py-cli.git
cd drt-sdk-py-cli
```

### Virtual environment

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt --upgrade
```

Install development dependencies, as well:

```
pip install -r ./requirements-dev.txt --upgrade
```

Above, `requirements.txt` should mirror the **dependencies** section of `setup.py`.

If using VSCode, restart it or follow these steps:

- `Ctrl + Shift + P`
- _Select Interpreter_
- Choose `./venv/bin/python`.

### Using your local `drtpy`

If you want to test the modifications you locally made to `drtpy`, set `PYTHONPATH` with the path to your local repository path.

For example, if you cloned the repository at `~/drt-sdk-py-cli`, run:

```
export PYTHONPATH="~/drt-sdk-py-cli"
```

Then `drtpy` will use the code in your local repository.
