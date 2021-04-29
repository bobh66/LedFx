import logging
from json import JSONDecodeError

from aiohttp import web

from ledfx.api import RestEndpoint
from ledfx.config import save_config

_LOGGER = logging.getLogger(__name__)


class VirtualsEndpoint(RestEndpoint):

    ENDPOINT_PATH = "/api/virtuals"

    async def get(self) -> web.Response:
        response = {
            "virtuals": {
                "blade": True,
                "list": self._ledfx.config["virtuals"],
            },
        }

        return web.json_response(data=response, status=200)

    async def post(self, request) -> web.Response:
        try:
            data = await request.json()
        except JSONDecodeError:
            response = {
                "status": "failed",
                "reason": "JSON Decoding failed",
            }
            return web.json_response(data=response, status=400)

        virtuals = data.get("virtuals")
        if virtuals is None:
            response = {
                "status": "failed",
                "reason": 'Required attribute "virtuals" was not provided',
            }
            return web.json_response(data=response, status=400)

        virtuals_list = virtuals["list"]

        _LOGGER.info(f"Adding virtuals list to config: {virtuals_list}")

        # Update and save the configuration
        self._ledfx.config["virtuals"] = virtuals_list

        save_config(
            config=self._ledfx.config,
            config_dir=self._ledfx.config_dir,
        )

        response = {
            "status": "success",
        }

        return web.json_response(data=response, status=200)