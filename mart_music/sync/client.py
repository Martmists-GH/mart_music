"""
Client for use in async applications
"""

# Stdlib
from io import BytesIO
from typing import List, Tuple
from urllib.parse import quote

# External Libraries
from requests import Session

# Library internal code
from mart_music.common import Song, _parse_songs
from mart_music.ratelimits import RatelimitHandler


class MusicClient:
    """
    Interfaces with the api using sync functions
    """

    ROOT = "https://music.martmists.com"

    def __init__(self, token: str):
        self.ratelimiter_search = RatelimitHandler(token)
        self.ratelimiter_download = RatelimitHandler(token)
        self.headers = {"API-KEY": token}
        self.session = Session()

    def search(self, query: str) -> List[Song]:
        """
        Searches the API for the given query

        Parameters
        -----------
        query : str
            The query to search for.

        Returns
        --------
        List[:class:`Song`]:
            The songs returned by the API.
        """

        self.ratelimiter_search.wait()

        with self.session.get(
                self.ROOT + "/api/search/" + quote(query),
                headers=self.headers) as response:
            data = response.json()

        return _parse_songs(data)

    def download(self, song: Song) -> Tuple[BytesIO, bool]:
        """
        Downloads a song from the API

        Parameters
        -----------
        song : :class:`Song`
            The :class:`Song` object to download.

        Returns
        --------
        Tuple[:class:`BytesIO`, bool]:
            A :class:`BytesIO` containing the data and a bool denoting whether this is opus or not.
        """

        self.ratelimiter_download.wait()

        effective_url = self.ROOT + song.path if song.downloadable else song.url

        with self.session.get(effective_url, headers=self.headers) as response:
            raw_bytes = response.content

        return BytesIO(raw_bytes), song.downloadable
