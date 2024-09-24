from enum import Enum
from typing import Any, Callable, Type

import click
from click import ParamType
from click_completion.core import (
    Shell as Shell,
    completion_configuration as completion_configuration,
    get_choices as get_choices,
    get_code as get_code,
    install as install,
    resolve_ctx as resolve_ctx,
    shells as shells,
    startswith as startswith,
)
from click_completion.lib import get_auto_shell as get_auto_shell

__version__: str
_initialized: bool

def init(
    complete_options: bool = False,
    match_incomplete: Callable[[str, str], bool] | None = None,
) -> None: ...

class DocumentedChoice(ParamType):
    name: str
    def __init__(self, choices: dict[str, str] | Type[Enum]) -> None: ...
    def get_metavar(self, param: Any) -> str: ...
    def get_missing_message(self, param: Any) -> str: ...
    def convert(self, value: str, param: Any, ctx: click.Context) -> str | None: ...
    def __repr__(self) -> str: ...
    def complete(
        self, ctx: click.Context, incomplete: str
    ) -> list[tuple[str, str]]: ...
