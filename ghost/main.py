from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import argparse

console = Console()
ROOT = Path(__file__).parent.resolve()

VCS_PACKAGES = [
    "badges @ git+https://github.com/EntySec/Badges",
    "pex @ git+https://github.com/EntySec/Pex",
    "colorscript @ git+https://github.com/EntySec/ColorScript",
    "adb-shell"
]

DEFAULT_VENV = ROOT / ".venv"

def run(cmd: List[str], env: dict | None = None, check: bool = True) -> None:
    console.log(f"[bold purple]$[/bold purple] {' '.join(cmd)}")
    res = subprocess.run(cmd, env=env)
    if check and res.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(cmd)} (exit {res.returncode})")

def ensure_virtualenv(venv_path: Path) -> Tuple[str, str]:
    if venv_path.exists():
        console.print(Panel(f"Using existing virtualenv: [bold]{venv_path}[/bold]", title="Virtualenv"))
    else:
        console.print(Panel(f"Creating virtualenv at: [bold]{venv_path}[/bold]", title="Virtualenv"))
        run([sys.executable, "-m", "venv", str(venv_path)])
    if os.name == "nt":
        py = venv_path / "Scripts" / "python.exe"
        pip = venv_path / "Scripts" / "pip.exe"
    else:
        py = venv_path / "bin" / "python"
        pip = venv_path / "bin" / "pip"
    return str(py), str(pip)

def install_packages(py_exe: str, packages: List[str], break_system: bool = False) -> None:
    if not packages:
        return
    cmd = [py_exe, "-m", "pip", "install"] + packages
    if break_system:
        cmd.append("--break-system-packages")
    run(cmd)

def install_local_package(py_exe: str, break_system: bool = False) -> None:
    cmd = [py_exe, "-m", "pip", "install", ".", "--no-deps"]
    if break_system:
        cmd.append("--break-system-packages")
    run(cmd)

def main() -> None:
    parser = argparse.ArgumentParser(description="Ghost installer (venv or system)")
    parser.add_argument("--no-venv", action="store_true", help="Do not create/use virtualenv; install in current interpreter")
    parser.add_argument("--venv", default=".venv", help="Virtualenv path (default: .venv)")
    parser.add_argument("--brek", action="store_true", help="Install only python packages (skip VCS URLs).")
    parser.add_argument("--yes", "-y", action="store_true", help="Automatic yes for prompts")
    args = parser.parse_args()

    console.print(Panel(Text("Ghost Installer — staged installation\n\nIndex 99 → Return to Menu / Exit", justify="center"), style="purple"))

    use_brek = args.brek
    use_venv = not args.no_venv

    # انتخاب خودکار در حالت بدون prompt
    if not args.yes:
        if not (args.brek or args.no_venv):
            choice = Prompt.ask(
                "Choose install mode",
                choices=["venv", "brek", "system"],
                default="venv",
                show_choices=True,
            )
            if choice == "venv":
                use_venv = True
                use_brek = False
            elif choice == "brek":
                use_venv = False
                use_brek = True
            else:
                use_venv = False
                use_brek = False
    else:
        if use_brek:
            use_venv = False

    break_system_flag = not use_venv
    if break_system_flag:
        console.print(Panel("Installing into current Python interpreter. --break-system-packages enabled", title="Notice", style="yellow"))

    if use_venv:
        py_exe, _ = ensure_virtualenv(Path(args.venv))
    else:
        py_exe = sys.executable

    console.print("[bold]Upgrading pip in target environment...[/bold]")
    cmd_upgrade = [py_exe, "-m", "pip", "install", "--upgrade", "pip"]
    if break_system_flag:
        cmd_upgrade.append("--break-system-packages")
    run(cmd_upgrade)

    if not use_brek:
        console.print(Panel(f"Installing VCS/GitHub packages ({len(VCS_PACKAGES)} items)...", title="Dependencies"))
        install_packages(py_exe, VCS_PACKAGES, break_system_flag)

    console.print(Panel("Installing Ghost main package...", style="purple"))
    install_local_package(py_exe, break_system_flag)

    console.print(Panel("[bold green]Installation completed successfully![/bold green]"))
    console.print("You can now run: ghost")
