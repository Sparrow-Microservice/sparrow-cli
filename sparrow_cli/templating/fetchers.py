from __future__ import annotations
from pathlib import Path
import urllib.request
import tarfile

from typing import (
    Any,
    Optional)
from tempfile import TemporaryDirectory

from sparrow_cli.consoles import console

TEMPLATE_URL: str = "https://github.com/Sparrow-Microservice/sparrow-templates/releases/download"
TEMPLATE_VERSION: str = "v0.1.0"


class TemplateFetcher:
    def __init__(self, uri: str, metadata: Optional[dict[str, Any]] = None):
        if metadata is None:
            metadata = dict()
        self.uri = uri
        self.metadata = metadata
        self._tmp = None

    @classmethod
    def from_name(cls, name: str, version: str = TEMPLATE_VERSION) -> TemplateFetcher:
        """Build a new instance from name and version.

        :param name: The name of the template.
        :param version: The version of the template.
        :return: A ``TemplateFetcher`` instance.
        """
        registry = f"{TEMPLATE_URL}/{version}"
        url = f"{registry}/{name}.tar.gz"
        metadata = {"template_registry": registry, "template_version": version, "template_name": name}
        return cls(url, metadata)

    @staticmethod
    def fetch_tar(url: str, path: str) -> None:
        """
        Fetch a tar file from a url and extract it to a path.

        :param url: The url of the tar file.
        :param path: The path where to extract the tar file.
        :return: None
        """
        with console.status(f"Downloading template from {url!r}...", spinner="moon"):
            stream = urllib.request.urlopen(url)
        console.print(f":moon: Downloaded template from {url!r}\n")

        tar = tarfile.open(fileobj=stream, mode="r|gz")
        with console.status(f"Extracting template into {path!r}...", spinner="moon"):
            tar.extractall(path=path)
        console.print(f":moon: Extracted template into {path!r}\n")

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.uri!r}, {self.metadata!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.uri == other.uri and self.metadata == other.metadata

    @property
    def path(self) -> Path:
        """ Get the local path of the template.
        :return: A ``Path`` instance.
        """
        return Path(self.tmp.name)

    @property
    def tmp(self) -> TemporaryDirectory:
        """ Get the temporal directory in which the template is downloaded.

        :return: A ``TemporaryDirectory`` instance.
        """
        if self._tmp is None:
            cache_dir = Path.home() / ".sparrow" / "tmp"
            cache_dir.mkdir(parents=True, exist_ok=True)
            tmp = TemporaryDirectory(dir=str(cache_dir))
            self.fetch_tar(self.uri, tmp.name)
            self._tmp = tmp
        return self._tmp
