from __future__ import annotations

import requests

from framex._dicts._constants import _EXTENSION

# GitHub API URL for the directory contents
_API_URL = "https://api.github.com/repos/Zaf4/datasets/contents/feather"


def _get_names(api_url: str) -> dict[str, str]:
    """
    Get the names of the datasets from the GitHub API.

    Parameters
    ----------
    api_url : str
        The URL of the GitHub API.

    Returns
    -------
    list of str
        The names of the datasets.
    """
    response = requests.get(api_url)
    files = response.json()

    # Extract .feather files
    datasets = {
        file["name"].rstrip(_EXTENSION): file["download_url"]
        for file in files
        if file["name"].endswith(_EXTENSION)
    }

    return datasets


_GITHUB_DATASETS = _get_names(_API_URL)
