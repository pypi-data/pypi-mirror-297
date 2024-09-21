# stringsext

A Python wrapper for the `stringsext` command-line tool, providing a convenient interface for extracting strings from binary files.

## Installation

1. First, ensure you have the `stringsext` command-line tool installed on your system. You can find installation instructions [here](https://github.com/getreu/stringsext?tab=readme-ov-file#building-and-installing).

2. Install the Python library using pip:

```
pip install stringsext
```

## Basic Usage

Here's a simple example of how to use the `stringsext` library:

```python
from pathlib import Path
from stringsext.core import Stringsext
from stringsext.encoding import EncodingName

# Create a Stringsext instance
extractor = Stringsext()

# Configure the extraction
results = (
    extractor.encoding(EncodingName.UTF_8, chars_min=4)
    .add_file(Path("example.bin"))
    .run()
)

# Parse the results
findings = results.parse()

# Print the findings
for finding in findings:
    print(f"Found: {finding.content}, encoding: {finding.encoding_info.name}")
```

## Parsing Results

The `parse` method is a crucial part of the `stringsext` library. It converts the raw output from the `stringsext` command-line tool into Python objects, making it easier to work with the results in your code.

After running the extraction with the `run()` method, you can call `parse()` on the results to get a list of `StringFinding` objects:

```python
findings = results.parse()
```

Each `StringFinding` object contains the following information:

-   `content`: The extracted string
-   `input_file`: The path to the file from which the string was extracted
-   `offset_info`: Information about the string's location in the file
-   `encoding_info`: Information about the encoding of the string

Here's an example of how to work with the parsed results:

```python
for finding in findings:
    print(f"Content: {finding.content}")
    print(f"File: {finding.input_file}")
    print(f"Offset: {finding.offset_info.exact}")
    print(f"Encoding: {finding.encoding_info.name}")
    print("---")
```

The `parse_stringsext_output` function handles the parsing of the raw output. It's used internally by the `parse()` method, but you can also use it directly if you have raw `stringsext` output:

```python
from stringsext.parse import parse_stringsext_output

raw_output = "... raw stringsext output ..."
files = [Path("example.bin")]
encodings = [EncodingName.UTF_8]

findings = parse_stringsext_output(raw_output, files, encodings)
```

## Advanced Features

### Multiple Encodings

You can search for strings in multiple encodings:

```python
extractor = Stringsext()
results = (
    extractor.encoding(EncodingName.UTF_8, chars_min=4)
    .encoding(EncodingName.UTF_16LE, chars_min=4)
    .encoding(EncodingName.UTF_16BE, chars_min=4)
    .add_file(Path("example.bin"))
    .run()
)
```

### Unicode Block Filtering

Filter strings based on Unicode blocks:

```python
from stringsext.encoding import UnicodeBlockFilter

extractor = Stringsext()
results = (
    extractor.encoding(EncodingName.UTF_8)
    .unicode_block_filter(UnicodeBlockFilter.ARABIC)
    .add_file(Path("example.bin"))
    .run()
)
```

### ASCII Filtering

Apply ASCII filters to refine your search:

```python
from stringsext.encoding import AsciiFilter

extractor = Stringsext()
results = (
    extractor.encoding(EncodingName.ASCII)
    .ascii_filter(AsciiFilter.PRINTABLE)
    .add_file(Path("example.bin"))
    .run()
)
```

### Multiple Files

Search through multiple files in one go:

```python
extractor = Stringsext()
results = (
    extractor.encoding(EncodingName.UTF_8)
    .add_file(Path("file1.bin"))
    .add_file(Path("file2.bin"))
    .run()
)
```

## Example: Extracting UUIDs

Here's an example of how to use `stringsext` to extract UUIDs from a binary file:

```python
import re
from pathlib import Path
from stringsext.core import Stringsext
from stringsext.encoding import EncodingName

UUID_PATTERN = r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"

def extract_uuids(content: str) -> list[str]:
    return list(set(re.findall(UUID_PATTERN, content)))

extractor = Stringsext()
findings = (
    extractor.encoding(EncodingName.UTF_8, chars_min=36)
    .encoding(EncodingName.UTF_16LE, chars_min=36)
    .encoding(EncodingName.UTF_16BE, chars_min=36)
    .add_file(Path("example.bin"))
    .run()
    .parse()
)

for finding in findings:
    uuids = extract_uuids(finding.content)
    for uuid in uuids:
        print(f"Found UUID: {uuid}, encoding: {finding.encoding_info.name}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
