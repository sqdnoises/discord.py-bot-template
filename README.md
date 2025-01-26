<div align="center">

# discord.py bot template

[![](https://img.shields.io/badge/Python-3.10+-FFD43B?labelColor=306998&style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/License-MIT-009900?style=for-the-badge&labelColor=111111)](LICENSE)

a discord.py bot template that I use for my bots.\
you're free to use this template if you like.

## License
You must have received a copy of the [<kbd> LICENSE </kbd>](LICENSE) file with this source code.\
This source code is licensed under the **MIT License**.

</div>

## Setup
**Python 3.10+** should work for this bot. However it is recommended to use any **Python 3.12** version.

> [!NOTE]
> In this section, `python3` would be `python` or just `py` on **Windows** platform.

### clone repo
First of all, git clone this repository:
```bash
git clone git@github.com:sqdnoises/discord.py-bot-template.git      # SSH
git clone https://github.com/sqdnoises/discord.py-bot-template.git  # HTTPS
```

### reinitialize git
Then reinitialize git `.git` (optional, do this if you are starting a new project)
```bash
rm -rf .git  # Linux
git init
git branch -M main
```

#### set remote
Set the remote aswell while you are reinitializing git for a new project.
```bash
git remote add origin git@github.com:user/repo.git      # SSH
git remote add origin https://github.com/user/repo.git  # HTTPS
```

Make sure to replace `user` with your GitHub username and `repo` with your repository name.

### create a `.env` file
`.env` template
```python
TOKEN="discord bot token"
```

This file contains secret environmental variables that are not meant to be shared with anyone.
The bot uses the `TOKEN` variable to login into the Discord bot.

### venv (For Linux)
On `bash`:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### venv (For Windows, optional but highly recommended)
On `powershell`:
```powershell
py -m venv .venv
& .\.venv\Scripts\activate
```

### install requirements
```bash
pip install -r requirements.txt
```

### setup the database
```bash
cd src
prisma db push
```

### setup config
Open [`src/config.py`](src/config.py) in the editor of your choice and edit the config variables as needed.

Make sure you update `ADMINS` and `LOG_CHANNEL` to the appropriate values.

### running
```bash
source .venv/bin/activate  # For Linux
# OR
& .\.venv\Scripts\activate  # For Windows (optional)

cd src
python3 bot.py  # py or python bot.py on Windows
```

### post-run
Since the bot's profile has been set up for the first time, you need to tell Discord that your bot has slash commands.
For this you need to use `!sync` only once after running the bot for the first time in the server it's in.

This will synchronise all the slash commands in the code on Discord. Please restart your Discord after this step to reload all the slash command data and show the bot's slash commands when you start typing with `/`.

## `/ping` command issues on a Linux host
If you host the bot on linux and use the `/ping` command, you will likely see the bot think forever or produce an error and see an `Permission Error` error in the console.
Linux uses a kernel parameter that restricts who can create ping sockets.

For troubleshooting, please refer to: [<kbd> kyan001/ping3/TROUBLESHOOTING.md </kbd>](https://github.com/kyan001/ping3/blob/master/TROUBLESHOOTING.md)
