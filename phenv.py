import json
import os
import subprocess
import sys
from pathlib import Path

import typer

JUPYTER_ENV = os.environ["JUPYTER_ENV"]

app = typer.Typer()


@app.command()
def make(dest: str) -> None:
    """Make a virtual environment."""
    venv_name = Path(dest).absolute().name
    venv_python = str(Path(dest) / "bin" / "python")
    # Create
    subprocess.run([sys.executable, "-m", "virtualenv", dest])
    # Upgrade
    subprocess.run(
        [
            venv_python,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "ipykernel",
            "pip",
            "setuptools",
            "wheel",
        ]
    )
    # Do something if kernel already exists
    kernels = list_kernels()
    if venv_name in kernels["kernelspecs"]:
        venv_name = venv_name + "_new"
    # Install kernel
    subprocess.run(
        [
            venv_python,
            "-m",
            "ipykernel",
            "install",
            "--prefix",
            JUPYTER_ENV,
            "--name",
            venv_name,
            "--display-name",
            venv_name,
        ]
    )


@app.command()
def clean() -> None:
    """Remove kernels that no longer exist."""
    kernels = list_kernels()

    kernels_to_remove = []
    for kernel_name, kernelspec in kernels["kernelspecs"].items():
        argv0 = kernelspec["spec"]["argv"][0]
        if not argv0.startswith("python") and not Path(argv0).exists():
            kernels_to_remove.append(kernel_name)

    if kernels_to_remove:
        print(f"Removing {', '.join(kernels_to_remove)}")
        subprocess.run(
            [
                str((Path(JUPYTER_ENV) / "bin" / "python")),
                "-m",
                "jupyter",
                "kernelspec",
                "remove",
                "-y",
            ]
            + kernels_to_remove
        )
    else:
        print("No kernels to remove")


def list_kernels() -> dict:
    """List kernels in the Jupyter environment."""
    out = subprocess.run(
        [
            str((Path(JUPYTER_ENV) / "bin" / "python")),
            "-m",
            "jupyter",
            "kernelspec",
            "list",
            "--json",
        ],
        capture_output=True,
        text=True,
        env={"PYDEVD_DISABLE_FILE_VALIDATION": "1"},
    )
    return json.loads(out.stdout)


if __name__ == "__main__":
    app()
