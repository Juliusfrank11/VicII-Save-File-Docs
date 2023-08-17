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
        extra = Extra.forbid


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
    this_is_a_repeated_key_please_collapse_down: bool = True


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
    enabled: quotedPDXDate | None = None


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
    mil: unquotedFiveSigFigDecimal
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


class Artisan(Worker):
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


class ProvincePopId(BaseModel):
    province_id: unquotedInt
    index: unquotedInt
    type: unquotedInt


class EmployeeData(BaseModel):
    province_pop_id: Repeated[RepeatedKeyIndicator | ProvincePopId] | ProvincePopId
    count: unquotedInt


class ProvinceEmployment(BaseModel):
    province_id: unquotedInt
    employees: EmployeeData


class StateEmployment(BaseModel):
    state_province_id: unquotedInt
    employees: EmployeeData


class RGO(BaseModel):
    employment: ProvinceEmployment
    last_income: unquotedFiveSigFigDecimal
    goods_type: quotedPDXVariable


class UnitNameData(BaseModel):
    # need more verification on this one
    # very unclear how it works
    count: unquotedInt | None = None
    id: list[unquotedInt] | None = None


class UnitNames(BaseModel):
    data: UnitNameData


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
    input_demand: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    input_goods: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    money: unquotedFiveSigFigDecimal


class MilitaryConstruction(BaseModel):
    id: Identifier
    start_date: quotedPDXDate
    date: quotedPDXDate
    location: Annotated[unquotedInt, "Province ID"]
    country: quotedTag
    input_goods: MilitaryInputGoodsData | None = None
    name: str
    type: str
    unit: Identifier
    regiment: Identifier
    pop: Identifier | None = None
    count: unquotedInt
    rally_point: unquotedInt


class Modifier(BaseModel):
    modifier: quotedPDXVariable
    date: quotedPDXDate


class Province(BaseModel):
    name: quotedPDXVariable
    garrison: unquotedThreeSigFigDecimal
    owner: quotedTag | None = None
    controller: quotedTag | None = None
    core: Repeated[RepeatedKeyIndicator | quotedTag] | None = None
    fort: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    railroad: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    naval_base: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    craftsmen: list[Worker | RepeatedKeyIndicator] | Worker | None = None
    farmers: list[Worker | RepeatedKeyIndicator] | Worker | None = None
    labourers: list[Worker | RepeatedKeyIndicator] | Worker | None = None
    slaves: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    soldiers: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    artisans: list[Artisan | RepeatedKeyIndicator] | Artisan | None = None
    bureaucrats: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    clergymen: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    clerks: list[Worker | RepeatedKeyIndicator] | Worker | None = None
    officers: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    aristocrats: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    capitalists: list[Pop | RepeatedKeyIndicator] | Pop | None = None
    rgo: RGO | None = None
    modifier: Repeated[RepeatedKeyIndicator | Modifier] | Modifier | None = None
    life_rating: unquotedInt | None = None
    infrastructure: unquotedThreeSigFigDecimal | None = None
    last_imigration: quotedPDXDate | None = None
    last_controller_change: quotedPDXDate | None = None
    unit_names: UnitNames | None = None
    party_loyalty: Repeated[RepeatedKeyIndicator | PartyLoyalty] | None = None
    nationalism: unquotedThreeSigFigDecimal | None = None
    building_construction: Repeated[
        RepeatedKeyIndicator | BuildingConstruction
    ] | None = None
    military_construction: Repeated[
        RepeatedKeyIndicator | MilitaryConstruction
    ] | None = None
    crime: unquotedInt | None = None
    colonial: unquotedInt

    @classmethod
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


class Research(BaseModel):
    technology: unquotedTechnology
    cost: unquotedThreeSigFigDecimal
    max_producing: unquotedThreeSigFigDecimal
    last_spending: unquotedThreeSigFigDecimal
    active: PDXBoolean


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
    pop: Identifier | None = None
    organisation: unquotedThreeSigFigDecimal
    strength: unquotedThreeSigFigDecimal
    experience: unquotedThreeSigFigDecimal | None = None
    count: unquotedInt | None = None
    type: unquotedPDXVariable


class Regiment(Ship):
    pop: Identifier
    current_distance: unquotedThreeSigFigDecimal


class Army(BaseModel):
    id: Identifier
    name: str
    leader: Identifier | None = None
    previous: Annotated[unquotedInt, "Province ID"] | None = None
    movement_progress: unquotedThreeSigFigDecimal | None = None
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    regiment: Repeated[RepeatedKeyIndicator | Regiment]
    base: unquotedInt
    path: list[unquotedInt] | None = None
    dig_in: unquotedThreeSigFigDecimal | None = None
    target: unquotedInt


class Navy(BaseModel):
    id: Identifier
    name: str
    leader: Identifier | None = None
    previous: Annotated[unquotedInt, "Province ID"] | None = None
    movement_progress: unquotedThreeSigFigDecimal | None = None
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    ship: Repeated[RepeatedKeyIndicator | Ship]
    at_sea: unquotedInt | None = "0"
    no_supply_days: unquotedInt | None = "0"
    path: list[unquotedInt] | None = None
    army: Army | None = None


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


class BuildingProvGoal(ProvinceDesire):
    key: quotedPDXVariable


class AIStrategy(BaseModel):
    initialized: PDXBoolean
    consolidate: PDXBoolean
    date: quotedPDXDate
    static: PDXBoolean
    personality: unquotedPDXVariable
    conquer_prov: Repeated[
        RepeatedKeyIndicator | ProvinceDesire
    ] | ProvinceDesire | None = None
    threat: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    antagonize: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    befriend: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    protect: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    rival: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    war_with: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    building_prov: Repeated[
        RepeatedKeyIndicator | BuildingProvGoal
    ] | BuildingProvGoal | None = None
    military_access: Repeated[
        RepeatedKeyIndicator | DiplomaticAttitude
    ] | DiplomaticAttitude | None = None
    status: unquotedInt | None = None


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


class PopProject(BaseModel):
    input_goods: dict[unquotedRGO, unquotedFiveSigFigDecimal] = {}
    money: unquotedThreeSigFigDecimal
    building: unquotedInt
    province: unquotedInt
    index: unquotedInt
    type: unquotedInt
    money2: PDXBoolean = "yes"  # AAAAAAAAAAAAAA
    pop: unquotedInt


class StateBuilding(BaseModel):
    building: quotedPDXVariable
    level: unquotedInt
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    employment: StateEmployment
    money: unquotedFiveSigFigDecimal
    last_spending: unquotedFiveSigFigDecimal
    last_income: unquotedFiveSigFigDecimal
    pops_paychecks: unquotedFiveSigFigDecimal
    last_investment: unquotedFiveSigFigDecimal
    unprofitable_days: unquotedInt
    leftover: unquotedFiveSigFigDecimal
    injected_money: unquotedFiveSigFigDecimal
    injected_days: unquotedInt
    produces: unquotedFiveSigFigDecimal
    profit_history_days: unquotedInt
    profit_history_current: unquotedInt
    profit_history_entry: list[unquotedFiveSigFigDecimal]
    subsidised: PDXBoolean | None = "no"
    priority: unquotedInt | None = None
    construction_time_left: unquotedInt | None = None
    days_without_input: unquotedInt | None = None


class State(BaseModel):
    id: Identifier
    name: quotedPDXVariable | None = None
    provinces: list[unquotedInt]
    is_colonial: unquotedInt | None = None
    savings: unquotedFiveSigFigDecimal
    interest: unquotedFiveSigFigDecimal
    flashpoint: PDXBoolean | None = None
    tension: unquotedThreeSigFigDecimal | None = None
    crisis: quotedTag | None = None
    is_slave: PDXBoolean | None = "no"
    popproject: PopProject | None = None
    state_buildings: Repeated[
        RepeatedKeyIndicator | StateBuilding
    ] | StateBuilding | None = None


class NationalBank(BaseModel):
    money: unquotedFiveSigFigDecimal
    money_lent: unquotedFiveSigFigDecimal


class Railroad(BaseModel):
    path: list[Annotated[unquotedInt, "Province ID"]]


class Creditor(BaseModel):
    country: quotedTag
    interest: unquotedFiveSigFigDecimal
    debt: unquotedFiveSigFigDecimal
    was_paid: PDXBoolean


class ScheduledMobilization(BaseModel):
    progress: unquotedThreeSigFigDecimal
    location: unquotedInt
    from_province: unquotedInt
    sub_unit: unquotedInt
    pop: Identifier
    spawned: PDXBoolean
    country: quotedTag
    active: PDXBoolean
    rally_point: unquotedInt


class Nation(BaseModel):
    human: PDXBoolean | None = "no"
    tax_base: unquotedFiveSigFigDecimal
    flags: dict[unquotedPDXVariable, PDXBoolean]
    variables: dict = {}
    capital: Annotated[unquotedInt, "Province ID"]
    research_points: unquotedThreeSigFigDecimal | None = None
    technology: dict[unquotedTechnology, Annotated[list, 2]]
    research: Research | None = None
    last_reform: quotedPDXDate | None = None
    last_election: quotedPDXDate
    wage_reform: unquotedPDXVariable
    upper_house_composition: unquotedPDXVariable
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
    admin_reform: unquotedPDXVariable | None
    army_schools: unquotedPDXVariable | None
    education_reform: unquotedPDXVariable | None
    finance_reform: unquotedPDXVariable | None
    foreign_naval_officers: unquotedPDXVariable | None
    foreign_navies: unquotedPDXVariable | None
    foreign_officers: unquotedPDXVariable | None
    foreign_training: unquotedPDXVariable | None
    foreign_weapons: unquotedPDXVariable | None
    industrial_construction: unquotedPDXVariable | None
    land_reform: unquotedPDXVariable | None
    military_constructions: unquotedPDXVariable | None
    naval_schools: unquotedPDXVariable | None
    pre_indust: unquotedPDXVariable | None
    tariffs: unquotedPDXVariable | None
    transport_improv: unquotedPDXVariable | None
    upper_house: dict[unquotedIdeology, unquotedFiveSigFigDecimal]
    last_party_change: quotedPDXDate | None = None
    ruling_party: unquotedInt | None = None
    active_party: unquotedInt | None = None
    naval_need: Convoys | None = None
    land_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    naval_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    diplomatic_points: unquotedThreeSigFigDecimal
    religion: quotedPDXVariable
    government: unquotedPDXVariable | None = None
    plurality: unquotedThreeSigFigDecimal
    revanchism: unquotedThreeSigFigDecimal
    modifier: Repeated[RepeatedKeyIndicator | Modifier] | None = None
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
    leader: Repeated[RepeatedKeyIndicator | Leader] | None = None
    army: Repeated[RepeatedKeyIndicator | Army] | None = None
    navy: Repeated[RepeatedKeyIndicator | Navy] | None = None
    relations: dict[unquotedTag, ForeignRelation] | None = None
    active_inventions: list[unquotedInt] | None = None
    possible_inventions: list[unquotedInt] | None = None
    illegal_inventions: list[unquotedInt]
    government_flag: dict[str, str]
    last_mission_cancel: quotedPDXDate = date(1, 1, 1)
    ai_hard_strategy: AIStrategy | None = None
    ai: AIStrategy | None = None
    foreign_investment: list[unquotedFiveSigFigDecimal] | None = None
    schools: quotedPDXVariable
    primary_culture: quotedPDXVariable | None = None
    culture: list[quotedPDXVariable] = []
    bank: NationalBank
    money: unquotedFiveSigFigDecimal
    last_bankrupt: quotedPDXDate = '"1.1.1"'
    prestige: unquotedThreeSigFigDecimal
    movement: Repeated[
        RepeatedKeyIndicator
        | Union[PoliticalMovement, IndependenceMovement, PolicyMovement]
    ] | None = None
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    national_value: quotedPDXVariable | None = None
    buy_domestic: dict = {}
    trade: dict[unquotedRGO, TradePolicy]
    civilized: PDXBoolean
    state: Repeated[RepeatedKeyIndicator | State] | None = None
    badboy: unquotedThreeSigFigDecimal
    trade_cap_land: unquotedFiveSigFigDecimal | None = None
    trade_cap_naval: unquotedFiveSigFigDecimal | None = None
    trade_cap_projects: unquotedFiveSigFigDecimal | None = None
    max_tariff: unquotedFiveSigFigDecimal | None = None
    domestic_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    sold_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    domestic_demand_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    actual_sold_domestic: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    saved_country_supply: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    max_bought: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    national_focus: dict[quotedInt, quotedPDXVariable]
    influence: dict[quotedTag, quotedInt] | None = None
    expenses: list[unquotedFiveSigFigDecimal]
    incomes: list[unquotedFiveSigFigDecimal]
    interesting_countries: list[unquotedInt] | None = None
    next_quarterly_pulse: quotedPDXDate
    next_yearly_pulse: quotedPDXDate
    suppression: unquotedThreeSigFigDecimal
    railroads: Repeated[RepeatedKeyIndicator | Railroad] | Railroad | None = None
    is_releasable_vassal: PDXBoolean = "yes"
    nationalvalue: quotedPDXVariable
    creditor: Repeated[RepeatedKeyIndicator | Creditor] | Creditor | None = None
    last_greatness_date: quotedPDXDate | None = None
    mobilize: PDXBoolean | None = None
    colonize: dict[unquotedInt, unquotedInt] | None = None
    war_exhaustion: unquotedThreeSigFigDecimal
    scheduled_mobilization: Repeated[
        RepeatedKeyIndicator | ScheduledMobilization
    ] | ScheduledMobilization | None = None

    @classmethod
    @model_validator(mode="after")
    def validate_non_REB(self) -> "Province":
        # REB has no government
        government_having_list = [
            self.ruling_party,
            self.active_party,
            self.government,
            self.primary_culture,
        ]
        if any(government_having_list):
            if not all(government_having_list):
                raise ValidationError(
                    "You must have a government if you are not a rebel! As in, `ruling_party`, `active_party`, `government` and `primary_culture` must be defined"
                )
            return self

    # TODO: add validator for countries that currently exist


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
    next_unit: unquotedInt


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
    alliance: Repeated[RepeatedKeyIndicator | Alliance] | None = None
    vassal: Repeated[RepeatedKeyIndicator | Vassalage] | None = None
    substate: Repeated[RepeatedKeyIndicator | Vassalage] | None = None
    casus_belli: Repeated[RepeatedKeyIndicator | CasusBelli] | None = None


class Combatant(BaseModel):
    dice: unquotedInt
    unit: Repeated[RepeatedKeyIndicator | Identifier] | Identifier | None = None
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
    reserves: Repeated[RepeatedKeyIndicator | Identifier] | Identifier | None = None
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
    attacker: Combatant | None = {}
    defender: Combatant | None = {}
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
    siege_combat: Repeated[RepeatedKeyIndicator | Siege] | Siege | None = None
    land_combat: Repeated[RepeatedKeyIndicator | LandBattle] | LandBattle | None = None
    naval_combat: Repeated[
        RepeatedKeyIndicator | NavalBattle
    ] | NavalBattle | None = None


class Colony(BaseModel):
    tag: quotedTag
    points: unquotedInt
    invest: unquotedInt
    date: quotedPDXDate


class Region(BaseModel):
    index: unquotedInt
    phase: unquotedInt
    date: quotedPDXDate | None = None
    temperature: unquotedThreeSigFigDecimal
    colony: Repeated[RepeatedKeyIndicator | Colony] | Colony | None = None


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
    inventions: list[unquotedInt] | None = None
    great_nations: Annotated[list[unquotedInt], 8]
    outliner: list[unquotedInt]
    # TODO: news_collector, need to add support for parsing strings first
    region: Repeated[RepeatedKeyIndicator | Region]
