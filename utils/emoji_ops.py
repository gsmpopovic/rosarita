from typing import Dict, Union

from discord import Guild, Emoji, PartialEmoji


def parse_emoji(emoji: Union[Emoji, PartialEmoji, str]) -> str:
    if isinstance(emoji, str):
        return emoji.lower()
    elif isinstance(emoji, PartialEmoji) and not emoji.is_custom_emoji():
        return emoji.name
    elif emoji.id is None:
        return f"<:{emoji.name}:>".lower()
    else:
        return f"<:{emoji.name}:{emoji.id}>".lower()
