import random
import re
from typing import List

faces: List[str] = ["(・`ω´・)", ";;w;;", "owo", "UwU", ">w<", "^w^"]
_matchers = {}
_replacers = {}


def owoify(content: str) -> str:
    content = replace('na', 'nya', content)
    content = replace('ove', 'uv', content)
    return (content
            .replace('r', 'w')
            .replace('R', 'W')
            .replace('l', 'w')
            .replace('L', 'W')
            .replace('!', f" {random.choice(faces)}"))


def limited_content(content: str, limited: List[str] = None, separator: str = "\n") -> List[str]:
    if limited is None or not limited:
        return [content]
    if len(limited[-1]) + len(content) <= 1800:
        limited[-1] += separator + content
    else:
        limited.append(content)
    return limited


def _word_matcher(word: str):
    def wrapper(message: str) -> bool:
        return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(message) is not None

    return wrapper


def _replacer(word: str):
    def wrapper(replacement: str, message: str) -> str:
        return re.compile(r'({0})'.format(word), flags=re.IGNORECASE).sub(replacement, message)

    return wrapper


def match(word: str, message: str) -> bool:
    if word not in _matchers:
        _matchers[word] = _word_matcher(word)
    return _matchers[word](message)


def replace(word: str, replacement: str, message: str) -> str:
    if word not in _replacers:
        _replacers[word] = _replacer(word)
    return _replacers[word](replacement, message)
