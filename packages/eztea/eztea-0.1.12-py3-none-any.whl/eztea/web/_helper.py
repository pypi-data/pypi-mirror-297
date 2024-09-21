from typing import List


def join_url_path(__a: str, *paths: List[str]) -> str:
    """Join url paths, insert '/' if needed."""
    r = __a
    for p in paths:
        if r[-1:] == "/" and p[:1] == "/":
            r += p[1:]
        elif r[-1:] != "/" and p[:1] != "/":
            r += "/" + p
        else:
            r += p
    return r


def shorten(text, width, placeholder="..."):
    """
    >>> shorten('123456789', width=8)
    '12345...'
    >>> shorten('123456789', width=9)
    '123456789'
    >>> shorten(None, width=8) is None
    True
    """
    if not text:
        return text
    if len(text) <= width:
        return text
    return text[: max(0, width - len(placeholder))] + placeholder
