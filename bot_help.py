from typing import List

import data
import defs


def do_help(is_owner: bool, is_guild_owner: bool, is_dm: bool) -> List[str]:
    content: List[str] = []
    if is_dm:
        if is_owner:
            content[0] = (f"\t**Commands:**\n*(the brackets `[]` are **not** part of the commands)*"
                          f"\n[{data.self_mention}` list warnings @mention_user`]"
                          f"\n\tLists a user's warnings across all servers."
                          f"\n[{data.self_mention}` leave server server_id`]"
                          f"\n\tMakes the bot leave server with ID `server_id`")
    else:
        if is_owner or is_guild_owner:
            content[0] = f"\t**Commands:**\n*(the brackets `[]` are **not** part of the commands)*" \
                         f"\n**---===---Admin commands---===---**"
            content.append(
                f"\n**---Warnings---**"
                f"\n[{data.self_mention}` warn @user warning_message`]"
                f"\n\tWarns mentioned user."
                f"\n\tWarning message will be either `warning_message` or a default message if none is given."
                f"\n[{data.self_mention}` clear warnings @user`] or [{data.self_mention}` unwarn @user`]"
                f"\n\tRemoves all warnings for mentioned user."
                f"\n[{data.self_mention}` list warnings`] or [{data.self_mention}` list warnings @user`]"
                f"\n\tIf a user is mentioned, list all of that user's warnings for this server."
                f"\n\tOtherwise, counts all warnings in this server, per user.")
            content.append(
                f"\n**---Mutes---**"
                f"\n**(these only work if mute roles were configured for this server)**"
                f"\n[{data.self_mention}` mute @user`]"
                f"\n\tMutes mentioned user."
                f"\n[{data.self_mention}` temp mute @user #h #m #s`] or [{data.self_mention}` arrest @user #h #m #s`]"
                f"\n\tMutes mentioned user for the duration specified,"
                f"\n\twhere `#` are numbers and `h`, `m` and `s`"
                f"\n\trepresent hours, minutes and seconds, respectively."
                f"\n[{data.self_mention}` unmute @user`]"
                f"\n\tUnmutes mentioned user. (including both temporary and permanent mutes)")
            content.append(
                f"\n**---Kicks---**"
                f"\n[{data.self_mention}` kick @user`]"
                f"\n\tKicks mentioned user")
            content.append(
                f"\n**---Bans---**"
                f"\n[{data.self_mention}` ban @user`] or [{data.self_mention}` kill @user`]"
                f"\n\tBans mentioned user"
                f"\n[{data.self_mention}` temp ban @user #h #m #s`] or [{data.self_mention}` shoot @user #h #m #s`]"
                f"\n\tBans user for the duration specified,"
                f"\n\twhere `#` are numbers and `h`, `m` and `s`"
                f"\n\trepresent hours, minutes and seconds, respectively."
                f"\n\t(do note that once user has been unbanned, they still have to join the server themselves."
                f"\n[{data.self_mention}` unban user_id`]"
                f"\n\tUnbans user with ID `user_id`"
                f"\n\t**Do note that this command does not work with mentions, it needs the user's ID,"
                f"\n\tsince the user isn't, by definition, a part of the server.**")
            content.append(
                f"\n**---Reaction Roles---**"
                f"\n[{data.self_mention}` add reaction role role_id emoji`]"
                f"\n\tAdds the role with id `role_id` to the reaction roles, associated with the emoji `emoji`."
                f"\n[{data.self_mention}` remove reaction role role_id`]"
                f"\n\tRemoves the role with id `role_id` from the reaction roles."
                f"\n[{data.self_mention}` reaction role message`]"
                f"\n\tCreates a message to work with this server's reaction roles."
                f"\n\tThe message is auto-updated. If you don't want it anymore, just delete it."
                f"\n[{data.self_mention}` list reaction roles`]"
                f"\n\tList all reaction roles currently configured for this server.")
            content.append(
                f"\n**---Misc---**"
                f"\n[{data.self_mention}` clear`] or [{data.self_mention}` clear all`]"
                f" or [{data.self_mention}` clear number`]"
                f"\n\tAttempts to delete the last `number` messages."
                f"\n\tIf no number is specified, deletes a single message."
                f"\n\tIf `all` is specified, deletes a large amount of messages."
                f"\n\t(ask bot owner for specific amount)"
                f"\n[{data.self_mention}` owoify`]"
                f"\n\tOwoifies or de-owoifies current channel.")
        content.append(
            f"**---===---Regular commands---===---**"
            f"\n-> If you mention me, I can tell you some server **status** or tell you your current **warnings**"
            f"\n-> Since I'm polite, I'll greet those who greet me properly."
            f"\n-> I'll also greet people if I know who they are."
            f"\n-> I can also tell you my family creed. Don't overdo it though."
            f"\n-> Since many people ask me whether I'm a public bot, that's also a command."
            f"\n-> If you want tea, just ask 'Dear {defs.readable_bot_name}, could you kindly serve me some tea?'"
            f"\n-> I do not appreciate impolite people."
            f"\n-> No simps"
            f"\n-> UwU"
            f"\n-> I bet you didn't know, but you can also ask me for **help**!"
        )
    return content
