import requests
from requests.models import Response
from requests.exceptions import HTTPError
from pokepy_sdk.src.models.pokemon import Pokemon, PokemonSummary
from pokepy_sdk.src.models.generation import Generation, GenerationSummary
from pokepy_sdk.exceptions import (
    BadRequest,
    Unauthorized,
    NotFound,
    UnprocessibleEntity,
)
from typing import Optional, List, Callable, Union
from tenacity import RetryCallState, retry, stop_after_attempt, wait_exponential_jitter  # type: ignore


def raise_for_error_code(
    response: requests.Response, identifier: Optional[Union[str, int]] = None
) -> None:
    """
    Raises an exception if the response.status_code matches a handled error
    """
    if response.status_code == 200:
        return
    if response.status_code == 400:
        raise BadRequest(response, response.text)
    if response.status_code == 401:
        raise Unauthorized(response, response.text)
    if response.status_code == 404:
        error_message = f"NotFound: The requested resource with identifier '{identifier}' was not found."
        print(error_message)
        raise NotFound(response, error_message)
    if response.status_code == 422:
        raise UnprocessibleEntity(response, response.text)


def log_rate_limit_exceeded(retry_state: RetryCallState):
    """
    If a 429 is encountered, log that waiting is occurring before the nex request
    """
    wait_time = retry_state.next_action.sleep
    print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")


def retry_if_status_code_429(retry_state: RetryCallState):
    """
    Determine if an encountered HTTPError code is a 429.
    If it is, trigger retries to handle the rate limiting
    """
    exception = retry_state.outcome.exception()
    if isinstance(exception, HTTPError):
        response: Response = exception.response
        return response.status_code == 429
    return False


class PokeAPIClient:
    """
    Client object for interacting with pokeapi API endpoints

    CLIENT CREATION
    ---------------
    ```
    client = PokeAPIClient()
    ```

    EXAMPLE USAGE
    -------------

    Get a specific pokemon based on its name (str) or id (int):
    ```
    identifier = "pikachu"
    client.get_pokemon(identifier)
    ```

    Get a specific generation of pokemon based on its name (str) or id (int):
    identifier = 1
    client.get_generation(identifier)
    """

    BASE_URL = "https://pokeapi.co/api/v2"

    @retry(
        wait=wait_exponential_jitter(initial=60, max=300),
        stop=stop_after_attempt(10),
        retry=retry_if_status_code_429,
        before_sleep=log_rate_limit_exceeded,
    )
    def _request(
        self,
        endpoint: str,
        method: Callable,
        params: Optional[dict] = None,
        identifier: Optional[Union[str, int]] = None,
    ) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        response = method(url, params=params)
        raise_for_error_code(response, identifier)
        return response.json()

    def get_pokemon(self, identifier: str) -> Pokemon:
        """
        Return a specific pokemon based on its name or ID
        """
        data = self._request(
            f"pokemon/{identifier}", method=requests.get, identifier=identifier
        )
        return Pokemon.from_dict(data)

    def get_generation(self, identifier: Union[str, int]) -> Generation:
        """
        Return a specific generation based on its name or ID
        """
        data = self._request(
            f"generation/{identifier}", method=requests.get, identifier=identifier
        )
        return Generation.from_dict(data)

    def get_all_pokemon_summaries(
        self, offset: int = 0, page_size: int = 100
    ) -> List[PokemonSummary]:
        """
        Returns a summary of every Pokemon with optional pagination support.

        Args:
            offset (int): The starting point within the collection of Pokemon. Default is 0.
            page_size (int): The maximum number of Pokemon to return. Default is 100.
        """
        all_pokemon_summaries = []
        next_url = f"{self.BASE_URL}/pokemon?offset={offset}&limit={page_size}"

        print("Getting summaries of all Pokemon...")
        while next_url:
            response = requests.get(next_url)
            data = response.json()
            all_pokemon_summaries.extend(
                [PokemonSummary.from_dict(pokemon) for pokemon in data["results"]]
            )
            next_url = data.get("next")
            if next_url:
                # Ensure the offset and page_size persist in the next_url
                next_offset = next_url.split("offset=")[-1].split("&")[0]
                next_url = (
                    f"{self.BASE_URL}/pokemon?offset={next_offset}&limit={page_size}"
                )

        return all_pokemon_summaries

    def get_all_generation_summaries(
        self, offset: int = 0, page_size: int = 100
    ) -> List[GenerationSummary]:
        """
        Returns a summary of every Pokemon generation with optional pagination support.

        Args:
            offset (int): The starting point within the collection of generations. Default is 0.
            page_size (int): The maximum number of generations to return. Default is 100.
        """
        all_generation_summaries = []
        next_url = f"{self.BASE_URL}/generation?offset={offset}&limit={page_size}"

        print("Getting summaries of all Pokemon generations...")
        while next_url:
            response = requests.get(next_url)
            data = response.json()
            all_generation_summaries.extend(
                [
                    GenerationSummary.from_dict(generation)
                    for generation in data["results"]
                ]
            )
            next_url = data.get("next")

        return all_generation_summaries

    def get_all_pokemon_names(self) -> List[str]:
        """
        Return a list containing the name of every available Pokemon
        """
        pokemon_summaries = self.get_all_pokemon_summaries()
        return [pokemon.name for pokemon in pokemon_summaries]
