import os
import tarfile
from collections import namedtuple

import requests

Release = namedtuple("Release", ["name", "download_link"])

# export your GitHub token for usage here
GH_TOKEN = os.getenv("GH_TOKEN")
HEADER = {"Authorization": f"token {GH_TOKEN}"}

req = requests.Session()
# If a token is passed in you won't get rate limited if you rerun this a bunch
if GH_TOKEN:
    req.headers.update(HEADER)


def get_tarball_link(asset_list):
    for i in asset_list.json():
        if "application/gzip" in i["content_type"]:
            print(f"Found download link: {i['browser_download_url']}")
            return i["browser_download_url"]
    return ""


def get_release_list(github_release_api_url: str):
    print(f"Fetching release list from {github_release_api_url}")
    r = req.get(github_release_api_url)
    release_list = []
    for i in r.json():
        assets_url = req.get(i["assets_url"])
        name = i["name"]
        release_list.append(Release(name, get_tarball_link(assets_url)))
    return release_list


def download_release(release):
    print(f"Downloading {release.name}")
    dl_req = req.get(release.download_link)
    with open(f"{release.name}.tar.gz", "wb") as f:
        f.write(dl_req.content)


def extract_release(release):
    print(f"Extracting {release.name}")
    homedir = os.path.expanduser("~")
    steam_path = os.path.join(homedir, ".steam/steam/compatibilitytools.d")
    tar = tarfile.open(f"{release.name}.tar.gz", "r:gz")
    tar.extractall(path=steam_path)
    tar.close()


def cleanup(release):
    print(f"Cleaning up {release.name}")
    os.remove(f"{release.name}.tar.gz")


if __name__ == "__main__":
    USERNAME = "GloriousEggroll"
    REPONAME = "proton-ge-custom"
    GH_R_API = f"https://api.github.com/repos/{USERNAME}/{REPONAME}/releases"

    release_list = get_release_list(GH_R_API)

    selected_release = release_list[0]
    download_release(selected_release)
    extract_release(selected_release)
    cleanup(selected_release)
