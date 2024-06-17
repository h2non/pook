import asyncio
from typing import Optional, Tuple

import pytest

import pook


class StandardTests:
    is_async: bool = False

    async def amake_request(self, method: str, url: str) -> Tuple[int, Optional[str]]:
        raise NotImplementedError(
            "Sub-classes for async transports must implement `amake_request`"
        )

    def make_request(self, method: str, url: str) -> Tuple[int, Optional[str]]:
        if self.is_async:
            return self.loop.run_until_complete(self.amake_request(method, url))

        raise NotImplementedError("Sub-classes must implement `make_request`")

    @pytest.fixture(autouse=True, scope="class")
    def _loop(self, request):
        if self.is_async:
            request.cls.loop = asyncio.new_event_loop()
            yield
            request.cls.loop.close()
        else:
            yield

    @pytest.mark.pook
    def test_activate_deactivate(self, httpbin):
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body("hello from pook")

        status, body = self.make_request("GET", url)

        assert status == 200
        assert body == "hello from pook"

        pook.disable()

        status, body = self.make_request("GET", url)

        assert status == 404

    @pytest.mark.pook(allow_pending_mocks=True)
    def test_network_mode(self, httpbin):
        upstream_url = f"{httpbin.url}/status/500"
        mocked_url = f"{httpbin.url}/status/404"
        pook.get(mocked_url).reply(200).body("hello from pook")
        pook.enable_network()

        # Avoid matching the mocks
        status, body = self.make_request("POST", upstream_url)

        assert status == 500
