#################
# Configuration #
#################

# Explanation of how to set values
# Text            -> "something" (must be under single or double quotes)
# Numbers         -> 1234, 12.34 (can also be negative)
# True/False      -> True, False (for on/off scenarios)
# List of text    -> ["A", "BC"] (must be under square brackets and comma separated)
# List of numbers -> [1, 2, 3.4] (must be under square brackets and comma separated)
# No value        -> None

##################################
# Explanations of all the values #
##################################

# BOT_NAME               - The bot name, only used to show in logs.
# DATABASE_LOCATION      - The location of the database file, only used to show in logs.
BOT_NAME = "template bot"
DATABASE_LOCATION = "./database/database.db"

# DEFAULT_PREFIX         - This can be the default prefix the bot will assign to a server when it
#                          detects its in a new server.
# MENTION_IS_ALSO_PREFIX - You can also @mention the bot as a prefix, for example `@mention help`
#                          would do the same thing as `!help`.
# ADMINS                 - A comma seperated list of Discord user IDs who will have admin control
#                          of the bot (access to developer cog).
# DEBUG                  - Debug mode, useful for printing more information and receiving debug
#                          messages in the logs channel. Mostly used for debugging purposes to
#                          fix a bug by providing more information on why something might not be
#                          working.
DEFAULT_PREFIX = "!"
MENTION_IS_ALSO_PREFIX = True
ADMINS = [1077982815070728223]
DEBUG = True

# NOTIFY_ALL_ERRORS_TO_USER - Whether to send an embed to the user with an error for all kinds of
#                             unhandled errors when an app command fails.
#                             (slash commands, context menu, buttons, etc.)
# LOG_CHANNEL               - A channel ID which the bot has access to so it can send bot logs.
# NOTE: LOG_CHANNEL can be set to None to disable it.
LOG_CHANNEL = 1318631693929680896
NOTIFY_ALL_ERRORS_TO_USER = True

# SAVE_CUSTOM_LOGS      - Whether to save the logs produced by the custom logger.
# SAVE_DISCORD_LOGS     - Whether to save the logs produced by the discord.py logger.
# LOGGER_FLUSH_ON_PRINT - Save file contents as logger prints. 
# Save path: ./logs/<bot name> <time>.log
SAVE_CUSTOM_LOGS = True
SAVE_DISCORD_LOGS = True
LOGGER_FLUSH_ON_PRINT = False

# LOG_COMMANDS_TO_CONSOLE           - Log every text and slash command being used by a user to
#                                     console.
# LOG_NOT_FOUND_COMMANDS_TO_CONSOLE - Log every text command that users try to use but do not
#                                     exist to console.
LOG_COMMANDS_TO_CONSOLE = True
LOG_NOT_FOUND_COMMANDS_TO_CONSOLE = True

# MISSING_ARGUMENT_MESSAGE   - The message sent when a user tries to use a command without
#                              providing the required arguments.
# NO_PERMISSIONS_MESSAGE     - The message sent when a user tries to use a command they don't
#                              have permissions for.
# BOT_NO_PERMISSIONS_MESSAGE - The message sent when the bot lacks the necessary permissions to
#                              execute a command. 
# COMMAND_NOT_FOUND_MESSAGE  - The message sent when a user tries to use a text command that does
#                              not exist.
# \n is a newline.
# The value can be set to None (without the quotes) to disable it.
MISSING_ARGUMENT_MESSAGE = "Missing argument `{argument}` of type `{type}`.\nFor more information refer to `{clean_prefix}help {command.qualified_name}`."
NO_PERMISSIONS_MESSAGE = "You don't have permissions to use this command."
BOT_NO_PERMISSIONS_MESSAGE = ("I'm missing permissions to run this command.\n"
                              "Permissions required: {joined_permissions_code}")
COMMAND_NOT_FOUND_MESSAGE = "Command `{ctx.clean_prefix}{command}` not found."

# ITEMS_PER_PAGE - The amount of items to show in any sort of command with multiple pages.
ITEMS_PER_PAGE = 5

# LOGGER_TIME_FORMAT        - Time format in to show in the logger.
# LOG_FILE_NAME_TIME_FORMAT - Time format to save files in.
LOGGER_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_NAME_TIME_FORMAT = "%Y-%m-%d %H-%M-%S"

# COGS_EXCLUDE - Comma seperated list of cogs to exclude on runtime.
# Example: ["developer", "test"]
# The example excludes developer.py and test.py cog from loading on bot startup.
COGS_EXCLUDE = ["template"]