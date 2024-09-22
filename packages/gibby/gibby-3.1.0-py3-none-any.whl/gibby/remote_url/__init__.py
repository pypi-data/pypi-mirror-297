from __future__ import annotations

import os
import urllib.parse
from pathlib import Path

from .file_remote_url import FileRemoteUrl
from .remote_url import RemoteUrl

__all__ = [
    "parse",
    "RemoteUrl",
    "FileRemoteUrl",
]
_KNOWN_SCHEMES: dict[str, type[RemoteUrl]] = {"file": FileRemoteUrl}


def parse(url_string: str) -> RemoteUrl:
    try:
        scheme_end_index = url_string.index(
            "://"
        )  # The // is technically optional according to the URI spec, but we need to support Windows paths that contain ':' (C:/Foo)
        scheme = url_string[:scheme_end_index]
    except ValueError:  # No explicit scheme
        canon_local_path = str(Path(url_string).absolute()).replace(os.sep, "/")
        url_string = "file:///" + urllib.parse.quote(canon_local_path)
        scheme = "file"

    if scheme in _KNOWN_SCHEMES:
        return _KNOWN_SCHEMES[scheme](url_string)
    else:
        raise ValueError(f"Unsupported scheme '{scheme}'.")
