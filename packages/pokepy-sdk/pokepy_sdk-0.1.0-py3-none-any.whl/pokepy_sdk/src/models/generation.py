from pydantic import BaseModel
from typing import List


class Generation(BaseModel):
    """
    Represents a Pokemon generation.

    Attributes:
        id (int): The unique identifier for the generation.
        name (str): The name of the generation.
        pokemon_species (List[str]): A list of Pokemon species names in this generation.
    """

    id: int
    name: str
    pokemon_species: List[str]

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Generation instance from a dictionary.

        Args:
            data (dict): A dictionary containing generation data.

        Returns:
            Generation: An instance of the Generation class.
        """
        pokemon_species = [species["name"] for species in data["pokemon_species"]]
        return cls(id=data["id"], name=data["name"], pokemon_species=pokemon_species)

    def __str__(self):
        """
        Returns a string representation of the Generation instance.

        Returns:
            str: A string describing the generation.
        """
        species_str = "\n".join([f"- {species}" for species in self.pokemon_species])
        return (
            f"Generation with id '{self.id}': and name '{self.name}'\n"
            f"SPECIES:\n{species_str}"
        )

    def __repr__(self):
        """
        Returns a detailed string representation of the Generation instance.

        Returns:
            str: A detailed string describing the generation.
        """
        return f"Generation(id={self.id}, name={self.name}, pokemon_species={self.pokemon_species})"


class GenerationSummary(BaseModel):
    """
    Represents a summary of a Pokemon generation.

    Attributes:
        name (str): The name of the generation.
        url (str): The URL to the generation resource.
    """

    name: str
    url: str

    @classmethod
    def from_dict(cls, data):
        """
        Creates a GenerationSummary instance from a dictionary.

        Args:
            data (dict): A dictionary containing generation summary data.

        Returns:
            GenerationSummary: An instance of the GenerationSummary class.
        """
        return cls(name=data["name"], url=data["url"])

    def __str__(self):
        """
        Returns a string representation of the GenerationSummary instance.

        Returns:
            str: A string describing the generation summary.
        """
        return f"GenerationSummary:\n" f"- Name: {self.name}\n" f"- URL: {self.url}"

    def __repr__(self):
        """
        Returns a detailed string representation of the GenerationSummary instance.

        Returns:
            str: A detailed string describing the generation summary.
        """
        return f"GenerationSummary(name={self.name}, url={self.url})"
