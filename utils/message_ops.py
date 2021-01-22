from typing import Union

from discord import User, Member


def parse(content: str, member: Union[User, Member]) -> str:
    return content.replace("{mention}", member.mention)
