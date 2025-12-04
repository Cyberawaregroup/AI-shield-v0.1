import asyncio
import logging
import typing
from urllib.parse import quote, urlencode, urljoin
import warnings

import httpx

from app.clients.hibp.errors import (
    HIBPAuthError,
    HIBPClientError,
    HIBPError,
    HIBPRateLimitError,
    HIBPResponseError,
    HIBPServerError,
)
from app.clients.hibp.types import (
    Breach,
    DataT,
    HIBPResponse,
    Paste,
    SubscribedDomain,
    SubscriptionStatus,
)

logger = logging.getLogger(__name__)

__all__ = ["HIBPAsyncClient"]


class HIBPAsyncClient:
    """Asynchronous client for interacting with the Have I Been Pwned API."""

    base_url = "https://haveibeenpwned.com/api/v3"
    """Default base URL for the HIBP API."""
    pwned_password_base_url = "https://api.pwnedpasswords.com/range/"
    """Base URL for the Pwned Passwords API."""

    def __init__(
        self,
        api_key: str,
        base_url: typing.Optional[str] = None,
        timeout: typing.Union[float, httpx.Timeout] = 30.0,
        user_agent: typing.Optional[str] = None,
    ):
        """
        Initialize the HIBP client with API key.

        :param api_key: Your HIBP API key (required for all requests).
        :param base_url: Optional base URL for the API (defaults to HIBP API URL).
        :param timeout: Request timeout in seconds or httpx.Timeout object.
        :param user_agent: Optional custom user agent string.
        """
        self.api_key = api_key
        self.base_url = base_url or self.base_url
        self.timeout = timeout
        self.user_agent = user_agent or "HIBP-Python-Client/1.0"
        self._session: typing.Optional[httpx.AsyncClient] = None
        logger.debug(
            f"Initialized {self.__class__.__name__} with base URL: {self.base_url}"
        )

    @property
    def session(self) -> httpx.AsyncClient:
        """Get or create the HTTP client session."""
        if self._session is None:
            logger.debug("Creating new HTTP session for HIBP client")
            self._session = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.get_headers(),
                timeout=self.timeout,
            )
        return self._session

    def get_headers(self) -> typing.Dict[str, str]:
        """Get the headers for the API requests."""
        return {
            "hibp-api-key": self.api_key,
            "user-agent": self.user_agent,
            "Accept": "application/json",
        }

    def get_url(
        self,
        service: str,
        parameter: typing.Optional[str] = None,
        query_params: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> str:
        """
        Construct a properly quoted URL for the HIBP API.

        :param service: The API service/endpoint (e.g., "breaches", "breach", "breachedaccount").
        :param parameter: Optional parameter to append to the service (e.g., breach name, email).
        :param query_params: Optional query parameters as a dictionary.
        :return: The complete URL with properly quoted parameter and query string.
        """
        if parameter:
            parameter_safe = quote(parameter, safe="")
            path = f"/{service}/{parameter_safe}"
        else:
            path = f"/{service}"

        if query_params:
            query_string = urlencode(query_params)
            return f"{path}?{query_string}"
        return path

    async def close(self):
        """Close the underlying HTTP session."""
        if self._session is not None:
            logger.debug("Closing HTTP session")
            await self._session.aclose()
            self._session = None
            logger.debug("HTTP session closed successfully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __del__(self):
        if self._session is not None and not self._session.is_closed:
            logger.warning("HIBP client session not properly closed")
            warnings.warn(
                "Unclosed client session. Please use 'async with' or call 'await close()' to close the session properly.",
                ResourceWarning,
            )
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.close())
            except RuntimeError:
                pass

    def get_response_model(self, typ: typing.Type[DataT]) -> HIBPResponse[DataT]:
        return typing.cast(HIBPResponse[DataT], HIBPResponse[typ])  # type: ignore

    @typing.overload
    async def _call(
        self,
        url: str,
        response_type: typing.Type[DataT],
        method: str = "GET",
        **kwargs: typing.Any,
    ) -> typing.Optional[DataT]: ...

    @typing.overload
    async def _call(
        self,
        url: str,
        response_type: None = None,
        method: str = "GET",
        **kwargs: typing.Any,
    ) -> typing.Optional[typing.Any]: ...

    async def _call(
        self,
        url: str,
        response_type: typing.Optional[typing.Type[typing.Any]] = None,
        method: str = "GET",
        **kwargs: typing.Any,
    ) -> typing.Optional[typing.Any]:
        """
        Make an API call to the HIBP API.

        :param url: The endpoint URL (relative to base_url).
        :param response_type: The type to parse the response data.
        :param method: HTTP method (GET, POST, etc.).
        :param kwargs: Additional arguments to pass to httpx request.
        :return: Parsed and validated response data or None for 404.
        :raises HIBPAuthError: For authentication errors (401, 403).
        :raises HIBPRateLimitError: For rate limit errors (429).
        :raises HIBPNotFoundError: For not found errors (404).
        :raises HIBPClientError: For other client errors (4xx).
        :raises HIBPServerError: For server errors (5xx).
        :raises HIBPResponseError: For response parsing errors.
        """
        logger.debug(f"Making {method} request to {url}")
        start_time = asyncio.get_event_loop().time()

        try:
            response = await self.session.request(method, url=url, **kwargs)
            elapsed_time = asyncio.get_event_loop().time() - start_time
            code = response.status_code

            logger.debug(f"API response: {code} in {elapsed_time:.3f}s")

            if code == 404:
                logger.debug("Resource not found (404)")
                return None

            if code == 429:
                retry_after = response.headers.get("Retry-After")
                retry_seconds = int(retry_after) if retry_after else None
                logger.warning(f"Rate limit exceeded. Retry after: {retry_seconds}s")
                raise HIBPRateLimitError(retry_after=retry_seconds)

            if code in (401, 403):
                logger.error(f"Authentication error: {code}")
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", "Authentication failed")
                except Exception:
                    error_msg = "Authentication failed. Invalid API key or insufficient permissions."
                raise HIBPAuthError(message=error_msg, code=code)

            if 400 <= code < 500:
                logger.warning(f"Client error: {code}")
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", f"Client error: {code}")
                except Exception:
                    error_msg = f"Client error: {code}"
                raise HIBPClientError(message=error_msg, code=code)

            if code >= 500:
                logger.error(f"Server error: {code}")
                raise HIBPServerError(message=f"HIBP server error: {code}", code=code)

            if code == 200:
                try:
                    response_data = response.json()
                except Exception as exc:
                    logger.error(f"Failed to parse API response: {exc}", exc_info=True)
                    raise HIBPResponseError(f"Failed to parse response: {exc}") from exc

                logger.debug(
                    f"API response received with {len(str(response_data))} bytes"
                )
                response_model = (
                    self.get_response_model(response_type) if response_type else None
                )
                if response_model is None:
                    return response_data
                return response_model.model_validate(response_data)

            logger.warning(f"Unexpected status code: {code}")
            raise HIBPClientError(message=f"Unexpected status code: {code}", code=code)

        except HIBPError:
            raise
        except Exception as exc:
            raise HIBPClientError(f"Request failed: {exc}") from exc
        finally:
            elapsed_time = asyncio.get_event_loop().time() - start_time
            logger.debug(f"API request to {url} completed in {elapsed_time:.3f}s")

    async def get_account_breaches(
        self,
        account: str,
        truncate_response: bool = False,
        domain: typing.Optional[str] = None,
        include_unverified: bool = True,
    ) -> typing.Optional[typing.List[Breach]]:
        """
        Get all breaches an account has been involved in.

        :param account: The account identifier (email or username).
        :param truncate_response: Whether to truncate the breach data.
        :param domain: Optional domain to filter breaches (e.g., "adobe.com").
        :param include_unverified: Whether to include unverified breaches.
        :return: List of `Breach` objects.
        """
        query_params = {
            "truncateResponse": str(truncate_response).lower(),
            "includeUnverified": str(include_unverified).lower(),
        }
        if domain:
            query_params["Domain"] = domain

        url = self.get_url(service="breachedaccount", parameter=account)
        logger.debug(
            f"Fetching all breaches{f' for domain {domain}' if domain else ''}"
        )
        return await self._call(
            url, response_type=typing.List[Breach], params=query_params
        )

    async def get_domain_emails_breaches(
        self, domain: str
    ) -> typing.Optional[typing.Dict[str, typing.List[str]]]:
        """
        Get all email addresses on a given domain and the breaches they've appeared in.

        :param domain: The domain to check (e.g., "adobe.com").
        :return: Dictionary mapping email addresses to list of breach names they appeared in.

        Example:
        ```json
        {"user@example.com": ["Adobe", "LinkedIn"], "admin@example.com": ["Yahoo"]}
        ```
        """
        url = self.get_url(service="breacheddomain", parameter=domain)
        logger.debug(f"Fetching breached emails for domain: {domain}")
        return await self._call(url, response_type=typing.Dict[str, typing.List[str]])

    async def get_subscribed_domains(
        self,
    ) -> typing.Optional[typing.List[SubscribedDomain]]:
        """
        Get all domains subscribed to breach notifications.

        :return: List of `SubscribedDomain` objects.
        """
        url = self.get_url(service="subscribeddomains")
        logger.debug("Fetching subscribed domains for breach notifications")
        return await self._call(url, response_type=typing.List[SubscribedDomain])

    async def get_all_breaches(
        self,
        domain: typing.Optional[str] = None,
        include_spam_lists: bool = False,
    ) -> typing.Optional[typing.List[Breach]]:
        """
        Get all breaches in the HIBP database.

        :param domain: Only return breaches this domain was involved in (e.g., "adobe.com").
        :param include_spam_lists: Whether to include spam list breaches.
        :return: List of `Breach` objects.
        """
        query_params = {
            "isSpamLists": str(include_spam_lists).lower(),
        }
        if domain:
            query_params["Domain"] = domain

        url = self.get_url(service="breaches")
        logger.debug(
            f"Fetching all breaches{f' for domain {domain}' if domain else ''}"
        )
        return await self._call(
            url, response_type=typing.List[Breach], params=query_params
        )

    async def get_breach(self, name: str) -> typing.Optional[Breach]:
        """
        Get details of a specific breach by name.

        :param name: The name of the breach (e.g., "Adobe").
            This is the stable value which may or may not be
            the same as the breach "Title", which can change.
        :return: A `Breach` object.
        """
        url = self.get_url(service="breach", parameter=name)
        logger.debug(f"Fetching details for breach: {name}")
        return await self._call(url, response_type=Breach)

    async def get_latest_breach(self) -> typing.Optional[Breach]:
        """
        Get the most recently added breach based on the "AddedDate" attribute
        of the breach model. This may not be the most recent breach to occur
        as there may be significant lead time between a service being breached
        and the data later appearing on HIBP.

        :return: A `Breach` object.
        """
        url = self.get_url(service="latestbreach")
        logger.debug("Fetching latest breach")
        return await self._call(url, response_type=Breach)

    async def get_all_dataclasses(self) -> typing.Optional[typing.List[str]]:
        """
        Get all data classes used to label breaches in the HIBP database.

        A "data class" is an attribute of a record compromised in a breach.
        For example, many breaches expose data classes such as "Email addresses"
        and "Passwords". The values returned by this service are ordered
        alphabetically in a string array and will expand over time as new
        breaches expose previously unseen classes of data.

        :return: List of data class strings.
        """
        url = self.get_url(service="dataclasses")
        logger.debug("Fetching all data classes")
        return await self._call(url, response_type=typing.List[str])

    async def get_stealer_log_domains(
        self, email: str
    ) -> typing.Optional[typing.List[str]]:
        """
        Get all stealer log domains associated with a given email address.

        :param email: The email address to check.
        :return: List of stealer log domain strings.
        """
        url = self.get_url(service="stealerlogsbyemail", parameter=email)
        logger.debug(f"Fetching stealer log domains for email: {email}")
        return await self._call(url, response_type=typing.List[str])

    async def get_stealer_log_domain_emails(
        self, domain: str
    ) -> typing.Optional[typing.List[str]]:
        """
        Get all email addresses associated with a given stealer log domain.

        :param domain: The stealer log domain to check.
        :return: List of email address strings.
        """
        url = self.get_url(service="stealerlogsbywebsitedomain", parameter=domain)
        logger.debug(f"Fetching stealer log emails for domain: {domain}")
        return await self._call(url, response_type=typing.List[str])

    async def get_account_pastes(
        self, account: str
    ) -> typing.Optional[typing.List[Paste]]:
        """
        Get all pastes for a given account.
        The collection is sorted chronologically with the newest paste first.

        :param account: The account identifier (email or username).
        :return: List of paste data dictionaries.
        """
        url = self.get_url(service="pasteaccount", parameter=account)
        logger.debug(f"Fetching pastes for account: {account}")
        return await self._call(url, response_type=typing.List[Paste])

    async def get_subscription_status(self) -> typing.Optional[SubscriptionStatus]:
        """
        Get the subscription status for the client account associated with the API key.

        :return: A `SubscriptionStatus` object.
        """
        url = self.get_url(service="subscription", parameter="status")
        logger.debug("Fetching subscription status...")
        return await self._call(url, response_type=SubscriptionStatus)

    async def search_pwned_password(
        self, hash_prefix: str, hash_mode: typing.Literal["sha1", "ntlm"] = "sha1"
    ) -> typing.Dict[str, int]:
        """
        Search pwned password hash suffixes and their breach counts for a given hash prefix.

        :param hash_prefix: The first 5 characters of the hashed password.
        :param hash_mode: The hashing algorithm used (default: "sha1").
        :return: Dictionary mapping hash suffixes to breach counts.
        """
        assert len(hash_prefix) == 5, "Hash prefix must be exactly 5 characters long"
        hash_prefix = hash_prefix.upper()
        url = urljoin(self.pwned_password_base_url, hash_prefix)
        logger.debug(f"Fetching pwned password suffixes for prefix: {hash_prefix}")
        data = await self._call(url, response_type=str)
        if data is None:
            return {}

        matching_suffixes = {}
        for line in data.splitlines():
            if ":" in line:
                suffix, count_str = line.split(":", 1)
                try:
                    count = int(count_str)
                    matching_suffixes[suffix] = count
                except ValueError:
                    logger.warning(
                        f"Invalid count value for suffix {suffix}: {count_str}"
                    )
        return matching_suffixes

    async def check_password_pwned(
        self, password_hash: str, hash_mode: typing.Literal["sha1", "ntlm"] = "sha1"
    ) -> int:
        """
        Check if a password hash has been pwned and return the breach count.

        :param password_hash: The hashed password (full hash).
        :param hash_mode: The hashing algorithm used (default: "sha1").
            Can be either "sha1" or "ntlm".
        :return: The number of times the password has been seen in breaches.
                 Returns 0 if not pwned.
        """
        hash_prefix = password_hash[:5]
        hash_suffix = password_hash[5:].upper()

        matching_suffixes = await self.search_pwned_password(
            hash_prefix, hash_mode=hash_mode
        )
        if hash_suffix in matching_suffixes:
            return matching_suffixes[hash_suffix]
        return 0
