# --- Bot name and token ---
# bot_token1: str = ""
# bot_token2: str = ""
readable_bot_name: str = "roberta"  # should be lower case

# --- Reaction emojis ---
reaction_yes: str = "⭕"
reaction_no: str = "❌"

# --- Times in seconds (floats can be fractions) ---
temp_check_delay: float = 2  # (seconds between each check on temp bans/mutes and warnings)
creed_cooldown_delay: float = 60 * 5  # How many seconds to calm down one point on the creed irritation meter
ban_message_wait: float = 5
kick_message_wait: float = 2
simp_mute_time: int = 30

# --- Other config values ---
max_delete = 100  # amount of messages to be deleted on "clear all".

# --- Admin function messages ---
# '{mention}' will be replaced with a mention to the target of the ban/kick/warn
temp_ban_message: str = "Clearly you are unfit for this establishment, {mention}."
post_temp_ban_message: str = "Let's hope your time in the corner changes that."  # No {mention} on this one
ban_message: str = "I see you have returned and, much to my dismay, have not changed. Let's fix that. {mention}."
post_ban_message: str = "Good riddance"  # No {mention} on this one

kick_message: str = "You are no longer welcome here.\nI will show {mention} the door."

# This will be the warning message if none is specified
default_warn_message: str = "{mention}, you've been warned!"

# Reaction role messages will start with this
reaction_role_message: str = "React with the proper emoji to get a role!"

# --- Other messages ---
# When someone mentions her without activating any commands
thats_me: str = "May I help you?"
# Sent when someone asks about their own warnings but has none
no_warning_message: str = "Congratulations, you have no warnings!"

owoifying_message: str = "I will owoify this channel!"
not_owoifying_message: str = "I will not owoify this channel  anymore!"

# Help messages
help_question: str = "Do you need this maid to clean up after your mess....again?"
# When a user chooses 'yes' after asking for help
help_yes: str = "As you wish, try not to mess up or forget the commands again {mention}."
# When a user chooses 'no' after asking for help
help_no: str = "Then why did you ask for help if you don't need it?\n**Glare**"
incoming_help: str = "INCOMING!!!"
incoming_img: str = "https://tenor.com/view/fail-hurricane-ocean-funny-boat-gif-18563156"

# --- Images ---
simp_images = [
    "https://imgur.com/M5ZSx1y",
    "https://imgur.com/exr3LM4",
    "https://imgur.com/ohdYpqu"
]

tea_images = [
    "https://imgur.com/t1Yd5Fq",
    "https://imgur.com/hBnzZT4",
    "https://imgur.com/rgGixO6",
    "https://imgur.com/rdkACwV",
    "https://imgur.com/uOc8ZSQ"
]

tea_syke_images = [
    "https://imgur.com/vNAFFId"
]

# --- Mute roles ---
# In the format "serverID : roleID"
mute_roles = {
    # For example:
    758169654887448587: 758173421929627670,
    703197406816370698: 759852272246587403

    # 999888777: 321654987
}
