# embedded-systems-and-networking-assignment

Our repo for the Embedded Systemns and Networking assignment

A friendly note to install git on you computer: then write
```powershell
git config set --global user.name "YOUR NAME"
git config set --global user.email "YOUR EMAIL"
# Now we install the github cli to easily authenticate
winget install --id GitHub.cli
# Reboot the console, just close and reopen the app
gh auth login
```


Just one more thing...

set up a python virtual environment and install the requirements

```powershell
python -m venv .\venv # This creates a virtual environment, it helps keep our site packages clean. you can replace .\venv with any directory

.\venv\Scripts\activate\ # This tells the command line 'hey, we're working in the virtual environment now

pip install -r requirements.txt --target typings # This installs all the packages listed in environment.txt

deactivate #This tells the command line we are no longer working in the virtual environment
```
