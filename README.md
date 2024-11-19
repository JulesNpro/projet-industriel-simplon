# Installation 

**Virtual environnement**
```powershell
python -m venv .venv
```
> .venv is the name of the virtual environnement 

**Connect to the venv** 

- mac/linux
`source .venv/bin/activate.fish`
- windows
`.venv/Scripts/activate` or `.venv/Scripts/activate.ps1` 

**create requirements.txt from pip**
`pip freeze > requirements.txt`

in a new environnement install the librairies
**install librairies**.
`pip install -r requirements.txt`

**quit venv**
`deactivate` 