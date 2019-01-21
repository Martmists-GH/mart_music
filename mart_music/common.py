from typing import List, Union, Dict, Any


class APIException(Exception):
    """
    Exception thrown when the API did not respond with a success status code.
    """
    pass


class Song:
    """
    A class containing all information a song from the API contains

    Attributes
    -----------
    title: str
        The song title.

    artist: str
        The artist of the song.

    path: str
        The path on the API to download this song.

    downloadable: bool
        A boolean denoting whether this song can be downloaded from the API or not.

    url: Union[str, None]
        A string holding the raw url if downloadable is False.

    source: str
        The source website.

    info: Union[Dict[str, Any], None]
        Additional information on a song, if available.
    """

    def __init__(self,
                 title: str, artist: str, dl_path: str,
                 downloadable: bool, source: str,
                 url: Union[str, None] = None,
                 info: Union[Dict[str, Any], None] = None):
        self.title = title
        self.artist = artist
        self.path = dl_path
        self.downloadable = downloadable
        self.url = url
        self.source = source
        self.info = info


def _parse_songs(data: Dict[str, Any]) -> List[Song]:
    if not data["success"]:
        raise APIException(data["error"])

    songs = [Song(**item) for item in data["result"]]
    return songs
