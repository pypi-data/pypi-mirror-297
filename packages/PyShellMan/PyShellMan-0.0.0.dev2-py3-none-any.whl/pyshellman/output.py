from typing import NamedTuple as _NamedTuple

from rich import text as _text, console as _console, panel as _panel, markdown as _markdown


class ShellOutput(_NamedTuple):
    command: str
    code: int | None = None
    output: str | bytes | None = None
    error: str | bytes | None = None

    @property
    def executed(self) -> bool:
        return self.code is not None

    @property
    def succeeded(self) -> bool:
        return self.code == 0

    @property
    def details(self) -> dict[str, str | bytes | int]:
        details = {"Command": self.command, "Executed": self.executed}
        if self.executed:
            details["Exit Code"] = self.code
        if self.output:
            details["Output"] = self.output
        if self.error:
            details["Error"] = self.error
        return details

    @property
    def summary(self) -> str:
        if not self.executed:
            return f"Command could not be executed."
        if not self.succeeded:
            return f"Command failed with exit code {self.code}."
        return f"Command executed successfully."

    def __rich__(self):
        group = [
            _markdown.Markdown(f"- **Command**: `{self.command}`"),
            _markdown.Markdown(f"- **Executed**: {self.executed}"),
        ]
        if self.executed:
            group.append(_markdown.Markdown(f"- **Exit Code**: {self.code}"))
        if self.output:
            output = self.output if not isinstance(self.output, str) else _text.Text.from_ansi(self.output)
            group.append(_panel.Panel(output, title="Output"))
        if self.error:
            error = self.error if not isinstance(self.error, str) else _text.Text.from_ansi(self.error)
            group.append(_panel.Panel(error, title="Error"))
        out = _panel.Panel(
            _console.Group(*group),
            title="Shell Command Output",
        )
        return out

    def __str__(self):
        return "\n".join([f"- {key}: {value}" for key, value in self.details.items()])
