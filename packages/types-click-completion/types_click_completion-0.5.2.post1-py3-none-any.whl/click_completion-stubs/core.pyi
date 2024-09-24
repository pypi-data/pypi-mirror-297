from enum import Enum
from typing import Callable, Generator, Literal

import click
from click_completion.lib import resolve_ctx as resolve_ctx

shells: dict[str, str]
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
    cli: click.Command, prog_name: str, args: list[str], incomplete: str
) -> Generator[tuple[str, str | None], None, None]: ...
def do_bash_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_fish_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_zsh_complete(cli: click.Command, prog_name: str) -> bool: ...
def do_powershell_complete(cli: click.Command, prog_name: str) -> bool: ...
def get_code(
    shell: str | None = None,
    prog_name: str | None = None,
    env_name: str | None = None,
    extra_env: dict[str, str] | None = None,
) -> str: ...
def install(
    shell: str | None = None,
    prog_name: str | None = None,
    env_name: str | None = None,
    path: str | None = None,
    append: bool | None = None,
    extra_env: dict[str, str] | None = None,
) -> tuple[ShellName, str]: ...
