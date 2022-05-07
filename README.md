# get_latest_proton_ge
Python script to snag the latest proton GE

This script will download the latest Proton-GE and install it in `$HOME/.steam/steam/compatibilitytools.d/`
You will need to restart your Steam client to see the new version there.

## Usage
``` bash
poetry update
poetry run python main.py
```

## Rate limited
If for some reason you are re-running this over and over, you can get rate limited by the Github API.
Just export your access token (it doesn't need any permissions set) prior to running the script.

``` bash
export GH_TOKEN=<yourgithubtokenhere>
```
