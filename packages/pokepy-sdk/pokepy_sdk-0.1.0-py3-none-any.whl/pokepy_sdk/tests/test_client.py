import pytest
import json
from pathlib import Path
from unittest.mock import patch, Mock
from pokepy_sdk.src.client import PokeAPIClient
from pokepy_sdk.exceptions import NotFound


@pytest.fixture
def client():
    return PokeAPIClient()


def test_get_pokemon_success(client):
    file_location = Path(__file__).parents[0] / "data" / "sample_pokemon_response.json"
    with open(file_location) as f:
        sample_response = json.load(f)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_response

    with patch("requests.get", return_value=mock_response):
        pokemon = client.get_pokemon("bulbasaur")
        assert pokemon.id == 1
        assert pokemon.name == "bulbasaur"


def test_get_pokemon_not_found(client):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(NotFound):
            client.get_pokemon("unknown")


def test_get_generation_success(client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "generation-i",
        "pokemon_species": [{"name": "bulbasaur"}, {"name": "ivysaur"}],
    }

    with patch("requests.get", return_value=mock_response):
        generation = client.get_generation(1)
        assert generation.id == 1
        assert generation.name == "generation-i"
        assert "bulbasaur" in generation.pokemon_species


def test_get_generation_not_found(client):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(NotFound):
            client.get_generation(999)


def test_get_all_pokemon_summaries(client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        {
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}
            ],
            "next": None,
        }
    ]

    with patch("requests.get", return_value=mock_response):
        summaries = client.get_all_pokemon_summaries()
        assert len(summaries) == 1
        assert summaries[0].name == "bulbasaur"


def test_get_all_generation_summaries(client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        {
            "results": [
                {
                    "name": "generation-i",
                    "url": "https://pokeapi.co/api/v2/generation/1/",
                }
            ],
            "next": None,
        }
    ]

    with patch("requests.get", return_value=mock_response):
        summaries = client.get_all_generation_summaries()
        assert len(summaries) == 1
        assert summaries[0].name == "generation-i"


def test_get_all_pokemon_names(client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        {
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            ],
            "next": None,
        }
    ]

    with patch("requests.get", return_value=mock_response):
        names = client.get_all_pokemon_names()
        assert len(names) == 2
        assert names[0] == "bulbasaur"
        assert names[1] == "ivysaur"
