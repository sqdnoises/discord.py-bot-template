# Dependencies for the template

This template of a [`discord.py` <img src="https://raw.githubusercontent.com/Rapptz/discord.py/master/docs/images/discord_py_logo.ico" alt="discord.py" height="12">](https://github.com/Rapptz/discord.py) bot **REQUIRES** [`Python 3.10.x` <img src="https://python.org/favicon.ico" alt="Python" height="12"> or above](https://python.org/downloads).

The following requirements must be met before using this template:

- [**`Python 3.10.x` <img src="https://python.org/favicon.ico" alt="Python" height="12"> or above**](#installing-python)
- Python packages from [`requirements.txt`](requirements.txt) must be installed ([**Installing `pip` requirements**](#installing-pip-requirements))

You can click the hyperlinks above to see how to install the clicked dependency or you can see how to install them below.

# Installing dependencies
This section shows you how to install the dependencies listed above.

## Installing Python <img src="https://python.org/favicon.ico" alt="Python" height="18">
This section shows you how to install python on most platforms.

### On Windows 10 <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Windows_logo_-_2012_%28dark_blue%29.svg" alt="Windows 10" height="16">/11 <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" alt="Windows 11" height="16">
Head to [**Python downloads** <img src="https://python.org/favicon.ico" alt="Python" height="12">](https://python.org/downloads) and click the big yellow `Download Python 3.x.x` button.

![python.org downloads page](images/installing%20python/python.org%20downloads%20page.png)

An installer for the latest version of **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** must have been downloaded:

![python installer file downloaded](images/installing%20python/python%20installer%20file%20downloaded.png)

Open the download file and this window will pop up.

![python installer window](images/installing%20python/python%20installer%20window.png)

Make sure to check `Add python.exe to PATH`.

![add python.exe to path](images/installing%20python/add%20python.exe%20to%20path.png)
**NOTE:** *It is not neessary to check `Use admin privilages when installing py.exe` but if you do have admin privileges, it's recommended to use it.*

Wait for Python to install (might take a few minutes) and finally you will see this:

![python setup was successful](images/installing%20python/setup%20was%20successful.png)
**NOTE:** *If you see `DISABLE PATH LENGTH LIMIT` and you have administrator priviliges, it is highly advised you disable the path length limit.*

**Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> has been installed.**

#### Check if Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> was installed correctly
Open your start menu by pressing the **Start button (<img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Windows_logo_-_2012_%28dark_blue%29.svg" alt="Windows 10" height="12"> for Windows 10/ <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" alt="Windows 11" height="12"> for Windows 11)** on the bottom left corner of your screen or bottom middle of the screen if on Windows 11 <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" alt="Windows 11" height="12">.

If you are on Windows 11 <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" alt="Windows 11" height="12"> or if you have the `Windows Terminal` app installed, search `Terminal` in the start menu.
<br>
If you are on Windows 10 <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Windows_logo_-_2012_%28dark_blue%29.svg" alt="Windows 10" height="12"> and you don't have the `Windows Terminal` app installed, search for `Command Prompt` in the start menu.

![start menu terminal search](images/installing%20python/checking%20that%20python%20is%20installed/start%20menu%20terminal%20search.png)
**NOTE:** *Use `Command Prompt` if you're on Windows 10 <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Windows_logo_-_2012_%28dark_blue%29.svg" alt="Windows 10" height="12"> and don't have `Windows Terminal` instlled.*

A black box will appear just like this one:

![terminal window](images/installing%20python/checking%20that%20python%20is%20installed/terminal%20window.png)

Type the commands below in the `Terminal` or `Command Prompt` window and press enter to check `python`'s and Python's package manager `pip`'s version so we are sure that Python is installed correctly.

```
python -V
pip -V
```

It should show their versions like this:

![checking python and pip](images/installing%20python/checking%20that%20python%20is%20installed/checking%20python%20and%20pip.png)

If it does, Hurray! **You've installed Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> correctly.**

### On Linux <img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" alt="Linux Tux" height="16">
There's many ways to install Python on different platforms.

This tutorial only covers [**Ubuntu <img src="https://upload.wikimedia.org/wikipedia/commons/9/9e/UbuntuCoF.svg" alt="Ubuntu" height="12">/Debian <img src="https://www.debian.org/logos/openlogo-nd.svg" alt="Debian" height="12">**](#on-ubuntudebian-based-distros) based distros and [**Termux <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Termux.svg" alt="Termux" height="12">**](#on-termux).

If you use some other Linux distro, you can:
- Search for it online: [<img src="https://google.com/favicon.ico" alt="Google" height="12">](https://google.com) [<img src="https://Bing.com/favicon.ico" alt="Bing" height="12">](https://bing.com) [<img src="https://duckduckgo.com/favicon.ico" alt="DuckDuckGo" height="12">](https://duckduckgo.com) [<img src="https://yahoo.com/favicon.ico" alt="Yahoo" height="12">](https://yahoo.com) [<img src="https://yandex.com/favicon.ico" alt="Yandex" height="12">](https://yandex.com) (easier)
- Or look at the Python's official [**Using Python on Unix platforms**](https://docs.python.org/3/using/unix.html) page.

### On Ubuntu <img src="https://upload.wikimedia.org/wikipedia/commons/9/9e/UbuntuCoF.svg" alt="Ubuntu" height="16">/Debian <img src="https://www.debian.org/logos/openlogo-nd.svg" alt="Debian" height="16"> based distros
Unlike Windows, installing Python requires extra packages you need to install to be able to use `pip` and to be able to make virtual environments (`venv`).

Open a new **Terminal** and install **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** by using the following commands:
```
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

**Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> has been installed.**

#### Check if Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> was installed correctly
To check if **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** was installed correctly, run the following commands to check if **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** and `pip` prints their versions:
```
python3 -V
pip -V
```

If it does, Hurray! **You've installed Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> correctly.**

### On Termux <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Termux.svg" alt="Termux" height="16">
Unlike Windows, installing Python requires extra packages you need to install to be able to use `pip` and to be able to make virtual environments (`venv`).

Open **Termux <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Termux.svg" alt="Termux" height="12">** and install **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** by using the following commands:
```
apt update
apt install python python-pip python-venv -y
```

**Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> has been installed.**

#### Check if Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> was installed correctly
To check if **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** was installed correctly, run the following commands to check if **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** and `pip` prints their versions:
```
python3 -V
pip -V
```

If it does, Hurray! **You've installed Python <img src="https://python.org/favicon.ico" alt="Python" height="12"> correctly.**

## Installing `pip` requirements
Once **Python <img src="https://python.org/favicon.ico" alt="Python" height="12">** has been installed correctly, open a terminal in the current folder where the [`requirements.txt`](requirements.txt) file is located and run the following commnd:

```
pip install -r requirements.txt
```

All the `pip` package dependencies would be installed.

**NOTE (for Ubuntu <img src="https://upload.wikimedia.org/wikipedia/commons/9/9e/UbuntuCoF.svg" alt="Ubuntu" height="12">/Debian <img src="https://www.debian.org/logos/openlogo-nd.svg" alt="Debian" height="12"> users):** *If any package fails to install, try using `sudo apt install python3-packagename` where `packagename` is the name of the package that failed and try `pip install -r requirements.txt` again.*

**NOTE (for Termux <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Termux.svg" alt="Termux" height="12"> users):** *If any package fails to install, try using `apt install python-packagename` where `packagename` is the name of the package that failed and try `pip install -r requirements.txt` again.*
