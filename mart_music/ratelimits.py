import asyncio
from time import monotonic, sleep
from typing import Tuple

RATES_PER_SECOND = {
    "T1": 1,
    "T2": 4,
    "T3": 10
}

RATES_PER_MINUTE = {
    "T1": 30,
    "T2": 120,
    "T3": 300
}


class RatelimitHandler:
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
        return monotonic()

    def time_remaining(self, mode: str):
        time_passed = self.time() - self.last_reset
        return getattr(self, mode) - time_passed

    def hitting_ratelimit(self) -> Tuple[bool, float]:
        for mode in ("second", "minute"):
            wait_time = self.time_remaining("per_" + mode)

            if wait_time <= 0:
                setattr(self, "amount_calls_" + mode, 0)
                setattr(self, "last_reset_" + mode, self.time())

            setattr(self, "amount_calls_" + mode, getattr(self, "amount_calls_" + mode) + 1)

            if getattr(self, "amount_calls_" + mode) > getattr(self, "per_" + mode):
                return True, wait_time

        return False, 0

    def wait(self):
        ratelimited, time = self.hitting_ratelimit()
        if ratelimited:
            sleep(time)

    async def wait_async(self):
        ratelimited, time = self.hitting_ratelimit()
        if ratelimited:
            await asyncio.sleep(time)
