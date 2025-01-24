from typing import Generator

from bs4 import BeautifulSoup

from src.exceptions.fragment_too_long import FragmentTooLongError


def split_message(source: str, max_len: int) -> Generator[str, None, None]:
    """
    Splits an HTML message into smaller fragments without
    exceeding the maximum length.

    Args:
        source (str): The HTML source string to be split.
        max_len (int): The maximum allowed length for each fragment.

    Yields:
        str: Fragments of the message that are within the maximum length.

    Raises:
        FragmentTooLongError: If it is impossible to split content
        with the allowed maximum length.
    """
    soup = BeautifulSoup(source, "html.parser")

    for fragment in split_message_recursive(
        soup.contents,
        max_len,
        [
            "p",
            "b",
            "strong",
            "i",
            "ul",
            "ol",
            "div",
            "span",
        ],
    ):
        fragment_len = len(fragment)
        if fragment_len == 0:
            continue

        if fragment_len > max_len:
            raise FragmentTooLongError(fragment_len, max_len)

        yield fragment


def split_message_recursive(
    contents: list,
    fragment_max_len: int,
    fragmentizable_tags: list[str],
    fragment: str = "",
    fragment_len: int = 0,
    tag_to_open: str = "",
    tags_to_close: str = "",
) -> Generator[str, None, None]:
    """
    Recursively splits an HTML message into smaller fragments based on tags.

    Args:
        contents (list): The list of parsed HTML elements to split.
        fragment_max_len (int): The maximum allowed length for each fragment.
        fragmentizable_tags (list[str]): Tags that can be split
            further (e.g., "p", "div").
        fragment (str): The current fragment being
            built (default is an empty string).
        fragment_len (int): The current length of the fragment being
            built (default is 0).
        tag_to_open (str): The opening tag to include in the
            fragment (default is an empty string).
        tags_to_close (str): The closing tags to include at
            the end of the fragment (default is an empty string).

    Yields:
        str: Fragments of the message that are within the maximum length.
    """
    tags_to_close_len = len(tags_to_close)

    content_index = 0
    while content_index < len(contents):
        content = contents[content_index]
        content_len = len(str(content))

        if fragment_len + content_len + tags_to_close_len > fragment_max_len:
            if (
                not hasattr(content, "contents")
                or content.name not in fragmentizable_tags
            ):
                yield fragment

                fragment = str(content)
                fragment_len = content_len

                content_index += 1
                continue

            subtag_to_open = str(content).split(str(content.contents[0]))[0]
            subfragments = list(
                split_message_recursive(
                    content.contents,
                    fragment_max_len,
                    fragmentizable_tags,
                    fragment,
                    fragment_len,
                    subtag_to_open,
                    f"</{content.name}>",
                )
            )

            if len(subfragments) == 1:
                yield fragment + tags_to_close
                fragment = str(content)
                fragment_len = len(fragment)
            elif len(subfragments) >= 2:
                yield subfragments[0] + tags_to_close

                for subfragment in subfragments[1:-1]:
                    yield subfragment

                fragment = subfragments[-1]
                fragment_len = len(str(fragment))
        else:
            fragment += str(content)
            fragment_len += content_len

        content_index += 1

    yield tag_to_open + fragment + tags_to_close
