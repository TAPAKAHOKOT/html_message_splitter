import os

import click

from src.splitter import split_message


@click.command()
@click.option(
    "--max-len", default=4096, help="One fragment length (default: 4096)"
)
@click.argument("message_source")
def main(message_source: str, max_len: int):
    """
    Processes a file with message, ensuring it exists and
    performs split message operations based on the provided
    maximum fragment length.

    :param max_len: Maximum length of one fragment. Default is 4096.
    :param message_filepath: Path to the message file to process.
    :raises FileNotFoundError: If the specified message file does not exist.
    """
    if not os.path.isfile(message_source):
        raise FileNotFoundError(
            f"The file at path '{message_source}' does not exist."
        )

    with open(message_source, "r", encoding="utf-8") as f:
        message_content = f.read()

    for i, fragment in enumerate(split_message(message_content, max_len), 1):
        click.echo(f"-- fragment #{i}: {len(fragment)} chars --")
        click.echo(fragment)


if __name__ == "__main__":
    main()
