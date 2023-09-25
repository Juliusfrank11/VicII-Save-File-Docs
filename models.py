from pydantic import (
    BaseModel as PydanticBaseModel,
    model_validator,
    field_validator,
    ValidationError,
    BeforeValidator,
    AfterValidator,
)
from datetime import date
from typing import Annotated, Literal, Union, Optional
from decimal import Decimal
import validators

from pydantic import Extra


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid


# TODO: change name of Identifier because parser uses it to refer to unquotedPDXVariable

# pesudo-primitive" PDX-exclusive classes
Repeated = list  # used for keys that repeat
PDXBoolean = Union[Literal["yes"], Literal["no"]]

repeated_key_indicator = Literal["this_is_a_repeated_key_please_collapse_down"]
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


def handle_singleton_repeated_key(d: dict | None):
    if isinstance(d, dict):
        if repeated_key_indicator not in d.keys():
            return {repeated_key_indicator: [d]}
    return d


class Convoys(BaseModel):
    clipper_convoy: unquotedFiveSigFigDecimal | None = None
    steamer_convoy: unquotedFiveSigFigDecimal | None = None


class WorldMarket(BaseModel):
    worldmarket_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    price_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    last_price_history: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    last_supply_pool: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    price_history: dict[
        repeated_key_indicator, list[dict[unquotedRGO, unquotedFiveSigFigDecimal]]
    ]
    price_history_last_update: quotedPDXDate
    price_change: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    discovered_goods: dict[unquotedRGO, float]
    actual_sold: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    actual_sold_world: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    real_demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    demand: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    player_balance: dict[unquotedRGO, unquotedFiveSigFigDecimal]
    player_pops_consumption_cache: dict[
        repeated_key_indicator, list[dict[unquotedRGO, unquotedFiveSigFigDecimal]]
    ]

    @classmethod
    @field_validator("price_history", "price_history")
    def handle_not_repeated(cls, v: dict):
        return handle_singleton_repeated_key(v)


class IdeologyEnabled(BaseModel):
    enable: quotedPDXDate | None = None


class Identifier(BaseModel):
    id: unquotedInt
    type: unquotedInt


class IndexedIdentifier(Identifier):
    index: unquotedInt


class FiredEvent(BaseModel):
    id: dict[repeated_key_indicator, list[Identifier]]

    @classmethod
    @field_validator("id")
    def handle_repeated_keys(cls, v):
        if isinstance(v, dict):
            return


class Culture(BaseModel):
    name: unquotedPDXVariable
    religion: unquotedPDXVariable


class Pop(BaseModel):
    id: unquotedInt
    pop_type: unquotedPDXVariable | None = None
    size: unquotedInt
    culture: Culture
    money: unquotedFiveSigFigDecimal
    ideology: dict[unquotedInt, unquotedFiveSigFigDecimal]
    issues: dict[unquotedInt, unquotedFiveSigFigDecimal]
    mil: unquotedFiveSigFigDecimal | None = None
    con: unquotedFiveSigFigDecimal | None = None
    literacy: unquotedFiveSigFigDecimal
    bank: unquotedFiveSigFigDecimal | None = None
    con_factor: unquotedFiveSigFigDecimal | None = None
    demoted: unquotedInt | None = None
    promoted: unquotedInt | None = None
    life_needs: unquotedFiveSigFigDecimal | None = None
    everyday_needs: unquotedFiveSigFigDecimal | None = None
    luxury_needs: unquotedFiveSigFigDecimal | None = None
    size_changes: list[unquotedInt] | None = None
    converted: unquotedInt | None = None
    random: unquotedInt
    faction: Identifier | None = None
    local_migration: unquotedInt | None = None
    external_migration: unquotedInt | None = None
    movement_tag: quotedTag | None = None
    colonial_migration: unquotedInt | None = None
    assimilated: unquotedInt | None = None
    movement_issue: quotedPDXVariable | None = None
    days_of_loss: unquotedInt | None = None


class Artisan(Pop):
    production_type: str | None = None
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    need: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    last_spending: unquotedFiveSigFigDecimal
    current_producing: unquotedFiveSigFigDecimal
    percent_afforded: unquotedFiveSigFigDecimal
    percent_sold_domestic: unquotedFiveSigFigDecimal
    percent_sold_export: unquotedFiveSigFigDecimal
    leftover: unquotedFiveSigFigDecimal
    throttle: unquotedFiveSigFigDecimal
    needs_cost: unquotedFiveSigFigDecimal
    production_income: unquotedFiveSigFigDecimal


class ProvincePopId(BaseModel):
    province_id: unquotedInt
    index: unquotedInt
    type: unquotedInt


class EmployeeData(BaseModel):
    province_pop_id: dict[repeated_key_indicator, list[ProvincePopId]]
    count: unquotedInt

    @classmethod
    @field_validator("province_pop_id")
    def handle_not_repated(cls, v: dict):
        return handle_singleton_repeated_key(v)


class ProvinceEmployment(BaseModel):
    province_id: unquotedInt
    employees: EmployeeData | None = None


class StateEmployment(BaseModel):
    state_province_id: unquotedInt
    employees: EmployeeData | None = None


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
    state_date: quotedPDXDate | None = None
    date: quotedPDXDate
    location: Annotated[unquotedInt, "Province ID"]
    country: quotedTag
    building: unquotedInt
    start_date: quotedPDXDate
    input_goods: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None


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
    name: quotedPDXVariable
    type: quotedPDXVariable
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
    core: dict[repeated_key_indicator, list[quotedTag]] | None = None
    fort: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    railroad: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    naval_base: Annotated[list[unquotedThreeSigFigDecimal], 2] | None = None
    craftsmen: dict[repeated_key_indicator, list[Pop]] | None = None
    farmers: dict[repeated_key_indicator, list[Pop]] | None = None
    labourers: dict[repeated_key_indicator, list[Pop]] | None = None
    slaves: dict[repeated_key_indicator, list[Pop]] | None = None
    soldiers: dict[repeated_key_indicator, list[Pop]] | None = None
    artisans: dict[repeated_key_indicator, list[Artisan]] | None = None
    bureaucrats: dict[repeated_key_indicator, list[Pop]] | None = None
    clergymen: dict[repeated_key_indicator, list[Pop]] | None = None
    clerks: dict[repeated_key_indicator, list[Pop]] | None = None
    officers: dict[repeated_key_indicator, list[Pop]] | None = None
    aristocrats: dict[repeated_key_indicator, list[Pop]] | None = None
    capitalists: dict[repeated_key_indicator, list[Pop]] | None = None
    rgo: RGO | None = None
    modifier: dict[repeated_key_indicator, list[Modifier]] | None = None
    life_rating: unquotedInt | None = None
    infrastructure: unquotedThreeSigFigDecimal | None = None
    last_imigration: quotedPDXDate | None = None  # misspelling of last_immigration
    last_controller_change: quotedPDXDate | None = None
    unit_names: UnitNames | None = None
    party_loyalty: dict[repeated_key_indicator, list[PartyLoyalty]] | None = None
    nationalism: unquotedThreeSigFigDecimal | None = None
    building_construction: dict[
        repeated_key_indicator, list[BuildingConstruction]
    ] | None = None
    military_construction: dict[
        repeated_key_indicator, list[MilitaryConstruction]
    ] | None = None
    crime: unquotedInt | None = None
    colonial: unquotedInt | None = None
    flags: dict[unquotedPDXVariable, PDXBoolean] | None = None

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

    @classmethod
    @field_validator(
        "artisans",
        "core",
        "craftsmen",
        "farmers",
        "labourers",
        "slaves",
        "soldiers",
        "artisans",
        "bureaucrats",
        "clergymen",
        "clerks",
        "officers",
        "aristocrats",
        "capitalists",
        "modifier",
        "party_loyalty",
        "building_construction",
        "military_construction",
    )
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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
    current_distance: unquotedThreeSigFigDecimal | None = None


class Regiment(Ship):
    pop: Identifier


class Army(BaseModel):
    id: Identifier
    name: str
    leader: Identifier | None = None
    previous: Annotated[unquotedInt, "Province ID"] | None = None
    movement_progress: unquotedThreeSigFigDecimal | None = None
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    regiment: dict[repeated_key_indicator, list[Regiment]]
    base: unquotedInt | None = None
    path: list[unquotedInt] | None = None
    dig_in: unquotedThreeSigFigDecimal | None = None
    target: unquotedInt | None = None

    @classmethod
    @field_validator("regiment")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class Navy(BaseModel):
    id: Identifier
    name: str
    leader: Identifier | None = None
    previous: Annotated[unquotedInt, "Province ID"] | None = None
    movement_progress: unquotedThreeSigFigDecimal | None = None
    location: Annotated[unquotedInt, "Province ID"]
    dig_in_last_date: quotedPDXDate = "2.1.1"
    supplies: unquotedThreeSigFigDecimal
    ship: dict[repeated_key_indicator, list[Ship]] | None = None
    at_sea: unquotedInt | None = "0"
    no_supply_days: unquotedInt | None = "0"
    path: list[unquotedInt] | None = None
    army: Army | None = None

    @classmethod
    @field_validator("ship")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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
    conquer_prov: dict[repeated_key_indicator, list[ProvinceDesire]] | None = None
    threat: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    antagonize: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    befriend: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    protect: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    rival: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    war_with: dict[repeated_key_indicator, list[DiplomaticAttitude]] | None = None
    building_prov: dict[repeated_key_indicator, list[BuildingProvGoal]] | None = None
    military_access: dict[
        repeated_key_indicator, list[DiplomaticAttitude]
    ] | None = None
    status: unquotedInt | None = None

    @classmethod
    @field_validator(
        "conquer_prov",
        "threat",
        "antagonize",
        "befriend",
        "protect",
        "rival",
        "war_with",
        "building_prov",
        "military_access",
    )
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class PoliticalMovement(BaseModel):
    support: unquotedInt
    cache: unquotedFiveSigFigDecimal


class IndependenceMovement(PoliticalMovement):
    tag: quotedTag


class PolicyMovement(PoliticalMovement):
    issue: quotedPDXVariable
    radicalism: unquotedFiveSigFigDecimal


class TradePolicy(BaseModel):
    limit: unquotedFiveSigFigDecimal
    buy: PDXBoolean
    automate_trade: PDXBoolean


class PopProject(BaseModel):
    input_goods: dict[unquotedRGO, unquotedFiveSigFigDecimal] = {}
    money: unquotedFiveSigFigDecimal
    building: unquotedInt
    province: unquotedInt | None = None
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
    input_goods: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None


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
    state_buildings: dict[repeated_key_indicator, list[StateBuilding]] | None = None

    @classmethod
    @field_validator("state_buildings")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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


class DiplomaticAction(BaseModel):
    type: unquotedInt
    actor: quotedTag
    recipient: quotedTag
    date: quotedPDXDate
    last_command_date: quotedPDXDate


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
    election: quotedPDXDate | None = None
    campaign_counter: unquotedInt | None = None
    wage_reform: unquotedPDXVariable
    upper_house_composition: unquotedPDXVariable
    work_hours: unquotedPDXVariable
    safety_regulations: unquotedPDXVariable
    unemployment_subsidies: unquotedPDXVariable
    pensions: unquotedPDXVariable
    health_care: unquotedPDXVariable
    school_reforms: unquotedPDXVariable
    slavery: unquotedPDXVariable
    vote_franschise: unquotedPDXVariable  # misspelling franchise
    voting_system: unquotedPDXVariable
    public_meetings: unquotedPDXVariable
    press_rights: unquotedPDXVariable
    trade_unions: unquotedPDXVariable
    political_parties: unquotedPDXVariable
    admin_reform: unquotedPDXVariable | None = None
    army_schools: unquotedPDXVariable | None = None
    education_reform: unquotedPDXVariable | None = None
    finance_reform: unquotedPDXVariable | None = None
    foreign_naval_officers: unquotedPDXVariable | None = None
    foreign_navies: unquotedPDXVariable | None = None
    foreign_officers: unquotedPDXVariable | None = None
    foreign_training: unquotedPDXVariable | None = None
    foreign_weapons: unquotedPDXVariable | None = None
    industrial_construction: unquotedPDXVariable | None = None
    land_reform: unquotedPDXVariable | None = None
    military_constructions: unquotedPDXVariable | None = None
    naval_schools: unquotedPDXVariable | None = None
    pre_indust: unquotedPDXVariable | None = None
    tariffs: unquotedPDXVariable | None = None
    transport_improv: unquotedPDXVariable | None = None
    upper_house: dict[unquotedIdeology, unquotedFiveSigFigDecimal]
    last_party_change: quotedPDXDate | None = None
    ruling_party: unquotedInt | None = None
    active_party: unquotedInt | None = None
    naval_need: Convoys | None = None
    land_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    naval_supply_cost: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    diplomatic_points: unquotedThreeSigFigDecimal | None = None
    religion: quotedPDXVariable
    government: unquotedPDXVariable | None = None
    plurality: unquotedThreeSigFigDecimal
    revanchism: unquotedThreeSigFigDecimal
    modifier: dict[repeated_key_indicator, list[Modifier]] | None = None
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
    leader: dict[repeated_key_indicator, list[Leader]] | None = None
    army: dict[repeated_key_indicator, list[Army]] | None = None
    navy: dict[repeated_key_indicator, list[Navy]] | None = None
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
    movement: dict[
        repeated_key_indicator,
        Union[PoliticalMovement, IndependenceMovement, PolicyMovement],
    ] | None = None
    stockpile: dict[unquotedRGO, unquotedFiveSigFigDecimal] | None = None
    national_value: quotedPDXVariable | None = None
    buy_domestic: dict = {}
    trade: dict[unquotedRGO, TradePolicy]
    civilized: PDXBoolean
    state: dict[repeated_key_indicator, list[State]] | None = None
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
    railroads: dict[repeated_key_indicator, list[Railroad]] | None = None
    is_releasable_vassal: PDXBoolean = "yes"
    nationalvalue: quotedPDXVariable
    creditor: dict[repeated_key_indicator, list[Creditor]] | None = None
    last_greatness_date: quotedPDXDate | None = None
    mobilize: PDXBoolean | None = None
    colonize: dict[unquotedInt, unquotedInt] | None = None
    war_exhaustion: unquotedThreeSigFigDecimal | None = None
    scheduled_mobilization: dict[
        repeated_key_indicator, list[ScheduledMobilization]
    ] | None = None
    last_lost_war: quotedPDXDate | None = None
    diplomatic_action: dict[unquotedPDXVariable, DiplomaticAction] | None = None
    domain_region: quotedPDXVariable | None = None

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

    @classmethod
    @field_validator(
        "modifier",
        "leader",
        "army",
        "navy",
        "movement",
        "state",
        "railroads",
        "creditor",
        "scheduled_mobilization",
    )
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)

    # TODO: add validator for countries that currently exist


class RebelUnitNames(BaseModel):
    count: unquotedInt
    id: list[unquotedInt] | None = None


class RebelFaction(BaseModel):
    id: Identifier
    type: quotedPDXVariable
    name: quotedPDXVariable
    country: quotedTag
    independence: Union[quotedTag, Literal["---"]] = "---"
    culture: quotedPDXVariable
    religion: quotedPDXVariable
    government: quotedPDXVariable
    province: unquotedInt
    leader: Identifier
    organization: unquotedFiveSigFigDecimal
    pop: dict[repeated_key_indicator, list[Identifier]]
    next_unit: unquotedInt
    unit_names: dict[Literal["data"], RebelUnitNames] | None = None
    provinces: list[unquotedInt] | None = None
    army: dict[repeated_key_indicator, list[Identifier]] | None = None

    @classmethod
    @field_validator("army")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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


class PeaceOfferCondition(BaseModel):
    first: quotedTag
    second: quotedTag
    start_date: quotedPDXDate


class CasusBelli(BaseModel):
    type: str
    first: quotedTag
    second: quotedTag
    start_date: quotedPDXDate
    end_date: quotedPDXDate | None = None


class Diplomacy(BaseModel):
    alliance: dict[repeated_key_indicator, list[Alliance]] | None = None
    vassal: dict[repeated_key_indicator, list[Vassalage]] | None = None
    substate: dict[repeated_key_indicator, list[Vassalage]] | None = None
    casus_belli: dict[repeated_key_indicator, list[CasusBelli]] | None = None
    po_disarmament: dict[
        repeated_key_indicator, list[PeaceOfferCondition]
    ] | None = None
    reparations: dict[repeated_key_indicator, list[PeaceOfferCondition]] | None = None

    @classmethod
    @field_validator(
        "alliance",
        "vassal",
        "substate",
        "casus_belli",
        "po_disarmament",
        "reparations",
    )
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class Combatant(BaseModel):
    dice: unquotedInt
    unit: dict[repeated_key_indicator, list[Identifier]] | None = None
    losses: unquotedThreeSigFigDecimal
    accumulated_losses: list[unquotedThreeSigFigDecimal]
    front: dict[unquotedInt, Identifier]
    back: dict[unquotedInt, Identifier]
    retreat: Identifier | None = None

    @classmethod
    @field_validator("unit")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class LandCombatant(Combatant):
    reserves: dict[repeated_key_indicator, list[Identifier]] | None = None
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

    @classmethod
    @field_validator("reserves")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class NavalCombatSlot(BaseModel):
    attacker: Identifier
    defender: Identifier
    distance: unquotedThreeSigFigDecimal
    stance: unquotedInt
    total_damage_str: unquotedThreeSigFigDecimal
    total_damage_org: unquotedThreeSigFigDecimal
    icon: unquotedInt
    name: quotedPDXVariable
    killer_name: quotedPDXVariable = ""
    tag: quotedTag


class NavalCombatant(Combatant):
    naval_combat_slot: dict[repeated_key_indicator, list[NavalCombatSlot]]
    penalty_factor: unquotedThreeSigFigDecimal
    steam_transport: unquotedInt | None = None
    frigate: unquotedInt | None = None
    commerce_raider: unquotedInt | None = None
    ironclad: unquotedInt | None = None
    manowar: unquotedInt | None = None
    clipper_transport: unquotedInt | None = None
    cruiser: unquotedInt | None = None
    battleship: unquotedInt | None = None
    dreadnought: unquotedInt | None = None
    monitor: unquotedInt | None = None

    @classmethod
    @field_validator("naval_combat_slot")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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
    siege_combat: dict[repeated_key_indicator, list[Siege]] | None = None
    land_combat: dict[repeated_key_indicator, list[LandBattle]] | None = None
    naval_combat: dict[repeated_key_indicator, list[NavalBattle]] | None = None

    @classmethod
    @field_validator("siege_combat", "land_combat", "navel_combat")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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
    colony: dict[repeated_key_indicator, list[Colony]] | None = None

    @classmethod
    @field_validator("colony")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


class CrisisManager(BaseModel):
    date: quotedPDXDate | None = None


class WarGoal(BaseModel):
    casus_belli: quotedPDXVariable | None = None
    country: quotedTag | None = None
    actor: quotedTag | None = None
    receiver: quotedTag | None = None
    score: unquotedThreeSigFigDecimal | None = None
    change: unquotedThreeSigFigDecimal | None = None
    date: quotedPDXDate | None = None
    is_fulfilled: PDXBoolean | None = None
    state_province_id: unquotedInt | None = None


class CombatantInBattleHistoryEntry(BaseModel):
    country: quotedTag
    leader: quotedPDXVariable
    losses: unquotedInt
    infantry: unquotedInt | None = None
    engineer: unquotedInt | None = None
    irregular: unquotedInt | None = None
    artillery: unquotedInt | None = None
    steam_transport: unquotedInt | None = None
    frigate: unquotedInt | None = None
    commerce_raider: unquotedInt | None = None
    hussar: unquotedInt | None = None
    cuirassier: unquotedInt | None = None
    ironclad: unquotedInt | None = None
    dragoon: unquotedInt | None = None
    manowar: unquotedInt | None = None
    clipper_transport: unquotedInt | None = None
    guard: unquotedInt | None = None
    cavalry: unquotedInt | None = None
    cruiser: unquotedInt | None = None
    battleship: unquotedInt | None = None
    dreadnought: unquotedInt | None = None
    monitor: unquotedInt | None = None


class BattleHistoryEntry(BaseModel):
    name: quotedPDXVariable
    location: unquotedInt
    result: PDXBoolean
    attacker: CombatantInBattleHistoryEntry
    defender: CombatantInBattleHistoryEntry


class WarDiplomacyEntry(BaseModel):
    add_attacker: quotedTag | None = None
    add_defender: quotedTag | None = None
    rem_attacker: quotedTag | None = None
    rem_defender: quotedTag | None = None


class War(BaseModel):
    name: quotedPDXVariable
    history: dict
    original_attacker: quotedTag
    original_defender: quotedTag
    action: quotedPDXDate
    original_wargoal: WarGoal
    great_wars_enabled: PDXBoolean | None = None

    @classmethod
    @field_validator("history")
    def validate_history(cls, value: dict):
        for k, v in value.items():
            for entry in v[repeated_key_indicator]:
                if k == "battle":
                    BattleHistoryEntry.model_validate(entry)
                else:
                    WarDiplomacyEntry.model_validate(entry)
        return value


class ActiveWar(War):
    attacker: quotedTag
    defender: quotedTag
    war_goal: dict[repeated_key_indicator, list[WarGoal]]

    @classmethod
    @field_validator("war_goal")
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)


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
    id: dict[repeated_key_indicator, list[Identifier]]
    fired_events: FiredEvent
    province_data: Annotated[dict[unquotedInt, Province], "Collapse by one level"]
    nation_data: Annotated[dict[unquotedTag, Nation], "Collapse by one level"]
    rebel_faction: dict[repeated_key_indicator, list[RebelFaction]]
    diplomacy: Diplomacy
    combat: Combat

    active_war: dict[repeated_key_indicator, list[ActiveWar]] | None = None
    previous_war: dict[repeated_key_indicator, list[War]]
    invention: list[unquotedInt] | None = None
    great_nations: Annotated[list[unquotedInt], 8]
    outliner: list[unquotedInt]
    # TODO: news_collector, need to add support for parsing strings first
    region: dict[repeated_key_indicator, list[Region]]
    crisis_manager: CrisisManager

    @classmethod
    @field_validator(
        "id",
        "rebel_faction",
        "active_war",
        "previous_war",
        "region",
    )
    def handle_not_repeated(cls, v: dict | None):
        return handle_singleton_repeated_key(v)
