"""
Ratelimit handler for the service.
"""

# Stdlib
import asyncio
from time import sleep, monotonic
from typing import Tuple

RATES_PER_SECOND = {"T1": 1, "T2": 4, "T3": 10}

RATES_PER_MINUTE = {"T1": 30, "T2": 120, "T3": 300}


class RatelimitHandler:
    """
    Handler class, should be instantiated for every route
    """

    def __init__(self, token: str):
        tier = token[:2]
        self.per_second = RATES_PER_SECOND[tier]
        self.per_minute = RATES_PER_MINUTE[tier]

        self.amount_calls_second = 0
        self.amount_calls_minute = 0
        self.last_reset_second = self.time()
        self.last_reset_minute = self.time()

    @staticmethod
    def time():
        """Returns the current time"""
        return monotonic()

    def time_remaining_second(self):
        """Returns the time remaining in seconds"""
        time_passed = self.time() - self.last_reset_second
        return self.per_second - time_passed

    def time_remaining_minute(self):
        """Returns the time remaining in seconds"""
        time_passed = self.time() - self.last_reset_minute
        return self.per_minute - time_passed

    def hitting_second_ratelimit(self) -> Tuple[bool, float]:
        """Returns whether it's ratelimited and a float of how long to sleep for"""
        wait_time = self.time_remaining_second()

        if wait_time <= 0:
            self.amount_calls_second = 0
            self.last_reset_second = self.time()

        self.amount_calls_second += 1

        if self.amount_calls_second > self.per_second:
            return True, wait_time

        return False, 0

    def hitting_minute_ratelimit(self) -> Tuple[bool, float]:
        """Returns whether it's ratelimited and a float of how long to sleep for"""
        wait_time = self.time_remaining_minute()

        if wait_time <= 0:
            self.amount_calls_minute = 0
            self.last_reset_minute = self.time()

        self.amount_calls_minute += 1

        if self.amount_calls_minute > self.per_minute:
            return True, wait_time

        return False, 0

    def hitting_ratelimit(self) -> Tuple[bool, float]:
        """Checks both second and minute ratelimit"""
        ratelimited, time_left = self.hitting_second_ratelimit()
        if not ratelimited:
            ratelimited, time_left = self.hitting_minute_ratelimit()

        return ratelimited, time_left

    def wait(self):
        """Waits sync"""
        ratelimited, time = self.hitting_ratelimit()
        if ratelimited:
            sleep(time)

    async def wait_async(self):
        """Waits async"""
        ratelimited, time = self.hitting_ratelimit()
        if ratelimited:
            await asyncio.sleep(time)
