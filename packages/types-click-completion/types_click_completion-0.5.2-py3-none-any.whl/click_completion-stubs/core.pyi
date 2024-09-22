from enum import Enum
from typing import Callable, Dict, Generator, List, Literal, Optional, Tuple

import click
from click_completion.lib import resolve_ctx as resolve_ctx

shells: Dict[str, str]
completion_configuration: CompletionConfiguration

class Shell(Enum):
    bash: str
    fish: str
    zsh: str
    powershell: str

ShellName = Literal["bash", "fish", "zsh", "powershell"]

def startswith(string: str, incomplete: str) -> bool: ...

class CompletionConfiguration:
    complete_options: bool
    match_complete: Callable[[str, str], bool]

    def __init__(self) -> None: ...

def match(string: str, incomplete: str) -> bool: ...
def get_choices(
    cli: click.Command, prog_name: str, args: List[str], incomplete: str
) -> Generator[Tuple[str, Optional[str]], None, None]: ...
def do_bash_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_fish_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_zsh_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_powershell_complete(cli: click.Command, prog_name: str) -> bool: ...
def get_code(
    shell: Optional[str] = None,
    prog_name: Optional[str] = None,
    env_name: Optional[str] = None,
    extra_env: Optional[Dict[str, str]] = None,
) -> str: ...
def install(
    shell: Optional[str] = None,
    prog_name: Optional[str] = None,
    env_name: Optional[str] = None,
    path: Optional[str] = None,
    append: Optional[bool] = None,
    extra_env: Optional[Dict[str, str]] = None,
) -> Tuple[ShellName, str]: ...
