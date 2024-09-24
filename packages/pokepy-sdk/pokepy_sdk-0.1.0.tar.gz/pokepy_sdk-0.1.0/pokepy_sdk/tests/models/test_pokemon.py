import pytest
from pokepy_sdk.src.models.pokemon import (
    Pokemon,
    PokemonSummary,
)


class TestPokemon:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = {
            "id": 1,
            "name": "bulbasaur",
            "base_experience": 64,
            "height": 7,
            "is_default": True,
            "order": 1,
            "weight": 70,
            "abilities": [
                {
                    "ability": {
                        "name": "overgrow",
                        "url": "https://pokeapi.co/api/v2/ability/65/",
                    }
                }
            ],
            "past_abilities": [],
            "forms": [
                {
                    "name": "bulbasaur",
                    "url": "https://pokeapi.co/api/v2/pokemon-form/1/",
                }
            ],
            "game_indices": [
                {
                    "game_index": 1,
                    "version": {
                        "name": "red",
                        "url": "https://pokeapi.co/api/v2/version/1/",
                    },
                }
            ],
            "held_items": [],
            "location_area_encounters": "https://pokeapi.co/api/v2/pokemon/1/encounters",
            "moves": [],
            "species": {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon-species/1/",
            },
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                "back_default": None,
                "front_shiny": None,
                "back_shiny": None,
                "front_female": None,
                "back_female": None,
                "front_shiny_female": None,
                "back_shiny_female": None,
            },
            "cries": {
                "latest": "bulbasaur_latest.mp3",
                "legacy": "bulbasaur_legacy.mp3",
            },
            "stats": [
                {
                    "base_stat": 45,
                    "effort": 0,
                    "stat": {
                        "name": "speed",
                        "url": "https://pokeapi.co/api/v2/stat/6/",
                    },
                }
            ],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "grass",
                        "url": "https://pokeapi.co/api/v2/type/12/",
                    },
                }
            ],
            "past_types": [],
        }
        self.pokemon = Pokemon.from_dict(self.data)

    def test_instantiation(self):
        assert self.pokemon.id == 1
        assert self.pokemon.name == "bulbasaur"
        assert self.pokemon.base_experience == 64
        assert self.pokemon.height == 7
        assert self.pokemon.is_default is True
        assert self.pokemon.order == 1
        assert self.pokemon.weight == 70
        assert len(self.pokemon.abilities) == 1
        assert len(self.pokemon.past_abilities) == 0
        assert len(self.pokemon.forms) == 1
        assert len(self.pokemon.game_indices) == 1
        assert len(self.pokemon.held_items) == 0
        assert (
            self.pokemon.location_area_encounters
            == "https://pokeapi.co/api/v2/pokemon/1/encounters"
        )
        assert len(self.pokemon.moves) == 0
        assert self.pokemon.species.name == "bulbasaur"
        assert (
            self.pokemon.sprites.front_default
            == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
        )
        assert self.pokemon.cries.latest == "bulbasaur_latest.mp3"
        assert len(self.pokemon.stats) == 1
        assert len(self.pokemon.types) == 1
        assert len(self.pokemon.past_types) == 0

    def test_str(self):
        expected_str = (
            "Pokemon with id '1': and name 'bulbasaur'\n"
            "ABILITIES:\n- overgrow\n"
            "STATS:\n- speed: 45"
        )
        assert str(self.pokemon) == expected_str

    def test_repr(self):
        expected_repr = "Pokemon(id=1, name=bulbasaur, base_experience=64, height=7, is_default=True, order=1, weight=70, abilities=[Ability(name='overgrow', url='https://pokeapi.co/api/v2/ability/65/')], past_abilities=[], forms=[PokemonFormSummary(name='bulbasaur', url='https://pokeapi.co/api/v2/pokemon-form/1/')], game_indices=[PokemonGameIndex(game_index=1, version={'name': 'red', 'url': 'https://pokeapi.co/api/v2/version/1/'})], held_items=[], location_area_encounters=https://pokeapi.co/api/v2/pokemon/1/encounters, moves=[], species=name='bulbasaur' url='https://pokeapi.co/api/v2/pokemon-species/1/', sprites=front_default='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png' back_default=None front_shiny=None back_shiny=None front_female=None back_female=None front_shiny_female=None back_shiny_female=None, cries=latest='bulbasaur_latest.mp3' legacy='bulbasaur_legacy.mp3', stats=[PokemonStat(base_stat=45, effort=0, stat={'name': 'speed', 'url': 'https://pokeapi.co/api/v2/stat/6/'})], types=[TypeDetail(slot=1, type={'name': 'grass', 'url': 'https://pokeapi.co/api/v2/type/12/'})], past_types=[])"
        assert repr(self.pokemon) == expected_repr


class TestPokemonSummary:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}
        self.pokemon_summary = PokemonSummary.from_dict(self.data)

    def test_instantiation(self):
        assert self.pokemon_summary.name == "bulbasaur"
        assert self.pokemon_summary.url == "https://pokeapi.co/api/v2/pokemon/1/"

    def test_str(self):
        expected_str = "PokemonSummary:\n- Name: bulbasaur\n- URL: https://pokeapi.co/api/v2/pokemon/1/"
        assert str(self.pokemon_summary) == expected_str

    def test_repr(self):
        expected_repr = (
            "PokemonSummary(name=bulbasaur, url=https://pokeapi.co/api/v2/pokemon/1/)"
        )
        assert repr(self.pokemon_summary) == expected_repr
