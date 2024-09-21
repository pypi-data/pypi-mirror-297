import subprocess
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Self

from stringsext.encoding import (
    AsciiCode,
    AsciiFilter,
    Encoding,
    EncodingFilter,
    EncodingName,
    UnicodeBlockFilter,
)
from stringsext.parse import StringFinding, parse_stringsext_output


class Radix(StrEnum):
    HEX = "x"
    OCTAL = "o"
    DECIMAL = "d"


def get_executable() -> Path:
    """Find the path to the `stringsext` executable."""
    stringsext = subprocess.check_output(["which", "stringsext"]).decode("utf-8").strip()
    if not stringsext:
        raise FileNotFoundError(
            "stringsext executable not found. Please install stringsext first.\n"
            "https://github.com/getreu/stringsext?tab=readme-ov-file#building-and-installing"
        )
    return Path(stringsext)


@dataclass
class StringsextOptions:
    ascii_filter: AsciiFilter | None = None
    no_metadata: bool = False
    debug_options: bool = False
    encodings: list[Encoding] = field(default_factory=list)
    grep_char: AsciiCode | None = None
    chars_min: int | None = None
    output_file: Path | None = None
    output_line_len: int | None = None
    same_unicode_block: bool = False
    counter_offset: int | None = None
    radix: Radix | None = None
    unicode_block_filter: UnicodeBlockFilter | None = None
    files: list[Path] = field(default_factory=list)


class StringsextError(Exception): ...


class StringsextOutput:
    def __init__(self, output: str, input_files: list[Path], enc_names: list[EncodingName]) -> None:
        self.output = output
        self.input_files = input_files
        self.encodings = enc_names

    def __repr__(self) -> str:
        return self.output

    def __str__(self) -> str:
        return self.output

    def parse(self) -> list[StringFinding]:
        return parse_stringsext_output(self.output, self.input_files, self.encodings)


class Stringsext:
    def __init__(self) -> None:
        self.options = StringsextOptions()

    def ascii_filter(self, af: AsciiFilter) -> Self:
        self.options.ascii_filter = af
        return self

    def no_metadata(self) -> Self:
        self.options.no_metadata = True
        return self

    def debug_options(self) -> Self:
        self.options.debug_options = True
        return self

    def encoding(
        self,
        enc: EncodingName,
        chars_min: int | None = None,
        filter: int | EncodingFilter | None = None,
        grep_char: AsciiCode | None = None,
    ) -> Self:
        self.options.encodings.append(Encoding(enc, chars_min, filter, grep_char))
        return self

    def grep_char(self, ascii_char: str) -> Self:
        self.options.grep_char = AsciiCode(ascii_char)
        return self

    def chars_min(self, min_chars: int) -> Self:
        self.options.chars_min = min_chars
        return self

    def output_file(self, file: Path) -> Self:
        self.options.output_file = file
        return self

    def output_line_len(self, length: int) -> Self:
        self.options.output_line_len = length
        return self

    def same_unicode_block(self) -> Self:
        self.options.same_unicode_block = True
        return self

    def counter_offset(self, offset: int) -> Self:
        self.options.counter_offset = offset
        return self

    def unicode_block_filter(self, ubf: UnicodeBlockFilter) -> Self:
        self.options.unicode_block_filter = ubf
        return self

    def add_file(self, file: Path) -> Self:
        self.options.files.append(file)
        return self

    @property
    def command(self) -> list[str]:
        cmd: list[str] = []

        if self.options.ascii_filter:
            cmd.extend(["-a", hex(self.options.ascii_filter)])
        if self.options.no_metadata:
            cmd.append("-c")
        if self.options.debug_options:
            cmd.append("-d")
        for encoding in self.options.encodings:
            cmd.extend(["-e", str(encoding)])
        if self.options.grep_char is not None:
            cmd.extend(["-g", str(self.options.grep_char)])
        if self.options.chars_min is not None:
            cmd.extend(["-n", str(self.options.chars_min)])
        if self.options.output_file:
            cmd.extend(["-p", str(self.options.output_file)])
        if self.options.output_line_len is not None:
            cmd.extend(["-q", str(self.options.output_line_len)])
        if self.options.same_unicode_block:
            cmd.append("-r")
        if self.options.counter_offset is not None:
            cmd.extend(["-s", str(self.options.counter_offset)])
        if self.options.unicode_block_filter:
            cmd.extend(["-u", hex(self.options.unicode_block_filter)])

        cmd.extend(["-t", Radix.HEX.value])  # always use hex
        cmd.append("--")
        cmd.extend([str(file) for file in self.options.files])
        return cmd

    def run(self, executable: Path | str | None = None, verbose: bool = False) -> StringsextOutput:
        executable = executable or get_executable()
        if verbose:
            print(f"Running: {executable} {' '.join(self.command)}")
        result = subprocess.run([executable, *self.command], capture_output=True, text=True)
        try:
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            raise StringsextError(
                f"Error running stringsext:\n\nStdout:\n{e.stdout}\n\nStderr:\n{e.stderr}\n\nReturn code: {e.returncode}"
            ) from e
        encoding_names = [encoding.enc_name for encoding in self.options.encodings]
        return StringsextOutput(result.stdout, self.options.files, encoding_names)


def list_encodings(executable: Path | str | None = None) -> tuple[str, str]:
    executable = executable or get_executable()
    result = subprocess.run([executable, "-l"], capture_output=True, text=True)
    return result.stdout, result.stderr


def version(executable: Path | str | None = None) -> tuple[str, str]:
    executable = executable or get_executable()
    result = subprocess.run([executable, "-V"], capture_output=True, text=True)
    return result.stdout, result.stderr
