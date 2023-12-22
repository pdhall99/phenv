# phenv

Notes on a `virtualenv`/`jupyterlab` setup for data science development in Python.

## Instructions

### Install multiple versions of Python
1. Install the Python versions you need, e.g., by using `brew` or the Python.org installers
1. Make aliases for each version, `python3.8` for Python 3.8, `python3.9` for Python 3.9, etc.
1. In each base environment, install `virtualenv` and this repo by running `pip install -e .`
1. Add a pip config file to your home directory, `pip.conf` to avoid accidentally installing any other packages in your base Python environments:
```ini
[global]
require-virtualenv = true
```

### Make a single "system" Jupyter environment
1. Make the system Jupyter environment by running `python3.11 -m virtualenv ~/envs/jupyter_env`
1. Install JupyterLab and any extensions by running `python -m pip install jupyterlab`
1. Add a Jupyter config file to stop the native kernel being shown in JupyterLab by running `jupyter server --generate-config` and manually editing the file (at `$JUPYTER_ENV/etc/jupyter`) to set
```python
c.KernelSpecManager.ensure_native_kernel = False
```
1. Manually edit the `activate` script at `~/envs/jupyter_env/bin/activate` to set and unset a `JUPYTER_CONFIG_DIR` environment variable on activation and deactivation, respectively, that points to the config file:
```bash
...
# Deactivate block
unset JUPYTER_CONFIG_DIR
...
# End of file
export JUPYTER_CONFIG_DIR=$VIRTUAL_ENV/etc/jupyter
```
1. Uninstall the default kernel by running `jupyter kernelspec remove python3`
1. Add a pip config file, `pip.conf` in `jupyter_env` to stop accidental pip installation into the Jupyter environment itself:
```ini
[global]
no-cache-dir = true
no-index = true
```
1. Declare an environment variable `JUPYTER_ENV`, the path to `jupyter_env`, in your `.bash_profile`:
```bash
export JUPYTER_ENV=/path/to/jupyter_env
```

### Make a virtual environment
Make a virtual environment using `python3.x` by running
```bash
python3.x -m phenv make /path/to/environment
```
which will make the environment, install `ipykernel` and make the kernel available in the system JupyterLab, but not any other instance on your machine.

## Start JupyterLab
Start JupyterLab by running
```bash
source ~/envs/jupyter_env/bin/activate
python -m jupyter lab &
```

Install packages into particular environments in a notebook using `%pip install ...`.

### Remove missing kernels
Remove any kernels for which the virtual environment no longer exists by running
```bash
python3.x -m phenv clean
```

## Rationale
Pros:
- Only need to install JupyterLab and extensions once.
- Can still install JupyterLab in a specific virtual environment and not see other kernels in that instance.
- Keeps the base Python and Jupyter environments separate and difficult to accidentally pollute with extra packages.
- Virtual environments can be anywhere. Specifically they can be kept close to where they are used.

Cons:
- Need to install `ipykernel` in every virtual environment, which brings in a lot of transitive dependencies.
- Need custom code (this repo) to make this setup practical.
- There may be a package somewhere that already does this at the expense of extra bloat.
- Duplicate kernel names are not dealt with.
