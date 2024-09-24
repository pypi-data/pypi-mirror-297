from pydantic import BaseModel
from typing import List, Dict, Optional


class Ability(BaseModel):
    """
    Represents an ability of a Pokemon.

    Attributes:
        name (str): The name of the ability.
        url (str): The URL to the ability resource.
    """

    name: str
    url: str


class PastAbility(BaseModel):
    """
    Represents a past ability of a Pokemon.

    Attributes:
        ability (Ability): The ability details.
        is_hidden (bool): Whether the ability is hidden.
        slot (int): The slot number of the ability.
    """

    ability: Ability
    is_hidden: bool
    slot: int


class PastAbilities(BaseModel):
    """
    Represents a list of past abilities of a Pokemon.

    Attributes:
        abilities (List[PastAbility]): A list of past abilities.
        generation (str): The generation in which these abilities were present.
    """

    abilities: List[PastAbility]
    generation: str


class PokemonFormSummary(BaseModel):
    """
    Represents a summary of a Pokemon form.

    Attributes:
        name (str): The name of the form.
        url (str): The URL to the form resource.
    """

    name: str
    url: str


class PokemonGameIndex(BaseModel):
    """
    Represents a game index of a Pokemon.

    Attributes:
        game_index (int): The game index number.
        version (Dict[str, str]): The version details.
    """

    game_index: int
    version: Dict[str, str]


class Item(BaseModel):
    """
    Represents an item.

    Attributes:
        name (str): The name of the item.
        url (str): The URL to the item resource.
    """

    name: str
    url: str


class Version(BaseModel):
    """
    Represents a version of a game.

    Attributes:
        name (str): The name of the version.
        url (str): The URL to the version resource.
    """

    name: str
    url: str


class VersionDetail(BaseModel):
    """
    Represents details of a version.

    Attributes:
        rarity (int): The rarity of the item in this version.
        version (Version): The version details.
    """

    rarity: int
    version: Version


class HeldItem(BaseModel):
    """
    Represents an item held by a Pokemon.

    Attributes:
        item (Item): The item details.
        version_details (List[VersionDetail]): A list of version details.
    """

    item: Item
    version_details: List[VersionDetail]


class Move(BaseModel):
    """
    Represents a move of a Pokemon.

    Attributes:
        name (str): The name of the move.
        url (str): The URL to the move resource.
    """

    name: str
    url: str


class MoveLearnMethod(BaseModel):
    """
    Represents a method by which a move is learned.

    Attributes:
        name (str): The name of the method.
        url (str): The URL to the method resource.
    """

    name: str
    url: str


class VersionGroup(BaseModel):
    """
    Represents a version group.

    Attributes:
        name (str): The name of the version group.
        url (str): The URL to the version group resource.
    """

    name: str
    url: str


class VersionGroupDetail(BaseModel):
    """
    Represents details of a version group.

    Attributes:
        level_learned_at (int): The level at which the move is learned.
        move_learn_method (MoveLearnMethod): The method by which the move is learned.
        version_group (VersionGroup): The version group details.
    """

    level_learned_at: int
    move_learn_method: MoveLearnMethod
    version_group: VersionGroup


class MoveDetail(BaseModel):
    """
    Represents details of a move.

    Attributes:
        move (Move): The move details.
        version_group_details (List[VersionGroupDetail]): A list of version group details.
    """

    move: Move
    version_group_details: List[VersionGroupDetail]


class PokemonSpeciesSummary(BaseModel):
    """
    Represents a summary of a Pokemon species.

    Attributes:
        name (str): The name of the species.
        url (str): The URL to the species resource.
    """

    name: str
    url: str


class Sprites(BaseModel):
    """
    Represents the sprites of a Pokemon.

    Attributes:
        front_default (Optional[str]): The default front sprite.
        back_default (Optional[str]): The default back sprite.
        front_shiny (Optional[str]): The shiny front sprite.
        back_shiny (Optional[str]): The shiny back sprite.
        front_female (Optional[str]): The female front sprite.
        back_female (Optional[str]): The female back sprite.
        front_shiny_female (Optional[str]): The shiny female front sprite.
        back_shiny_female (Optional[str]): The shiny female back sprite.
    """

    front_default: Optional[str]
    back_default: Optional[str]
    front_shiny: Optional[str]
    back_shiny: Optional[str]
    front_female: Optional[str]
    back_female: Optional[str]
    front_shiny_female: Optional[str]
    back_shiny_female: Optional[str]


class Cries(BaseModel):
    """
    Represents the cries of a Pokemon.

    Attributes:
        latest (str): The latest cry.
        legacy (str): The legacy cry.
    """

    latest: str
    legacy: str


class PokemonStat(BaseModel):
    """
    Represents a stat of a Pokemon.

    Attributes:
        base_stat (int): The base stat value.
        effort (int): The effort value.
        stat (Dict[str, str]): The stat details.
    """

    base_stat: int
    effort: int
    stat: Dict[str, str]


class TypeDetail(BaseModel):
    """
    Represents a type detail of a Pokemon.

    Attributes:
        slot (int): The slot number of the type.
        type (Dict[str, str]): The type details.
    """

    slot: int
    type: Dict[str, str]


class PastType(BaseModel):
    """
    Represents a past type of a Pokemon.

    Attributes:
        generation (str): The generation in which this type was present.
        types (List[TypeDetail]): A list of type details.
    """

    generation: str
    types: List[TypeDetail]


class Pokemon(BaseModel):
    """
    Represents a Pokemon.

    Attributes:
        id (int): The unique identifier for the Pokemon.
        name (str): The name of the Pokemon.
        base_experience (Optional[int]): The base experience of the Pokemon.
        height (Optional[int]): The height of the Pokemon.
        is_default (bool): Whether this is the default form of the Pokemon.
        order (Optional[int]): The order of the Pokemon.
        weight (Optional[int]): The weight of the Pokemon.
        abilities (List[Ability]): A list of abilities of the Pokemon.
        past_abilities (List[PastAbilities]): A list of past abilities of the Pokemon.
        forms (List[PokemonFormSummary]): A list of forms of the Pokemon.
        game_indices (List[PokemonGameIndex]): A list of game indices of the Pokemon.
        held_items (List[HeldItem]): A list of items held by the Pokemon.
        location_area_encounters (str): The location area encounters of the Pokemon.
        moves (List[MoveDetail]): A list of moves of the Pokemon.
        species (PokemonSpeciesSummary): The species summary of the Pokemon.
        sprites (Sprites): The sprites of the Pokemon.
        cries (Cries): The cries of the Pokemon.
        stats (List[PokemonStat]): A list of stats of the Pokemon.
        types (List[TypeDetail]): A list of types of the Pokemon.
        past_types (List[PastType]): A list of past types of the Pokemon.
    """

    id: int
    name: str
    base_experience: Optional[int]
    height: Optional[int]
    is_default: bool
    order: Optional[int]
    weight: Optional[int]
    abilities: List[Ability]
    past_abilities: List[PastAbilities]
    forms: List[PokemonFormSummary]
    game_indices: List[PokemonGameIndex]
    held_items: List[HeldItem]
    location_area_encounters: str
    moves: List[MoveDetail]
    species: PokemonSpeciesSummary
    sprites: Sprites
    cries: Cries
    stats: List[PokemonStat]
    types: List[TypeDetail]
    past_types: List[PastType]

    @classmethod
    def from_dict(cls, data):
        abilities = [Ability(**ability["ability"]) for ability in data["abilities"]]
        past_abilities = [
            PastAbilities(**past_ability) for past_ability in data["past_abilities"]
        ]
        forms = [PokemonFormSummary(**form) for form in data["forms"]]
        game_indices = [
            PokemonGameIndex(**game_index) for game_index in data["game_indices"]
        ]
        held_items = [HeldItem(**held_item) for held_item in data["held_items"]]
        moves = [MoveDetail(**move) for move in data["moves"]]
        species = PokemonSpeciesSummary(**data["species"])
        sprites = Sprites(**data["sprites"])
        cries = Cries(**data["cries"])
        stats = [PokemonStat(**stat) for stat in data["stats"]]
        types = [TypeDetail(**type_detail) for type_detail in data["types"]]
        past_types = [PastType(**past_type) for past_type in data["past_types"]]

        return cls(
            id=data["id"],
            name=data["name"],
            base_experience=data.get("base_experience"),
            height=data.get("height"),
            is_default=data["is_default"],
            order=data.get("order"),
            weight=data.get("weight"),
            abilities=abilities,
            past_abilities=past_abilities,
            forms=forms,
            game_indices=game_indices,
            held_items=held_items,
            location_area_encounters=data["location_area_encounters"],
            moves=moves,
            species=species,
            sprites=sprites,
            cries=cries,
            stats=stats,
            types=types,
            past_types=past_types,
        )

    def __str__(self):
        stats_str = "\n".join(
            [f"- {stat.stat['name']}: {stat.base_stat}" for stat in self.stats]
        )
        abilities_str = "\n".join([f"- {ability.name}" for ability in self.abilities])
        return (
            f"Pokemon with id '{self.id}': and name '{self.name}'\n"
            f"ABILITIES:\n{abilities_str}\n"
            f"STATS:\n{stats_str}"
        )

    def __repr__(self):
        return (
            f"Pokemon(id={self.id}, name={self.name}, base_experience={self.base_experience}, "
            f"height={self.height}, is_default={self.is_default}, order={self.order}, weight={self.weight}, "
            f"abilities={self.abilities}, past_abilities={self.past_abilities}, forms={self.forms}, "
            f"game_indices={self.game_indices}, held_items={self.held_items}, "
            f"location_area_encounters={self.location_area_encounters}, moves={self.moves}, "
            f"species={self.species}, sprites={self.sprites}, cries={self.cries}, stats={self.stats}, "
            f"types={self.types}, past_types={self.past_types})"
        )


class PokemonSummary(BaseModel):
    """
    Represents a summary of a Pokemon.

    Attributes:
        name (str): The name of the Pokemon.
        url (str): The URL to the Pokemon resource.
    """

    name: str
    url: str

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], url=data["url"])

    def __str__(self):
        return f"PokemonSummary:\n" f"- Name: {self.name}\n" f"- URL: {self.url}"

    def __repr__(self):
        return f"PokemonSummary(name={self.name}, url={self.url})"
