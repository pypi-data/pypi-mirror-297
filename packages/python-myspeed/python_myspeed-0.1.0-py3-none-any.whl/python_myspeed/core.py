from __future__ import annotations

from typing import Any
from json import JSONDecodeError
import requests
import requests.packages

from python_myspeed.exceptions import (
    MySpeedAPIAuthenticationError,
    MySpeedAPIConnectionError,
    MySpeedAPIError,
    MySpeedAPIJSONDecodeError,
)
from python_myspeed import models

_INSTANCE = "{schema}://{host}:{port}/api"


class MySpeedAPI:
    """A class for interacting with a MySpeed instance."""

    def __init__(
        self,
        host: str,
        port: int,
        api_token: str | None = None,
        tls: bool = False,
        verify_tls: bool = True,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the connection to a Myspeed instance.

        Args:
            host (str): Hostname or ip address of the MySpeed instance.
            port (int): Port of the MySpeed instance.
            api_token (str | None, optional): API token to use. Defaults to None.
            tls (bool, optional): Use TLS (HTTPS) to connect to the MySpeed instance. Defaults to False.
            verify_tls (bool, optional): Verify the TLS certificate of the MySpeed instance. Defaults to True.
            session (requests.Session, optional): Preconfigured requests session. Defaults to None.
        """
        self._session = session or requests.Session()
        self.tls = tls
        self.verify_tls = verify_tls
        if not verify_tls:
            requests.packages.urllib3.disable_warnings()
        self.schema = "https" if self.tls else "http"
        self.host = host
        self.port = port
        self.api_token = api_token
        self.data = {}
        self.versions = {}
        self.base_url = _INSTANCE.format(
            schema=self.schema, host=self.host, port=self.port
        )

    @staticmethod
    def _verify_response_or_raise(response: requests.Response) -> None:
        """Verify that the response is valid.

        Args:
            response (requests.Response): The response to verify.
        """
        if response.status_code in (401, 403):
            msg = "Invalid API token"
            raise MySpeedAPIAuthenticationError(
                msg,
            )
        response.raise_for_status()

    def _get_url(self, endpoint: str, id: Any | None = None) -> str:
        """Get the full URL for the API endpoint.

        Args:
            endpoint (str): The endpoint to get the URL for.
            id (Any, optional): Id of the endpoint. Defaults to None.

        Returns:
            str: The full URL to the API endpoint.
        """
        return self.base_url + "/" + endpoint.lstrip("/") + (f"/{id}" if id is not None else "")

    def get_recommendations(self) -> models.Recommendations:
        """Get the current recommendations from the last 10 speed tests.

        Returns:
            models.Recommendations: The current recommendations.
        """
        return models.Recommendations(**self.get("recommendations").data)

    def get_version(self) -> models.Version:
        """Get the server version.

        Returns:
            models.Version: The server version.
        """
        return models.Version(**self.get("info/version").data)

    def get_servers(self, provider: str) -> list[models.Server]:
        """The all available servers of the given provider.

        Args:
            provider (str): The provider to get the available servers for.

        Returns:
            list[models.Server]: List of available servers.
        """
        response = self.get("info/server", provider)
        return [models.Server(id, name) for id, name in response.data.items()]

    def get_interface(self) -> models.Interface:
        """Get the interface used for the speed tests.

        Returns:
            models.Interface: The interface used for the speed tests.
        """
        return [
            models.Interface(name, ip_address)
            for name, ip_address in self.get("info/interfaces").data.items()
        ][0]

    def get_speedtest_statistics(self, days: int = 1) -> models.SpeedTestStatistics:
        """Get the speedtests statistics for a given number of days.

        Args:
            days (int, optional): The number of days which should be included in the statistics. Defaults to 1.

        Returns:
            models.SpeedTestStatistics: The speedtest statistics.
        """
        return models.SpeedTestStatistics(
            **self.get("speedtests/statistics", params={"days": days}).data
        )

    def get_speedtest_averages(
        self, days: int = 7
    ) -> list[models.SpeedTestAverageElement]:
        """Get the average speedtest results for a given number of days.

        Args:
            days (int, optional): The number of days which should be included in the average results. Defaults to 7.

        Returns:
            list[models.SpeedTestAverageElement]: A list of speedtest average results.
        """
        return [
            models.SpeedTestAverageElement(**item)
            for item in self.get("speedtests/averages", params={"days": days}).data[1:]
        ]

    def get_speedtest(self, speedtest_id: int) -> models.SpeedTest:
        """Get a single speedtest by it's id.

        Args:
            speedtest_id (int): The id of the speedtest.

        Returns:
            models.SpeedTest: The speedtest.
        """
        return models.SpeedTest(**self.get("speedtests", id=speedtest_id).data)

    def list_speedtests(
        self,
        hours: int | None = None,
        start: int | None = None,
        limit: int | None = None,
    ) -> list[models.SpeedTest]:
        """Get a list of speedtests.

        Args:
            hours (int | None, optional): The number of hours to go back. Defaults to None.
            start (int | None, optional): The id to start. Defaults to None.
            limit (int | None, optional): Limit the returned speedtests. Defaults to None.

        Returns:
            list[models.SpeedTest]: A list of multiple speedtests.
        """
        return [
            models.SpeedTest(**item)
            for item in self.get(
                "speedtests", params={"hours": hours, "start": start, "limit": limit}
            ).data
        ]

    def run_speedtest(self) -> str:
        """Run a single speedtest.

        Returns:
            str: The message returned from the server.
        """
        return self.post("speedtests/run").data.get("message")

    def pause_speedtest(self, resume_h: int = -1) -> str:
        """Pause the automated speedtests.

        Args:
            resume_h (int, optional): Resume the automated speedtests automatically after given hours. Defaults to -1 for infinite pause.

        Returns:
            str: The message returned from the server.
        """
        return self.post("speedtests/pause", data={"resumeIn": resume_h}).data.get(
            "message"
        )

    def continue_speedtest(self) -> str:
        """Resume with the automated speedtests.

        Returns:
            str: The message returned from the server.
        """
        return self.post("speedtests/continue").data.get("message")

    def delete_speedtest(self, speedtest_id: int) -> str:
        """Delete a single speedtest.

        Args:
            speedtest_id (int): The id of the speedtest to delete.

        Returns:
            str: The message returned from the server.
        """
        return self.delete("speedtests", id=speedtest_id).data.get("message")

    def get_config(self) -> models.Config:
        """Get the instance configuration.

        Returns:
            models.Config: The instance configuration.
        """
        return models.Config(**self.get("config").data)

    def set_config_key(self, key: str, value: Any) -> str:
        """Set a new value for a instance configuration key.

        Args:
            key (str): The instance configuration key to update.
            value (Any): The new value.

        Returns:
            str: The message returned from the server.
        """
        return self.patch("config", id=key, data={"value": value}).data.get("message")

    def get_speedtest_status(self) -> models.SpeedTestStatus:
        """Get the speedtest status.

        Returns:
            models.SpeedTestStatus: The speedtest status.
        """
        return models.SpeedTestStatus(**self.get("speedtests/status").data)

    def get(
        self,
        endpoint: str,
        id: Any | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> models.Response:
        return self._api_wrapper(
            method="get", endpoint=endpoint, id=id, params=params, headers=headers
        )

    def post(
        self,
        endpoint: str,
        id: Any | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> models.Response:
        return self._api_wrapper(
            method="post",
            endpoint=endpoint,
            id=id,
            data=data,
            params=params,
            headers=headers,
        )

    def patch(
        self,
        endpoint: str,
        id: Any | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> models.Response:
        return self._api_wrapper(
            method="patch",
            endpoint=endpoint,
            id=id,
            data=data,
            params=params,
            headers=headers,
        )

    def delete(
        self,
        endpoint: str,
        id: Any | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> models.Response:
        return self._api_wrapper(
            method="delete", endpoint=endpoint, id=id, params=params, headers=headers
        )

    def _api_wrapper(
        self,
        method: str,
        endpoint: str,
        id: Any | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> models.Response:
        """Communicate with the api.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The API endpoint to communicate with.
            id (Any | None, optional): Object id which is being appended to the API endpoint. Defaults to None.
            data (dict | None, optional): Data to be sent to the API endpoint as a JSON dictionary. Defaults to None.
            params (dict | None, optional): Query parameters to be sent to the API endpoint. Defaults to None.
            headers (dict | None, optional): Custom headers to be sent to the API endpoint. Defaults to None.

        Raises:
            MySpeedAPIJSONDecodeError: Raised if the JSON in the response could not be parsed.
            MySpeedAPIConnectionError: Raised if a connection/communication error occured.
            MySpeedAPIError: Raised if an unknown error occured.

        Returns:
            models.Response: The response of the server.
        """
        headers = headers or {}
        headers["password"] = self.api_token

        try:
            response = self._session.request(
                method=method,
                url=self._get_url(endpoint, id),
                headers=headers,
                json=data,
                params=params,
            )
            self._verify_response_or_raise(response)

            data = response.json()
            return models.Response(response.status_code, response.reason, data)
        except (ValueError, JSONDecodeError) as exc:
            msg = "Bad JSON in response"
            raise MySpeedAPIJSONDecodeError(msg) from exc
        except requests.exceptions.RequestException as exc:
            msg = f"Error fetching information - {exc}"
            raise MySpeedAPIConnectionError(
                msg,
            ) from exc
        except Exception as exc:
            msg = f"Unknown error occured - {exc}"
            raise MySpeedAPIError(
                msg,
            ) from exc
