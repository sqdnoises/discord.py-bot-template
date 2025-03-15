<div align="center">

# discord.py bot template

[![](https://img.shields.io/badge/Python-3.10+-FFD43B?labelColor=306998&style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/License-MIT-009900?style=for-the-badge&labelColor=111111)](LICENSE)
[![](https://img.shields.io/badge/code_style-black-000000?style=for-the-badge&labelColor=FFFFFF)](https://github.com/psf/black)

a discord.py bot template that I use for my bots.\
you're free to use this template if you like.

</div>

## License [![](https://img.shields.io/badge/MIT-009900)](LICENSE)
You should have received a copy of the [<kbd> LICENSE </kbd>](LICENSE) file with this source code.\
This source code is licensed under the **MIT License**.

## Setup dev environment
> [!NOTE]
> **Python 3.10+** should work with this bot. However it is recommended to use the latest **Python 3.13** version.

---

## Visual Studio Code extensions [<sub><sub>skip?</sub></sub>](#setting-up-a-new-project-skip)
This bot was created, developed and meant to be used with the [**Visual Studio Code**](https://code.visualstudio.com/) IDE. I have listed the recommended extensions for this bot to be used with Visual Studio Code below.

### 1. recommended Visual Studio Code extensions for this template
- autoDocstring (by Nils Werner)
- Better Color Picker (by Jannchie)
- Black Formatter (by Microsoft)
- Error lens (by Alexander)
- GitHub Markdown Preview <sub>[Extension Pack]</sub> (by Matt Bierner)
  1. Markdown Preview GitHub Styling (by Matt Bierner)
  2. Markdown Emoji (by Matt Bierner)
  3. Markdown Checkboxes (by Matt Bierner)
  4. Markdown yaml Preamble (by Matt Bierner)
  5. Markdown Footnotes (by Matt Bierner)
  6. Markdown Preview Mermaid Support (by Matt Bierner)
- Local History (by xyz)
- Prisma (by Prisma)
- Pylance (by Microsoft)
- Python (by Microsoft)
- Python Debugger (by Microsoft)
- Python Environments (by Microsoft)
- Python Indent (by Kevin Rose)
- SQLite3 Editor (by yy0931)

#### 2. other extensions I use
- :emojisense: (by Matt Bierner)
- AmazonQ (by Amazon Web Services)
- Even Better TOML (by tamasfe)
- Hex Editor (by Microsoft)
- Live Share (by Microsoft)
- Rainbow CSV (by mechatroner)
- Remote - SSH (by Microsoft)

#### 3. customization
- Discord Rich Presence (by leonardssh)
- Material Icon Theme (by Philipp Kief)
- One Dark Pro (by binaryify) (I use this rarely)
- Vitesse Theme (Anthony Fu) (I use this one the most)

---

## Setting up a new project [<sub><sub>skip?</sub></sub>](#setting-up--running-the-bot)

### clone repo
First of all, git clone this repository:
```bash
git clone git@github.com:sqdnoises/discord.py-bot-template.git      # SSH
git clone https://github.com/sqdnoises/discord.py-bot-template.git  # HTTPS
```

### setup your repo
Then reinitialize git `.git` (recommended to do this if you are starting a new project)
```bash
rm -rf .git  # Linux
git init
git branch -M main
```

Set the remote for a new project.
```bash
git remote add origin git@github.com:user/repo.git      # SSH
git remote add origin https://github.com/user/repo.git  # HTTPS
```

Make sure to replace `user` with your GitHub username and `repo` with your repository name.

---

## Setting up & running the bot

### create a `.env` file
`.env` template
```python
TOKEN="discord bot token"
```

This file contains secret environmental variables that are not meant to be shared with anyone.

The bot uses the `TOKEN` variable to login into the Discord bot.

### install uv
[Installation instructions here](https://github.com/astral-sh/uv#installation)\
<sub>(tl;dr: you can use `pip install uv`)</sub>

### install python 3.13
```console
$ uv python install 3.13
Searching for Python versions matching: Python 3.13
Installed 1 version in 3.13s
 + cpython-3.13.2-windows-x86_64-none
```

### create a venv
```console
$ uv venv
Using CPython 3.13.2
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Run the shown venv activation command after the command is executed.

### install requirements
```console
$ uv pip install -r requirements.txt
Resolved 44 packages in 5.11s
Prepared 44 packages in 1m 50s
Installed 44 packages in 81ms
 + aiohappyeyeballs==2.6.1
 + aiohttp==3.11.13
...
```

### setup the database
```console
$ prisma db push
Environment variables loaded from .env
Prisma schema loaded from prisma\schema.prisma
Datasource "db": SQLite database "database.db" at "file:../database/database.db"

SQLite database database.db created at file:../database/database.db

Your database is now in sync with your Prisma schema. Done in 57ms

✔ Generated Prisma Client Python (v0.15.0) to .venv/lib/site-packages/prisma in 394ms
```

### setup config
Open [`src/config.py`](src/config.py) in the editor of your choice and edit the config variables as needed.

Make sure you update `ADMINS` and `LOG_CHANNEL` to the appropriate values.

### running
make sure your venv is activated and run:
```bash
python3 -m src  # py -m src/python -m src on Windows
```

### post-run
Since the bot's profile has been set up for the first time, you need to tell Discord that your bot has slash commands.\
For this you need to use `!sync` in a server the bot is in after running the bot for the first time.

This will synchronise all the slash commands in the code on Discord. Please restart your Discord app after this step to refetch all slash commands and then it should show the bot's slash commands when you start typing with `/` in a server the bot is in or anywhere if installed as an user app.

---

## `/ping` command issues on a Linux host
If you host the bot on linux and use the `/ping` command, you will likely see the bot think forever or produce an error and see an `Permission Error` error in the console.
Linux uses a kernel parameter that restricts who can create ping sockets.

For troubleshooting, please refer to: [<kbd> kyan001/ping3/TROUBLESHOOTING.md </kbd>](https://github.com/kyan001/ping3/blob/master/TROUBLESHOOTING.md)

---

<sub>© 2023-present SqdNoises<br>
Licensed under the MIT License.</sub>
<div align="right"><sub><a href="#top">back to top ↑</a></sub></div>
