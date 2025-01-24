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
    min_fragment_len: int = 0,
    fragment_len: int = 0,
) -> Generator[str, None, None]:
    """
    Recursively splits an HTML message into smaller fragments based on tags.

    Args:
        contents (list): The list of parsed HTML elements to split.
        fragment_max_len (int): The maximum allowed length for each fragment.
        fragmentizable_tags (list[str]): Tags that can be split
            further (e.g., "p", "div").
        min_fragment_len (int): The minimal possible length of the
            fragment being built (default is 0).
        fragment_len (int): The current length of the fragment being
            built (default is 0).

    Yields:
        str: Fragments of the message that are within the maximum length.
    """
    if min_fragment_len >= fragment_max_len:
        raise FragmentTooLongError(min_fragment_len + 1, fragment_max_len)

    fragment = ""
    for content in contents:
        content_len = len(str(content))

        if fragment_len + content_len == fragment_max_len:
            yield fragment + str(content)

            fragment = ""
            fragment_len = min_fragment_len
            continue

        elif fragment_len + content_len < fragment_max_len:
            fragment += str(content)
            fragment_len += len(str(content))
            continue

        if not hasattr(content, "contents"):
            # TEXT
            content_str = str(content)
            while content_str:
                available_len = fragment_max_len - fragment_len

                if available_len <= len(content_str):
                    yield fragment + content_str[:available_len]
                    content_str = content_str[available_len:]

                    fragment = ""
                    fragment_len = min_fragment_len
                else:
                    fragment = content_str
                    fragment_len = min_fragment_len + len(fragment)
                    break

        elif content.name not in fragmentizable_tags:
            # UNSPLITTABLE TAG
            yield fragment

            fragment = str(content)
            fragment_len = min_fragment_len + len(fragment)

        else:
            # SPLITTABLE TAG
            has_tag = content.name is not None
            tag_to_open = (
                str(content).split(str(content.contents[0]))[0]
                if has_tag
                else ""
            )
            tag_to_close = f"</{content.name}>" if has_tag else ""

            tags_len = len(tag_to_open) + len(tag_to_close)

            if fragment_len + tags_len >= fragment_max_len:
                yield fragment

                fragment = ""
                fragment_len = min_fragment_len

            subfragments = list(
                split_message_recursive(
                    content.contents,
                    fragment_max_len,
                    fragmentizable_tags,
                    min_fragment_len + tags_len,
                    fragment_len + tags_len,
                )
            )

            if len(subfragments) > 0:
                yield fragment + (
                    f"{tag_to_open}{subfragments[0]}{tag_to_close}"
                )

                fragment = ""
                fragment_len = min_fragment_len

            if len(subfragments) > 2:
                for subfragment in subfragments[1:-1]:
                    yield f"{tag_to_open}{subfragment}{tag_to_close}"

            fragment = f"{tag_to_open}{subfragments[-1]}{tag_to_close}"
            fragment_len = min_fragment_len + len(fragment)

    yield fragment
