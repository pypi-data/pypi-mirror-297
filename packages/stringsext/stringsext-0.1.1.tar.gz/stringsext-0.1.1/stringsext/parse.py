import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from stringsext.encoding import EncodingName
from stringsext.utils import expect


@dataclass
class OffsetInfo:
    exact: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None
    is_continuation: bool = False

    @property
    def range(self) -> Optional[tuple[Optional[int], Optional[int]]]:
        if self.start is not None or self.end is not None:
            return (self.start, self.end)
        return None


@dataclass
class EncodingInfo:
    scanner_index: int
    name: EncodingName


@dataclass
class StringFinding:
    content: str
    input_file: Path
    offset_info: OffsetInfo
    encoding_info: EncodingInfo


def parse_file(text: str, files: list[Path]) -> tuple[Path, str]:
    """Parse the file index from a string, return the index and remaining text"""
    text = text.lstrip()
    if len(files) == 1:
        return files[0], text
    matched = expect(re.match(r"([A-Z])", text), f"Invalid file index in '{text}'")
    file_index = ord(matched.group(1)) - ord("A")
    return files[file_index], text[matched.end() :]


def parse_offset_info(text: str) -> tuple[OffsetInfo, str]:
    """Parse an offset info string into an OffsetInfo object"""

    def get_number(text: str) -> int:
        number_text = "".join([c for c in text if c.isdigit()])
        return int(number_text, 16)

    text = text.lstrip()
    matched = expect(re.match(r"([0-9A-Fa-f<>+]+)", text), f"Invalid offset info in '{text}'")
    offset_info = OffsetInfo()
    match matched.group().strip():
        case s if s.startswith(">"):
            offset_info.is_continuation = True
            offset_info.end = get_number(s[1:])
        case s if s.startswith("<"):
            offset_info.start = get_number(s[1:])
        case s if s.endswith("+"):
            offset_info.exact = get_number(s[:-1])
        case _:
            offset_info.exact = int(matched.group(), 16)
    return offset_info, text[matched.end() :]


def parse_encoding_info(text: str) -> tuple[EncodingInfo, str]:
    """Parse an encoding string into an index and encoding, return the index and remaining text"""
    text = text.lstrip()
    matched = expect(re.match(r"^\(([a-z]) (.+?)\)", text), f"Invalid encoding info in '{text}'")
    scanner_index = ord(matched.group(1)) - ord("a")
    encoding = EncodingName(matched.group(2))
    return EncodingInfo(scanner_index, encoding), text[matched.end() :]


def parse_content(text: str) -> str:
    """Parse the content from a string, return the content and remaining text"""
    return text.lstrip()


def parse_stringsext_output(
    output: str, files: list[Path], encodings: list[EncodingName]
) -> list[StringFinding]:
    """Parse the output of stringsext into a list of StringFindings"""

    def parse_line(line: str) -> StringFinding | None:
        """Parse a single line of output"""
        if len(line) < 4:
            return None
        input_file, line = parse_file(line, files)
        offset_info, line = parse_offset_info(line)
        encoding_info, line = (
            parse_encoding_info(line)
            if len(encodings) > 1
            else (EncodingInfo(0, encodings[0]), line)
        )
        content = parse_content(line)
        return StringFinding(
            content=content,
            input_file=input_file,
            offset_info=offset_info,
            encoding_info=encoding_info,
        )

    return list(filter(None, map(parse_line, output.splitlines())))
