# HTML Message Splitter

## Overview

This project provides a solution for splitting large HTML-formatted messages into smaller fragments that conform to a specified character limit (`max_len`). The primary use case is to ensure that messages processed by a corporate messenger bot do not exceed the API-imposed limit of 4096 characters, while preserving the correctness of the HTML structure and formatting in each fragment.

## Usage

### Installation

To set up the project, run the following command:

```bash
poetry install
```

### Running the Script

Use the script with the following parameters:

- `--max-len`: Specifies the maximum character length for each message fragment.
- Path to the input HTML file.

Example:

```bash
python split_msg.py --max-len=3072 ./test-1.html
```

### Development

For development tasks, the following commands are available:

- Linting: `make lint`
- Formatting: `make format`
- Running tests: `make test`
