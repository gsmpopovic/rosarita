from typing import List

import data
import defs


def do_help(is_owner: bool, is_guild_owner: bool, is_dm: bool) -> List[str]:
    content: List[str] = []
    interval="Xs/m/h/d"
    hour="HH:MM"
    if is_dm:
        if is_owner:
            content.append(f"\t**Commands:**\n*(the brackets `[]` are **not** part of the commands)*"
                           f"\n[{data.self_mention}` list warnings @mention_user`]"
                           f"\n\tLists a user's warnings across all servers."
                           f"\n[{data.self_mention}` leave server server_id`]"
                           f"\n\tMakes the bot leave server with ID `server_id`")
    else:
        if is_owner or is_guild_owner:
            content.append(                
                "\n**---Support---**"
                "\n Find tech support at: https://discord.gg/48cgK679PU")
            content.append(f"\t**Commands:**\n*(the brackets `[]` are **not** part of the commands)*"
                           f"\n**---===---Admin commands---===---**")
            content.append(
                f"\n**---Warnings---**"
                f"\n[{data.self_mention}` warn @user (warning_message) {'reason'}`]"
                f"\n\tWarns mentioned user."
                f"\n\tWarning message will be either `warning_message` or a default message if none is given."
                f"\n\Requires the parameter {'reason'}, i.e., a reason entered between curly braces."
                f"\n[{data.self_mention}` remove warnings @user`] or [{data.self_mention}` unwarn @user`]"
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
                f" or [{data.self_mention}` snipe X edits/deletes`]"
                f"\n\tAttempts to snipe (retrieve) a set number of deleted or edited messages."
                f"\n\tEdited and deleted messages are deleted 30 seconds after deletion or edit."

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
        content.append(
            f"**---===---Music commands---===---**"
            f"\n^^^ {data.self_mention} music play https://www.youtube.com/some-video-url ^^^"
            f"\n <<< {defs.readable_bot_name} will join the voice channel which message author is currently in,"
            F"\n and play the song given in the URL. Message author *must* be in a voice channel. <<<"
            F"\n If a song is already playing, the URL will be passed to a queue. <<<"
            f"\n^^^ {data.self_mention} music pause ^^^"
            f"\n <<< {defs.readable_bot_name} will pause the song currently playing. <<<"
            f"\n^^^ {data.self_mention} music resume ^^^"
            f"\n <<< {defs.readable_bot_name} will resume the song that was paused. <<<"
            f"\n^^^ {data.self_mention} music stop ^^^"
            f"\n <<< {defs.readable_bot_name} will cease playing and exit queue. <<<"
        )
        content.append(
            f"**---===--- Scheduling commands---===---**"
            f"\n^^^ {data.self_mention} remind me ('something here') in  {interval}  y ^^^"
            F"\n<<< {defs.readable_bot_name} will DM message author with the content set in parentheses () at interval, s/m/h/d stands for seconds, minutes, etc. <<<"
            F"\n<<< y is an optional parameter and designates that this reminder will be recurring, i.e., for the interval set by the message author.<<<"

            f"\n^^^ {data.self_mention} remind me ('something here') at {hour} y ^^^"
            F"\n<<< {defs.readable_bot_name} will DM message author with the content set in parentheses () at time (24-hour clock), HH/MM stands for hours and minutes, e.g., 22:00 for 10:00 PM, etc. <<<"
            F"\n<<< y is an optional parameter and designates that this reminder will be recurring, i.e., every day at the hour set by the message author.<<<"
            F"\n<<< You may, if you would like, pass a date, e.g., on 17/03/2021 <<<"
            f"\n^^^ {data.self_mention} remind me ('something here') at {hour} on dd/mm/YYYY ^^^"
            f"\n^^^ NB: If you would like to schedule a time for tomorrow: ^^^"
            f"\n^^^ If at a time later than the current hour (if there is an interval greater than 24 hours), e.g., 5PM tomorrow when the current time is 4PM^^^"
            f"\n^^^ You MUST pass a date. e.g., at 17:00 on 18/03/2021 ^^^"
            f"\n^^^ If at a time earlier than the current hour (if there is an interval less than 24 hours), e.g., 3PM tomorrow when the current time is 4PM^^^"
            f"\n^^^ You MUST NOT pass a date. e.g., at 15:00 ^^^"
            f"\n^^^ NB: It is assumed that the user will schedule a time for today (if later than current hour), if no date is passed. ^^^"








            
            f"\n^^^ {data.self_mention} canceltask (Task-Name) ^^^"
            f"\n<<< When the recurring flag is set by the message author, {defs.readable_bot_name} will DM them and send the name of the task created by this flag., i.e., the recurring reminder. To cancel the reminder, to stop it from recurring, the author must invoke the above command in a channel. <<<"
            f"\n <<< The name of the task will always be something to the effect of, 'Task-Number'. <<<"
            
            )
    return content
