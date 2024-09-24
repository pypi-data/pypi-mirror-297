import pytest
from pokepy_sdk.src.client import PokeAPIClient
from pokepy_sdk.src.models.pokemon import Pokemon
from pokepy_sdk.src.models.generation import Generation


@pytest.fixture
def client():
    return PokeAPIClient()


def test_get_pokemon_integration(client):
    # Test fetching a known Pokemon by name
    pokemon = client.get_pokemon("pikachu")
    assert isinstance(pokemon, Pokemon)
    assert pokemon.name == "pikachu"

    # Test fetching a known Pokemon by ID
    pokemon = client.get_pokemon(25)
    assert isinstance(pokemon, Pokemon)
    assert pokemon.name == "pikachu"


def test_get_generation_integration(client):
    # Test fetching a known generation by ID
    generation = client.get_generation(1)
    assert isinstance(generation, Generation)
    assert generation.name == "generation-i"

    # Test fetching a known generation by name
    generation = client.get_generation("generation-i")
    assert isinstance(generation, Generation)
    assert generation.name == "generation-i"


def test_get_all_pokemon_names_integration(client):
    # Test fetching all Pokemon names
    pokemon_names = client.get_all_pokemon_names()
    assert isinstance(pokemon_names, list)
    assert "pikachu" in pokemon_names
