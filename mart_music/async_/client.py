"""
Client for use in async applications
"""

# Stdlib
from io import BytesIO
from typing import List, Tuple
from urllib.parse import quote

# External Libraries
from aiohttp import ClientSession

# Library internal code
from mart_music.common import Song, _parse_songs
from mart_music.ratelimits import RatelimitHandler


class MusicClient:
    """
    Interfaces with the api using async functions
    """

    ROOT = "https://music.martmists.com"

    def __init__(self, token: str):
        self.ratelimiter_search = RatelimitHandler(token)
        self.ratelimiter_download = RatelimitHandler(token)
        self.session = ClientSession(headers={"API-KEY": token})

    async def search(self, query: str) -> List[Song]:
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

        await self.ratelimiter_search.wait_async()

        async with self.session.get(self.ROOT + "/api/search/" +
                                    quote(query)) as response:
            data = await response.json()

        return _parse_songs(data)

    async def download(self, song: Song) -> Tuple[BytesIO, bool]:
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

        await self.ratelimiter_download.wait_async()

        effective_url = self.ROOT + song.path if song.downloadable else song.url

        async with self.session.get(effective_url) as response:
            raw_bytes = await response.read()

        return BytesIO(raw_bytes), song.downloadable
