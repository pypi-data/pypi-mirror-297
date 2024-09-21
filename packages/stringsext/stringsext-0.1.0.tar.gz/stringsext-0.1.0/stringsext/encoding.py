from dataclasses import dataclass
from enum import IntEnum, StrEnum


# class for ascii number, a number must be created using this class to be a valid ascii number
class AsciiCode(int):
    @classmethod
    def from_string(cls: type["AsciiCode"], s: str) -> "AsciiCode":
        try:
            return cls(ord(s))
        except ValueError:
            raise ValueError(f"Invalid ascii character: {s}")


class EncodingName(StrEnum):
    ASCII = "ascii"
    BIG5 = "Big5"
    EUC_JP = "EUC-JP"
    EUC_KR = "EUC-KR"
    GBK = "GBK"
    IBM866 = "IBM866"
    ISO_2022_JP = "ISO-2022-JP"
    ISO_8859_10 = "ISO-8859-10"
    ISO_8859_13 = "ISO-8859-13"
    ISO_8859_14 = "ISO-8859-14"
    ISO_8859_15 = "ISO-8859-15"
    ISO_8859_16 = "ISO-8859-16"
    ISO_8859_2 = "ISO-8859-2"
    ISO_8859_3 = "ISO-8859-3"
    ISO_8859_4 = "ISO-8859-4"
    ISO_8859_5 = "ISO-8859-5"
    ISO_8859_6 = "ISO-8859-6"
    ISO_8859_7 = "ISO-8859-7"
    ISO_8859_8 = "ISO-8859-8"
    ISO_8859_8_I = "ISO-8859-8-I"
    KOI8_R = "KOI8-R"
    KOI8_U = "KOI8-U"
    SHIFT_JIS = "Shift_JIS"
    UTF_16BE = "UTF-16BE"
    UTF_16LE = "UTF-16LE"
    UTF_8 = "UTF-8"
    GB18030 = "gb18030"
    MACINTOSH = "macintosh"
    REPLACEMENT = "replacement"
    WINDOWS_1250 = "windows-1250"
    WINDOWS_1251 = "windows-1251"
    WINDOWS_1252 = "windows-1252"
    WINDOWS_1253 = "windows-1253"
    WINDOWS_1254 = "windows-1254"
    WINDOWS_1255 = "windows-1255"
    WINDOWS_1256 = "windows-1256"
    WINDOWS_1257 = "windows-1257"
    WINDOWS_1258 = "windows-1258"
    WINDOWS_874 = "windows-874"
    X_MAC_CYRILLIC = "x-mac-cyrillic"
    X_USER_DEFINED = "x-user-defined"


class AsciiFilter(IntEnum):
    ALL = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE
    ALL_CTRL = 0x7FFFFFFFFFFFFFFFFFFFFFFF00000000
    ALL_CTRL_WSP = 0x7FFFFFFFFFFFFFFFFFFFFFFF00001E00
    DEFAULT = 0x7FFFFFFFFFFFFFFFFFFFFFFF00000000
    NONE = 0x0
    WSP = 0x100001E00


class UnicodeBlockFilter(IntEnum):
    AFRICAN = 0xFFE00000
    ALL_ASIAN = 0x1FC003FFFFFFFC
    ALL = 0x1FFFFFFFFFFFFC
    ARABIC = 0x3F000000
    ARMENIAN = 0x200000
    ASIAN = 0x3FFC00000000
    CJK = 0x3F000000000
    COMMON = 0xFFFFFFFC
    CYRILLIC = 0x1F0000
    DEFAULT = 0x1FFFFFFFFFFFFC
    GREEK = 0xC000
    HANGUL = 0x380000000000
    HEBREW = 0xC00000
    KANA = 0x800000000
    LATIN = 0x31FC
    NONE = 0x0
    PRIVATE = 0x10400000000000
    UNCOMMON = 0x1F400000000000


EncodingFilter = AsciiFilter | UnicodeBlockFilter


@dataclass
class Encoding:
    enc_name: EncodingName
    chars_min: int | None = None
    filter: int | None = None
    grep_char: AsciiCode | None = None

    def __str__(self) -> str:
        text = ",".join(
            [
                self.enc_name,
                str(self.chars_min) if self.chars_min is not None else "",
                hex(self.filter) if self.filter is not None else "",
                hex(self.grep_char) if self.grep_char is not None else "",
            ]
        )
        return text
