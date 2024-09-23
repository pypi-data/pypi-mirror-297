from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.io.inputs.argument import Argument


class NewCommand(Command):
    name: str = "new"

    description = "Create a new Expanse project."

    arguments: ClassVar[list[Argument]] = [
        argument("path", "The path where the new project will be created.")
    ]

    def handle(self) -> int:
        return 0
