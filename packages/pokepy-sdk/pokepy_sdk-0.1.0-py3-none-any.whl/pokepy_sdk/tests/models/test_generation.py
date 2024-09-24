import pytest
from pokepy_sdk.src.models.generation import Generation, GenerationSummary


class TestGeneration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = {
            "id": 1,
            "name": "generation-i",
            "pokemon_species": [
                {"name": "bulbasaur"},
                {"name": "ivysaur"},
                {"name": "venusaur"},
            ],
        }
        self.generation = Generation.from_dict(self.data)

    def test_instantiation(self):
        assert self.generation.id == 1
        assert self.generation.name == "generation-i"
        assert self.generation.pokemon_species == ["bulbasaur", "ivysaur", "venusaur"]

    def test_str(self):
        expected_str = (
            "Generation with id '1': and name 'generation-i'\n"
            "SPECIES:\n- bulbasaur\n- ivysaur\n- venusaur"
        )
        assert str(self.generation) == expected_str

    def test_repr(self):
        expected_repr = "Generation(id=1, name=generation-i, pokemon_species=['bulbasaur', 'ivysaur', 'venusaur'])"
        assert repr(self.generation) == expected_repr


class TestGenerationSummary:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data = {
            "name": "generation-i",
            "url": "https://pokeapi.co/api/v2/generation/1/",
        }
        self.generation_summary = GenerationSummary.from_dict(self.data)

    def test_instantiation(self):
        assert self.generation_summary.name == "generation-i"
        assert self.generation_summary.url == "https://pokeapi.co/api/v2/generation/1/"

    def test_str(self):
        expected_str = "GenerationSummary:\n- Name: generation-i\n- URL: https://pokeapi.co/api/v2/generation/1/"
        assert str(self.generation_summary) == expected_str

    def test_repr(self):
        expected_repr = "GenerationSummary(name=generation-i, url=https://pokeapi.co/api/v2/generation/1/)"
        assert repr(self.generation_summary) == expected_repr
