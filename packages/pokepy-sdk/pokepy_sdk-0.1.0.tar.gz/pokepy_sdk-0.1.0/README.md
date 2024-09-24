# PokeAPI SDK

A Python SDK for PokeAPI, providing easy access to Pokémon data.

## Installation
Install `pokepy_sdk` with Python's `pip` package manager:
`pip install pokeapi-sdk`

## Usage
First, instantiate a client:```
from pokeapi_sdk.client import PokeAPIClient
client = PokeAPIClient()
```

With a `PokeAPIClient` object:
- 1: Get a Pokémon by name (str) or ID (int)
```
pokemon = client.get_pokemon("pikachu")
print(pokemon.name, pokemon.abilities)
```
This returns a `Pokemon` object.

- 2: Get a generation by name (str) or ID (int)
```
generation = client.get_generation(1)
print(generation.name, generation.pokemon_species)
```
This returns a `Generation` object.

- 3: Get a summary of every Pokemon:
```
all_pokemon = client.get_all_pokemon_summaries()
```
This returns a list of `PokemonSummary` objects.

- 4: Get a summary of every Generation:
```
all_generations = client.get_all_generation_summaries()
```
This returns a list of `GenerationSummary` objects.

Both `get_all_pokemon_summaries()` & `get_all_generation_summaries()` support optional offset-based pagiation parameters:
- `offset`: The starting point within the collection 
- `page_size`: The maximum number of objects to return in the request

## Testing

To run the unit tests:
`pytest`

To run the integration tests:
`pytest pokep_sdky/tests/integration_tests.py`

## Design Decisions 
- **Pagination**: Optional offset-based pagination is supported when fetching all Pokemon & all Pokemon generations. 
- **Pydantic data validation**: Pydantic provides excellent validation tools for instantiation of class instances
- **Error Handling**: Comprehensive HTTP error handling for all requests
- **Abstractions**: Significant use of classes & a client object to simplify user experience
- **Package management with Poetry**: Poetry provides intuitive dependency & package management
- **Rate Limit Handling**: PokeAPI does not currently impose API rate limits, but a simple rate limit handler has been included for all requests
- **`__str__` & `__repr__` overrides**: For improved informational display of class instances

## Tools Used
- `black` formatter: https://github.com/psf/black
- `ruff` linting & formatting: https://docs.astral.sh/ruff/
- `mypy` for static type checking: https://github.com/python/mypy
- `pytest` for unit test & integration tests https://docs.pytest.org/en/stable/
- `tenacity` for handling rate limiting: https://github.com/jd/tenacity
