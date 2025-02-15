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

## Project Structure

- `src/`
    Contains the main source code for the project
  - `exceptions`
        Defines any custom exception classes used by the application
  - `splitter.py` Main module containing the logic
        for splitting messages

- `tests/`
    Holds all test-related files
  - `html_files/`
        Contain HTML files used for testing purposes
  - `unit/`
        Contains unit tests for different
        parts of the application

- `split_msg.py`
    A CLI entry point that uses the logic from src/splitter/splitter.py to split messages.
