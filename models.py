from pydantic import (
    BaseModel as PydanticBaseModel,
    Field,
    model_validator,
    ValidationError,
    BeforeValidator,
    AfterValidator,
)
from enum import Enum
from datetime import date
from typing import Annotated, Literal, Union, Tuple, Optional, ClassVar
from decimal import Decimal
import validators

from pydantic import Extra, FilePath


class BaseModel(PydanticBaseModel):
    class Config:
        pass
        # extra = Extra.forbid
        # arbitrary_types_allowed = True


# pesudo-primitive" PDX-exclusive classes
Repeated = list  # used for keys that repeat
PDXBoolean = Union[Literal["yes"], Literal["no"]]

unquotedPDXVariable = Annotated[
    str,
    BeforeValidator(validators.validate_unquoted_string),
    AfterValidator(validators.make_string_unquoted),
]
unquotedPDXDate = Annotated[
    str,
    BeforeValidator(validators.validate_pdx_date),
    AfterValidator(validators.make_string_unquoted),
]
unquotedTag = Annotated[
    str,
    BeforeValidator(validators.validate_tag),
    AfterValidator(validators.make_string_unquoted),
]
unquotedThreeSigFigDecimal = Annotated[
    float,
    BeforeValidator(validators.validate_3_sigfig_decimal),
    AfterValidator(validators.make_string_unquoted),
]
unquotedFiveSigFigDecimal = Annotated[
    float,
    BeforeValidator(validators.validate_5_sigfig_decimal),
    AfterValidator(validators.make_string_unquoted),
]
unquotedIdeology = Annotated[
    str,
    BeforeValidator(validators.validate_ideology),
    AfterValidator(validators.make_string_unquoted),
]
unquotedInt = Annotated[
    int,
    BeforeValidator(validators.validate_int_str),
    AfterValidator(validators.make_string_unquoted),
]
unquotedRGO = Annotated[
    str,
    BeforeValidator(validators.validate_rgo),
    AfterValidator(validators.make_string_unquoted),
]
unquotedTechnology = Annotated[
    str,
    BeforeValidator(validators.validate_technology),
    AfterValidator(validators.make_string_unquoted),
]
quotedPDXVariable = Annotated[
    str,
    BeforeValidator(validators.validate_quoted_string),
    AfterValidator(validators.make_string_quoted),
]
quotedPDXDate = Annotated[
    str,
    BeforeValidator(validators.validate_pdx_date),
    AfterValidator(validators.make_string_quoted),
]
quotedTag = Annotated[
    str,
    BeforeValidator(validators.validate_tag),
    AfterValidator(validators.make_string_quoted),
]
quotedThreeSigFigDecimal = Annotated[
    float,
    BeforeValidator(validators.validate_3_sigfig_decimal),
    AfterValidator(validators.make_string_quoted),
]
quotedFiveSigFigDecimal = Annotated[
    float,
    BeforeValidator(validators.validate_5_sigfig_decimal),
    AfterValidator(validators.make_string_quoted),
]
quotedIdeology = Annotated[
    str,
    BeforeValidator(validators.validate_ideology),
    AfterValidator(validators.make_string_quoted),
]
quotedInt = Annotated[
    int,
    BeforeValidator(validators.validate_int_str),
    AfterValidator(validators.make_string_quoted),
]
quotedRGO = Annotated[
    str,
    BeforeValidator(validators.validate_rgo),
    AfterValidator(validators.make_string_quoted),
]
quotedTechnology = Annotated[
    str,
    BeforeValidator(validators.validate_technology),
    AfterValidator(validators.make_string_quoted),
]


class RepeatedKeyIndicator(BaseModel):
    this_is_a_repeated_key_please_collapse_down: Optional[bool] = True


class Convoys(BaseModel):
    clipper_convoy: unquotedFiveSigFigDecimal
    steamer_convoy: unquotedFiveSigFigDecimal


class WorldMarket(BaseModel):
    worldmarket_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    price_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    last_price_history: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    last_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    price_history: Repeated[
        RepeatedKeyIndicator | dict[unquotedRGO, unquotedFiveSigFigDecimal]
    ]
    price_history_last_update: quotedPDXDate
    price_change: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    discovered_goods: dict[unquotedRGO, float]
    actual_sold: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    actual_sold_world: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    real_demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    player_balance: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    player_pops_consumption_cache: Repeated[
        RepeatedKeyIndicator | dict[unquotedRGO, unquotedFiveSigFigDecimal]
    ]


class IdeologyEnabled(BaseModel):
    enabled: quotedPDXDate


class Identifier(BaseModel):
    id: unquotedInt
    type: unquotedInt


class IndexedIdentifier(Identifier):
    index: unquotedInt


class FiredEvent(BaseModel):
    id: Repeated[RepeatedKeyIndicator | Identifier]


class Culture(BaseModel):
    name: unquotedPDXVariable
    religion: unquotedPDXVariable


class Pop(BaseModel):
    id: unquotedInt
    pop_type: unquotedPDXVariable
    size: unquotedInt
    culture: Culture
    money: unquotedFiveSigFigDecimal
    ideology: dict[unquotedInt, unquotedFiveSigFigDecimal]
    issues: dict[unquotedInt, unquotedFiveSigFigDecimal]
    con: unquotedFiveSigFigDecimal
    literacy: unquotedFiveSigFigDecimal
    bank: unquotedFiveSigFigDecimal
    con_factor: unquotedFiveSigFigDecimal
    demoted: unquotedInt
    promoted: unquotedInt
    life_needs: unquotedFiveSigFigDecimal
    everyday_needs: unquotedFiveSigFigDecimal
    luxury_needs: unquotedFiveSigFigDecimal
    size_changes: list[unquotedInt]
    converted: unquotedInt
    random: unquotedInt
    faction: Identifier
    local_migration: unquotedInt
    external_migration: unquotedInt
    movement_tag: quotedTag
    colonial_migration: unquotedInt
    assimilated: unquotedInt


class Worker(Pop):
    days_of_loss: unquotedInt


class Artisans(Pop):
    production_type: str
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    need: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    last_spending: unquotedFiveSigFigDecimal
    current_producing: unquotedFiveSigFigDecimal
    percent_afforded: unquotedFiveSigFigDecimal
    percent_sold_domestic: unquotedFiveSigFigDecimal
    percent_sold_export: unquotedFiveSigFigDecimal
    leftover: unquotedFiveSigFigDecimal
    throttle: unquotedFiveSigFigDecimal
    needs_cost: unquotedFiveSigFigDecimal
    production_income: unquotedFiveSigFigDecimal
    con_factor: unquotedFiveSigFigDecimal


class EmployeeData(BaseModel):
    province_pop_id: Repeated[RepeatedKeyIndicator | IndexedIdentifier]
    count: unquotedInt


class Employment(BaseModel):
    province_id: unquotedInt
    employees: EmployeeData
    last_income: unquotedFiveSigFigDecimal
    goods_type: str


class UnitNameData(BaseModel):
    # need more verification on this one
    # very unclear how it works
    count: unquotedInt
    id: list[unquotedInt]


class PartyLoyalty(BaseModel):
    ideology: str
    loyalty_value: unquotedFiveSigFigDecimal


class BuildingConstruction(BaseModel):
    id: Identifier
    state_date: quotedPDXDate
    date: quotedPDXDate
    location: Annotated[unquotedInt, "Province ID"]
    country: quotedTag
    building: unquotedInt


class MilitaryInputGoodsData(BaseModel):
    goods_demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    input_demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    money: unquotedFiveSigFigDecimal


class MilitaryConstruction(BaseModel):
    id: Identifier
    start_date: quotedPDXDate
    date: quotedPDXDate
    location: Annotated[unquotedInt, "Province ID"]
    country: quotedTag
    input_goods: MilitaryInputGoodsData
    name: str
    type: str
    unit: Identifier
    regiment: Identifier
    pop: Identifier
    count: unquotedInt
    rally_point: unquotedInt


class Province(BaseModel):
    name: quotedPDXVariable
    garrison: unquotedThreeSigFigDecimal
    owner: quotedTag
    controller: quotedTag
    core: Optional[Repeated[RepeatedKeyIndicator | quotedTag]]
    fort: Annotated[list[unquotedThreeSigFigDecimal], 2]
    railroad: Annotated[list[unquotedThreeSigFigDecimal], 2]
    naval_base: Annotated[list[unquotedThreeSigFigDecimal], 2]
    pops: list[Pop]
    rgo: Employment
    life_rating: unquotedInt
    infrastructure: unquotedThreeSigFigDecimal
    last_imigration: quotedPDXDate
    last_controller_change: quotedPDXDate
    unit_names: UnitNameData
    party_loyalty: Repeated[RepeatedKeyIndicator | PartyLoyalty]
    nationalism: unquotedThreeSigFigDecimal
    building_construction: Repeated[RepeatedKeyIndicator | BuildingConstruction]
    military_construction: Repeated[RepeatedKeyIndicator | MilitaryConstruction]
    crime: unquotedInt


"""
    @model_validator(mode="after")
    def validate_sea_province(self) -> "Province":
        # assuming that sea provinces never have rgos
        if not self.rgo:
            if validators.check_quoted_string(self.name):
                try:
                    validators.validate_3_sigfig_decimal(self.garrison)
                    return self
                except ValueError:
                    raise ValidationError(
                        "Garrison must be specified for sea provinces"
                    )
            else:
                raise ValidationError("Name must be specified for sea provinces")

"""


class Research(BaseModel):
    technology: unquotedTechnology
    cost: unquotedThreeSigFigDecimal
    max_producing: unquotedThreeSigFigDecimal
    last_spending: unquotedThreeSigFigDecimal
    active: PDXBoolean


class CountryModifier(BaseModel):
    modifier: str
    date: quotedPDXDate


class TaxBracket(BaseModel):
    current: unquotedFiveSigFigDecimal
    tax_income: list[unquotedFiveSigFigDecimal]
    tax_eff: list[unquotedFiveSigFigDecimal]
    total: unquotedFiveSigFigDecimal
    rangeLimitMax: unquotedFiveSigFigDecimal
    rangeLimitMin: unquotedFiveSigFigDecimal
    max_tax: unquotedInt
    min_tax: unquotedInt


class SpendingSetting(BaseModel):
    settings: unquotedFiveSigFigDecimal
    temp_settings: unquotedFiveSigFigDecimal
    factor: unquotedFiveSigFigDecimal
    reserve: unquotedFiveSigFigDecimal
    maxValue: unquotedFiveSigFigDecimal
    rangeLimitMax: unquotedFiveSigFigDecimal
    rangeLimitMin: unquotedFiveSigFigDecimal
    max_tax: unquotedInt
    min_tax: unquotedInt


class Leader(BaseModel):
    name: str
    date: quotedPDXDate
    type: Annotated[unquotedPDXVariable, "`land` or `sea`"]
    personality: str
    background: str
    country: quotedTag
    picture: str
    prestige: unquotedThreeSigFigDecimal
    id: Identifier


class Ship(BaseModel):
    id: Identifier
    name: str
    pop: Identifier
    organisation: unquotedThreeSigFigDecimal
    strength: unquotedThreeSigFigDecimal
    experience: unquotedThreeSigFigDecimal
    count: unquotedInt
    type: unquotedPDXVariable


class Regiment(Ship):
    pop: Identifier


class Army(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[unquotedInt, "Province ID"]
    movement_progress: unquotedThreeSigFigDecimal
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    regiment: Repeated[RepeatedKeyIndicator | Regiment]


class Navy(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[unquotedInt, "Province ID"]
    movement_progress: unquotedThreeSigFigDecimal
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    ship: Repeated[RepeatedKeyIndicator | Ship]


class ForeignRelation(BaseModel):
    value: unquotedInt
    last_send_diplomat: quotedPDXDate
    last_war: quotedPDXDate
    truce_until: quotedPDXDate
    level: unquotedInt
    level_changed_date: quotedPDXDate
    influence_value: unquotedThreeSigFigDecimal


class ProvinceDesire(BaseModel):
    id: unquotedInt
    value: unquotedInt


class DiplomaticAttitude(BaseModel):
    id: quotedTag
    value: unquotedInt


class AIStrategy(BaseModel):
    initialized: PDXBoolean
    consolidate: PDXBoolean
    date: quotedPDXDate
    static: PDXBoolean
    personality: unquotedPDXVariable
    conquer_prov: Repeated[RepeatedKeyIndicator | ProvinceDesire] | None
    threat: Repeated[RepeatedKeyIndicator | DiplomaticAttitude] | None
    antagonize: Repeated[RepeatedKeyIndicator | DiplomaticAttitude] | None
    befriend: Repeated[RepeatedKeyIndicator | DiplomaticAttitude] | None
    protect: Repeated[RepeatedKeyIndicator | DiplomaticAttitude] | None
    rival: Repeated[RepeatedKeyIndicator | DiplomaticAttitude] | None


class PoliticalMovement(BaseModel):
    support: unquotedInt
    cache: unquotedFiveSigFigDecimal


class IndependenceMovement(PoliticalMovement):
    tag: quotedTag


class PolicyMovement(PoliticalMovement):
    issue: str


class TradePolicy(BaseModel):
    limit: unquotedFiveSigFigDecimal
    buy: PDXBoolean
    automate_trade: PDXBoolean


class State(BaseModel):
    id: Identifier
    provinces: list[unquotedInt]
    is_colonial: unquotedInt
    savings: unquotedFiveSigFigDecimal
    interest: unquotedFiveSigFigDecimal
    flashpoint: PDXBoolean
    tension: unquotedThreeSigFigDecimal
    crisis: quotedTag


class NationalBank(BaseModel):
    money: unquotedFiveSigFigDecimal
    money_lent: unquotedFiveSigFigDecimal


class Railroad(BaseModel):
    path: list[Annotated[unquotedInt, "Province ID"]]


class Nation(BaseModel):
    human: PDXBoolean | None
    tax_base: unquotedFiveSigFigDecimal
    flags: dict[unquotedPDXVariable, PDXBoolean]
    variables: dict = {}
    capital: Annotated[unquotedInt, "Province ID"]
    research_points: unquotedThreeSigFigDecimal | None
    technology: dict[unquotedTechnology, Annotated[list, 2]]
    research: Research | None
    last_reform: quotedPDXDate | None
    last_election: quotedPDXDate
    wage_reform: unquotedPDXVariable
    work_hours: unquotedPDXVariable
    safety_regulations: unquotedPDXVariable
    unemployment_subsidies: unquotedPDXVariable
    pensions: unquotedPDXVariable
    health_care: unquotedPDXVariable
    school_reforms: unquotedPDXVariable
    slavery: unquotedPDXVariable
    vote_franschise: unquotedPDXVariable
    voting_system: unquotedPDXVariable
    public_meetings: unquotedPDXVariable
    press_rights: unquotedPDXVariable
    trade_unions: unquotedPDXVariable
    political_parties: unquotedPDXVariable
    upper_house: dict[unquotedIdeology, unquotedFiveSigFigDecimal]
    last_party_change: quotedPDXDate | None
    ruling_party: unquotedInt
    active_party: unquotedInt
    naval_need: Convoys | None
    land_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None
    naval_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None
    diplomatic_points: unquotedThreeSigFigDecimal
    religion: quotedPDXVariable
    government: unquotedPDXVariable
    plurality: unquotedThreeSigFigDecimal
    revanchism: unquotedThreeSigFigDecimal
    modifier: Repeated[RepeatedKeyIndicator | CountryModifier] | None
    poor_tax: TaxBracket
    middle_tax: TaxBracket
    rich_tax: TaxBracket
    education_spending: SpendingSetting
    crime_fighting: SpendingSetting
    social_spending: SpendingSetting
    military_spending: SpendingSetting
    overseas_penalty: unquotedFiveSigFigDecimal = Decimal(0.00000)
    leadership: unquotedFiveSigFigDecimal = Decimal(0.00000)
    auto_assign_leaders: PDXBoolean
    auto_create_leaders: PDXBoolean
    leader: Repeated[RepeatedKeyIndicator | Leader] | None
    army: Repeated[RepeatedKeyIndicator | Army] | None
    navy: Repeated[RepeatedKeyIndicator | Navy] | None
    relations: dict[unquotedTag, ForeignRelation] | None
    active_inventions: list[unquotedInt] | None
    possible_inventions: list[unquotedInt] | None
    illegal_inventions: list[unquotedInt]
    government_flag: dict[str, str]
    last_mission_cancel: quotedPDXDate = date(1, 1, 1)
    ai_hard_strategy: AIStrategy | None
    ai_strategy: AIStrategy | None
    foreign_investment: list[unquotedFiveSigFigDecimal] | None
    schools: quotedPDXVariable
    primary_culture: quotedPDXVariable
    culture: list[str] = []
    bank: NationalBank
    money: unquotedFiveSigFigDecimal
    last_bankrupt: quotedPDXDate = '"1.1.1"'
    prestige: unquotedThreeSigFigDecimal
    movement: Repeated[
        RepeatedKeyIndicator
        | Union[PoliticalMovement, IndependenceMovement, PolicyMovement]
    ] | None
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None
    national_value: quotedPDXVariable | None
    buy_domestic: dict = {}
    trade: dict[unquotedRGO, TradePolicy]
    civilized: PDXBoolean
    state: Repeated[RepeatedKeyIndicator | State] | None
    badboy: unquotedThreeSigFigDecimal
    trade_cap_land: unquotedFiveSigFigDecimal | None
    trade_cap_naval: unquotedFiveSigFigDecimal | None
    trade_cap_projects: unquotedFiveSigFigDecimal | None
    max_tariff: unquotedFiveSigFigDecimal | None
    domestic_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    sold_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    domestic_demand_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    actual_sold_domestic: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    saved_country_supply: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    max_bought: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    national_focus: dict[quotedInt, quotedPDXVariable]
    influence: dict[quotedTag, quotedInt] | None
    expenses: list[unquotedFiveSigFigDecimal]
    incomes: list[unquotedFiveSigFigDecimal]
    interesting_countries: list[unquotedInt] | None
    next_quarterly_pulse: quotedPDXDate
    next_yearly_pulse: quotedPDXDate
    suppression: unquotedThreeSigFigDecimal
    railroads: Repeated[RepeatedKeyIndicator | Railroad]
    is_releasable_vassal: PDXBoolean = "yes"


class RebelFaction(BaseModel):
    id: Identifier
    type: str
    name: str
    country: quotedTag
    independence: Union[quotedTag, Literal["---"]] = "---"
    culture: str
    religion: str
    government: str
    province: unquotedInt
    leader: Identifier
    organization: unquotedFiveSigFigDecimal
    pop: Repeated[RepeatedKeyIndicator | Identifier]


class Alliance(BaseModel):
    first: quotedTag
    second: quotedTag
    end_date: quotedPDXDate = '"1949.1.1"'
    start_date: quotedPDXDate = '"1795.1.1"'


class Vassalage(BaseModel):
    first: Annotated[quotedTag, "Overload"]
    second: Annotated[quotedTag, "Vassal"]
    end_date: quotedPDXDate = '"1949.1.1"'
    start_date: quotedPDXDate = '"1795.1.1"'


class CasusBelli(BaseModel):
    type: str
    first: quotedTag
    second: quotedTag
    start_date: quotedPDXDate


class Diplomacy(BaseModel):
    alliance: Optional[Repeated[RepeatedKeyIndicator | Alliance]]
    vassal: Optional[Repeated[RepeatedKeyIndicator | Vassalage]]
    substate: Optional[Repeated[RepeatedKeyIndicator | Vassalage]]
    casus_belli: Optional[Repeated[RepeatedKeyIndicator | CasusBelli]]


class Combatant(BaseModel):
    dice: unquotedInt
    unit: Repeated[RepeatedKeyIndicator | Identifier]
    losses: unquotedThreeSigFigDecimal
    accumulated_losses: list[unquotedThreeSigFigDecimal]
    front: dict[unquotedInt, Identifier]
    back: dict[unquotedInt, Identifier]


class LandCombatant(BaseModel):
    dice: unquotedInt
    unit: Repeated[RepeatedKeyIndicator | Identifier]
    losses: unquotedThreeSigFigDecimal
    accumulated_losses: list[unquotedThreeSigFigDecimal]
    front: dict[unquotedInt, Identifier]
    back: dict[unquotedInt, Identifier]
    reserves: Optional[Repeated[RepeatedKeyIndicator | Identifier]]
    irregular: unquotedThreeSigFigDecimal = Decimal(0.000)
    infantry: unquotedThreeSigFigDecimal = Decimal(0.000)
    guard: unquotedThreeSigFigDecimal = Decimal(0.000)
    cavalry: unquotedThreeSigFigDecimal = Decimal(0.000)
    cuirassier: unquotedThreeSigFigDecimal = Decimal(0.000)
    dragoon: unquotedThreeSigFigDecimal = Decimal(0.000)
    hussar: unquotedThreeSigFigDecimal = Decimal(0.000)
    airplane: unquotedThreeSigFigDecimal = Decimal(0.000)
    artillery: unquotedThreeSigFigDecimal = Decimal(0.000)
    engineer: unquotedThreeSigFigDecimal = Decimal(0.000)
    armor: unquotedThreeSigFigDecimal = Decimal(0.000)


class NavalCombatSlot(BaseModel):
    attacker: Identifier
    distance: unquotedThreeSigFigDecimal
    stance: unquotedInt
    total_damage_str: unquotedThreeSigFigDecimal
    total_damage_org: unquotedThreeSigFigDecimal
    icon: unquotedInt
    name: quotedPDXVariable
    killer_name: quotedPDXVariable = ""
    tag: quotedTag


class NavalCombatant(Combatant):
    naval_combat_slot: Repeated[RepeatedKeyIndicator | NavalCombatSlot]
    penalty_factor: unquotedThreeSigFigDecimal
    # TODO: list out unit keys like in LandCombatant


class Siege(BaseModel):
    location: Annotated[unquotedInt, "Province Id"]
    day: unquotedInt = -1
    duration: unquotedInt = 0
    attacker: Combatant = {}
    defender: Combatant = {}
    total: unquotedInt


class LandBattle(BaseModel):
    location: Annotated[unquotedInt, "Province Id"]
    day: unquotedInt
    duration: unquotedInt
    attacker: LandCombatant
    defender: LandCombatant


class NavalBattle(BaseModel):
    location: Annotated[unquotedInt, "Province Id"]
    day: unquotedInt
    duration: unquotedInt
    attacker: NavalCombatant
    defender: NavalCombatant


class Combat(BaseModel):
    siege_combat: Optional[Repeated[RepeatedKeyIndicator | Siege] | Siege]
    land_combat: Optional[Repeated[RepeatedKeyIndicator | LandBattle] | LandBattle]
    naval_combat: Optional[Repeated[RepeatedKeyIndicator | NavalBattle] | NavalBattle]


class Colony(BaseModel):
    tag: quotedTag
    points: unquotedInt
    invest: unquotedInt
    date: quotedPDXDate


class Region(BaseModel):
    index: unquotedInt
    phase: unquotedInt
    date: Optional[quotedPDXDate]
    temperature: unquotedThreeSigFigDecimal


class VicIISave(BaseModel):
    date: quotedPDXDate
    player: quotedTag
    government: unquotedInt
    automate_trade: PDXBoolean
    automate_sliders: unquotedInt
    rebel: unquotedInt
    unit: unquotedInt
    state: unquotedInt
    flags: dict[unquotedPDXVariable, PDXBoolean]
    gameplaysettings: dict[Literal["setgameplayoptions"], list[unquotedInt]]
    start_date: quotedPDXDate
    start_pop_index: unquotedInt
    worldmarket: WorldMarket
    great_wars_enabled: PDXBoolean
    world_wars_enabled: PDXBoolean
    overseas_penalty: Convoys
    unit_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    budget_balance: list[unquotedFiveSigFigDecimal]
    player_monthly_pop_growth: Annotated[list[unquotedInt], 30]
    player_monthly_pop_growth_tag: quotedTag
    player_monthly_pop_growth_date: quotedPDXDate
    fascist: IdeologyEnabled
    socialist: IdeologyEnabled
    communist: IdeologyEnabled
    anarcho_liberal: IdeologyEnabled
    canals: list[unquotedInt]
    id: Repeated[RepeatedKeyIndicator | Identifier] | Identifier
    fired_events: FiredEvent
    province_data: Annotated[dict[unquotedInt, Province], "Collapse by one level"]
    nation_data: Annotated[dict[unquotedTag, Nation], "Collapse by one level"]
    rebel_faction: Repeated[RepeatedKeyIndicator | RebelFaction]
    diplomacy: Diplomacy
    combat: Combat

    # TODO: active_war
    # TODO: previous_war
    inventions: Optional[list[unquotedInt]]
    great_nations: Annotated[list[unquotedInt], 8]
    outliner: list[unquotedInt]
    # TODO: news_collector, need to add support for parsing strings first
    region: Repeated[RepeatedKeyIndicator | Region]
