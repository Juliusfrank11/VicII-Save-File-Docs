from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import date
from typing import Annotated, Literal, Union, Tuple, Optional
from decimal import Decimal
from validators import make_string_unquoted, validate_pdx_date
import unquoted_dtypes as unquoted
import quoted_dtypes as quoted

from pydantic import Extra, FilePath


class Configuration(BaseModel):
    input: FilePath = "input"
    output: FilePath = "output"

    class Config:
        extra = Extra.forbid


# pesudo-primitive" PDX-exclusive classes
Repeated = list  # used for keys that repeat
PDXBoolean = Union[Literal["yes"], Literal["no"]]


class RepeatedKeyIndicator(BaseModel):
    this_is_a_repeated_key_please_collapse_down: bool


class Convoys(BaseModel):
    clipper_convoy: unquoted.FiveSigFigDecimal
    steamer_convoy: unquoted.FiveSigFigDecimal


class WorldMarket(BaseModel):
    worldmarket_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    price_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    last_price_history: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    supply_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    last_supply_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    price_history: Repeated[
        RepeatedKeyIndicator | dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    ]
    price_history_last_update: quoted.PDXDate
    price_change: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    discovered_goods: dict[unquoted.RGO, float]
    actual_sold: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    actual_sold_world: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    real_demand: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    demand: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    player_balance: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    player_pops_consumption_cache: Repeated[
        RepeatedKeyIndicator | dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    ]


class IdeologyEnabled(BaseModel):
    enabled = quoted.PDXDate


class Identifier(BaseModel):
    id: unquoted.Int
    type: unquoted.Int


class IndexedIdentifier(Identifier):
    index: unquoted.Int


class FiredEvent(BaseModel):
    id: Repeated[RepeatedKeyIndicator | Identifier]


class Culture(BaseModel):
    name: unquoted.PDXVariable
    religion: unquoted.PDXVariable


class Pop(BaseModel):
    id: unquoted.Int
    pop_type: unquoted.PDXVariable
    size: unquoted.Int
    culture: Culture
    money: unquoted.FiveSigFigDecimal
    ideology: dict[unquoted.Int, unquoted.FiveSigFigDecimal]
    issues: dict[unquoted.Int, unquoted.FiveSigFigDecimal]
    con: unquoted.FiveSigFigDecimal
    literacy: unquoted.FiveSigFigDecimal
    bank: unquoted.FiveSigFigDecimal
    con_factor: unquoted.FiveSigFigDecimal
    demoted: unquoted.Int
    promoted: unquoted.Int
    life_needs: unquoted.FiveSigFigDecimal
    everyday_needs: unquoted.FiveSigFigDecimal
    luxury_needs: unquoted.FiveSigFigDecimal
    size_changes: list[unquoted.Int]
    converted: unquoted.Int
    random: unquoted.Int
    faction: Identifier
    local_migration: unquoted.Int
    external_migration: unquoted.Int
    movement_tag: quoted.Tag
    colonial_migration: unquoted.Int
    assimilated: unquoted.Int


class Worker(Pop):
    days_of_loss = unquoted.Int


class Artisans(Pop):
    production_type: str
    stockpile: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    need: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    last_spending: unquoted.FiveSigFigDecimal
    current_producing: unquoted.FiveSigFigDecimal
    percent_afforded: unquoted.FiveSigFigDecimal
    percent_sold_domestic: unquoted.FiveSigFigDecimal
    percent_sold_export: unquoted.FiveSigFigDecimal
    leftover: unquoted.FiveSigFigDecimal
    throttle: unquoted.FiveSigFigDecimal
    needs_cost: unquoted.FiveSigFigDecimal
    production_income: unquoted.FiveSigFigDecimal
    con_factor: unquoted.FiveSigFigDecimal


class EmployeeData(BaseModel):
    province_pop_id: Repeated[RepeatedKeyIndicator | IndexedIdentifier]
    count: unquoted.Int


class Employment(BaseModel):
    province_id: unquoted.Int
    employees: EmployeeData
    last_income: unquoted.FiveSigFigDecimal
    goods_type: str


class UnitNameData(BaseModel):
    # need more verification on this one
    # very unclear how it works
    count: unquoted.Int
    id: list[unquoted.Int]


class PartyLoyalty(BaseModel):
    ideology: str
    loyalty_value: unquoted.FiveSigFigDecimal


class BuildingConstruction(BaseModel):
    id: Identifier
    state_date: quoted.PDXDate
    date: quoted.PDXDate
    location: Annotated[unquoted.Int, "Province ID"]
    country: quoted.Tag
    building: unquoted.Int


class MilitaryInputGoodsData(BaseModel):
    goods_demand: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    input_demand: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    money: unquoted.FiveSigFigDecimal


class MilitaryConstruction(BaseModel):
    id: Identifier
    start_date: quoted.PDXDate
    date: quoted.PDXDate
    location: Annotated[unquoted.Int, "Province ID"]
    country: quoted.Tag
    input_goods: MilitaryInputGoodsData
    name: str
    type: str
    unit: Identifier
    regiment: Identifier
    pop: Identifier
    count: unquoted.Int
    rally_point: unquoted.Int


class Province(BaseModel):
    name: str
    owner: quoted.Tag
    controller: quoted.Tag
    core: Optional[Repeated[RepeatedKeyIndicator | quoted.Tag]]
    garrison: unquoted.ThreeSigFigDecimal
    fort: Annotated[list[unquoted.ThreeSigFigDecimal], 2]
    railroad: Annotated[list[unquoted.ThreeSigFigDecimal], 2]
    naval_base: Annotated[list[unquoted.ThreeSigFigDecimal], 2]
    pops: list[Pop]
    rgo: Employment
    life_rating: unquoted.Int
    infrastructure: unquoted.ThreeSigFigDecimal
    last_imigration: quoted.PDXDate
    last_controller_change: quoted.PDXDate
    unit_names: UnitNameData
    party_loyalty: Repeated[RepeatedKeyIndicator | PartyLoyalty]
    nationalism: unquoted.ThreeSigFigDecimal
    building_construction: Repeated[RepeatedKeyIndicator | BuildingConstruction]
    military_construction: Repeated[RepeatedKeyIndicator | MilitaryConstruction]
    crime: unquoted.Int


class Research(BaseModel):
    technology: unquoted.Technology
    cost: unquoted.ThreeSigFigDecimal
    max_producing: unquoted.ThreeSigFigDecimal
    last_spending: unquoted.ThreeSigFigDecimal
    active: PDXBoolean


class CountryModifier(BaseModel):
    modifier: str
    date: quoted.PDXDate


class TaxBracket(BaseModel):
    current: unquoted.FiveSigFigDecimal
    tax_income: list[unquoted.FiveSigFigDecimal, 13]
    tax_eff: list[unquoted.FiveSigFigDecimal, 13]
    total: unquoted.FiveSigFigDecimal
    rangeLimitMax: unquoted.FiveSigFigDecimal
    rangeLimitMin: unquoted.FiveSigFigDecimal
    max_tax: unquoted.Int
    min_tax: unquoted.Int


class SpendingSetting(BaseModel):
    settings: unquoted.FiveSigFigDecimal
    temp_settings: unquoted.FiveSigFigDecimal
    factor: unquoted.FiveSigFigDecimal
    reserve: unquoted.FiveSigFigDecimal
    maxValue: unquoted.FiveSigFigDecimal
    rangeLimitMax: unquoted.FiveSigFigDecimal
    rangeLimitMin: unquoted.FiveSigFigDecimal
    max_tax: unquoted.Int
    min_tax: unquoted.Int


class Leader(BaseModel):
    name: str
    date: quoted.PDXDate
    type: Annotated[unquoted.PDXVariable, "`land` or `sea`"]
    personality: str
    background: str
    country: quoted.Tag
    picture: str
    prestige: unquoted.ThreeSigFigDecimal
    id: Identifier


class Ship(BaseModel):
    id: Identifier
    name: str
    pop: Identifier
    organisation: unquoted.ThreeSigFigDecimal
    strength: unquoted.ThreeSigFigDecimal
    experience: unquoted.ThreeSigFigDecimal
    count: unquoted.Int
    type: unquoted.PDXVariable


class Regiment(Ship):
    pop: Identifier


class Army(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[unquoted.Int, "Province ID"]
    movement_progress: unquoted.ThreeSigFigDecimal
    location: Annotated[unquoted.Int, "Province ID"]
    dig_in_last_date: quoted.PDXDate = "2.1.1"
    supplies: unquoted.ThreeSigFigDecimal
    regiment: Repeated[RepeatedKeyIndicator | Regiment]


class Navy(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[unquoted.Int, "Province ID"]
    movement_progress: unquoted.ThreeSigFigDecimal
    location: Annotated[unquoted.Int, "Province ID"]
    dig_in_last_date: quoted.PDXDate = "2.1.1"
    supplies: unquoted.ThreeSigFigDecimal
    ship: Repeated[RepeatedKeyIndicator | Ship]


class ForeignRelation(BaseModel):
    value: unquoted.Int
    last_send_diplomat: quoted.PDXDate
    last_war: quoted.PDXDate
    truce_until: quoted.PDXDate
    level: unquoted.Int
    level_changed_date: quoted.PDXDate
    influence_value: unquoted.ThreeSigFigDecimal


class ProvinceDesire(BaseModel):
    id: unquoted.Int
    value: unquoted.Int


class DiplomaticAttitude(BaseModel):
    id: quoted.Tag
    value: unquoted.Int


class AIStrategy(BaseModel):
    initialized: PDXBoolean
    consolidate: PDXBoolean
    date: quoted.PDXDate
    static: PDXBoolean
    personality: unquoted.PDXVariable
    conquer_prov: Repeated[RepeatedKeyIndicator | ProvinceDesire]
    threat: Repeated[RepeatedKeyIndicator | DiplomaticAttitude]
    antagonize: Repeated[RepeatedKeyIndicator | DiplomaticAttitude]
    befriend: Repeated[RepeatedKeyIndicator | DiplomaticAttitude]
    protect: Repeated[RepeatedKeyIndicator | DiplomaticAttitude]
    rival: Repeated[RepeatedKeyIndicator | DiplomaticAttitude]


class PoliticalMovement(BaseModel):
    support: unquoted.Int
    cache: unquoted.FiveSigFigDecimal


class IndependenceMovement(PoliticalMovement):
    tag: quoted.Tag


class PolicyMovement(PoliticalMovement):
    issue: str


class TradePolicy(BaseModel):
    limit: unquoted.FiveSigFigDecimal
    buy: PDXBoolean
    automate_trade: PDXBoolean


class State(BaseModel):
    id: Identifier
    provinces: list[unquoted.Int]
    is_colonial: unquoted.Int
    savings: unquoted.FiveSigFigDecimal
    interest: unquoted.FiveSigFigDecimal
    flashpoint: PDXBoolean
    tension: unquoted.ThreeSigFigDecimal
    crisis: quoted.Tag


class NationalBank(BaseModel):
    money: unquoted.FiveSigFigDecimal
    money_lent: unquoted.FiveSigFigDecimal


class Railroad(BaseModel):
    path: list[Annotated[unquoted.Int, "Province ID"]]


class Nation(BaseModel):
    human: PDXBoolean
    tax_base: unquoted.FiveSigFigDecimal
    flags: dict[unquoted.PDXVariable, PDXBoolean]
    variables: dict = {}
    capital: Annotated[unquoted.Int, "Province ID"]
    research_points: unquoted.ThreeSigFigDecimal
    technology: dict[unquoted.Technology, Annotated[list, 2]]
    research: Research
    last_reform: quoted.PDXDate
    last_election: quoted.PDXDate
    wage_reform: unquoted.PDXVariable
    work_hours: unquoted.PDXVariable
    safety_regulations: unquoted.PDXVariable
    unemployment_subsidies: unquoted.PDXVariable
    pensions: unquoted.PDXVariable
    health_care: unquoted.PDXVariable
    school_reforms: unquoted.PDXVariable
    slavery: unquoted.PDXVariable
    vote_franschise: unquoted.PDXVariable
    voting_system: unquoted.PDXVariable
    public_meetings: unquoted.PDXVariable
    press_rights: unquoted.PDXVariable
    trade_unions: unquoted.PDXVariable
    political_parties: unquoted.PDXVariable
    upper_house: dict[unquoted.Ideology, unquoted.FiveSigFigDecimal]
    last_party_change: quoted.PDXDate
    ruling_party: unquoted.Int
    active_party: unquoted.Int
    naval_need: Convoys
    land_supply_cost: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    naval_supply_cost: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    diplomatic_points: unquoted.ThreeSigFigDecimal
    religion: quoted.PDXVariable
    government: unquoted.PDXVariable
    plurality: unquoted.ThreeSigFigDecimal
    revanchism: unquoted.ThreeSigFigDecimal
    modifier: Repeated[RepeatedKeyIndicator | CountryModifier]
    poor_tax: TaxBracket
    middle_tax: TaxBracket
    rich_tax: TaxBracket
    education_spending: SpendingSetting
    crime_fighting: SpendingSetting
    social_spending: SpendingSetting
    military_spending: SpendingSetting
    overseas_penalty: unquoted.FiveSigFigDecimal = Decimal(0.00000)
    leadership: unquoted.FiveSigFigDecimal = Decimal(0.00000)
    auto_assign_leaders: PDXBoolean
    auto_create_leaders: PDXBoolean
    leader: Repeated[RepeatedKeyIndicator | Leader]
    army: Repeated[RepeatedKeyIndicator | Army]
    navy: Repeated[RepeatedKeyIndicator | Navy]
    relations: dict[unquoted.Tag, ForeignRelation]
    active_inventions: list[unquoted.Int]
    possible_inventions: list[unquoted.Int]
    illegal_inventions: list[unquoted.Int]
    government_flag: dict[str, str]
    last_mission_cancel: quoted.PDXDate = date(1, 1, 1)
    ai_hard_strategy: AIStrategy
    ai_strategy: AIStrategy
    foreign_investment: list[unquoted.FiveSigFigDecimal]
    schools: quoted.PDXVariable
    primary_culture: quoted.PDXVariable
    culture: list[str] = []
    bank: NationalBank
    money: unquoted.FiveSigFigDecimal
    last_bankrupt: quoted.PDXDate = '"1.1.1"'
    prestige: unquoted.ThreeSigFigDecimal
    movement: Repeated[
        RepeatedKeyIndicator
        | Union[PoliticalMovement, IndependenceMovement, PolicyMovement]
    ]
    stockpile: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    national_value: quoted.PDXVariable
    buy_domestic: dict = {}
    trade: dict[unquoted.RGO, TradePolicy]
    civilized: PDXBoolean
    state: Repeated[RepeatedKeyIndicator | State]
    badboy: unquoted.ThreeSigFigDecimal
    trade_cap_land: unquoted.FiveSigFigDecimal
    trade_cap_naval: unquoted.FiveSigFigDecimal
    trade_cap_projects: unquoted.FiveSigFigDecimal
    max_tariff: unquoted.FiveSigFigDecimal
    domestic_supply_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    sold_supply_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    domestic_demand_pool: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    actual_sold_domestic: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    saved_country_supply: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    max_bought: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    national_focus: dict[quoted.Int, quoted.PDXVariable]
    influence: dict[quoted.Tag, quoted.Int]
    expenses: list[unquoted.FiveSigFigDecimal]
    incomes: list[unquoted.FiveSigFigDecimal]
    interesting_countries: list[unquoted.Int]
    next_quarterly_pulse: quoted.PDXDate
    next_yearly_pulse: quoted.PDXDate
    suppression: unquoted.ThreeSigFigDecimal
    railroads = Repeated[RepeatedKeyIndicator | Railroad]
    is_releasable_vassal: PDXBoolean = "yes"


class RebelFaction(BaseModel):
    id: Identifier
    type: str
    name: str
    country: quoted.Tag
    independence: Union[quoted.Tag, Literal["---"]] = "---"
    culture: str
    religion: str
    government: str
    province: unquoted.Int
    leader: Identifier
    organization: unquoted.FiveSigFigDecimal
    pop: Repeated[RepeatedKeyIndicator | Identifier]


class Alliance(BaseModel):
    first: quoted.Tag
    second: quoted.Tag
    end_date: quoted.PDXDate = '"1949.1.1"'
    start_date: quoted.PDXDate = '"1795.1.1"'


class Vassalage(BaseModel):
    first: Annotated[quoted.Tag, "Overload"]
    second: Annotated[quoted.Tag, "Vassal"]
    end_date: quoted.PDXDate = '"1949.1.1"'
    start_date: quoted.PDXDate = '"1795.1.1"'


class CasusBelli(BaseModel):
    type: str
    first: quoted.Tag
    second: quoted.Tag
    start_date: quoted.PDXDate


class Combatant(BaseModel):
    dice: unquoted.Int
    unit: Repeated[RepeatedKeyIndicator | Identifier]
    losses: unquoted.ThreeSigFigDecimal
    accumulated_losses: list[unquoted.ThreeSigFigDecimal]
    front: dict[unquoted.Int, Identifier]
    back: dict[unquoted.Int, Identifier]


class LandCombatant(BaseModel):
    dice: unquoted.Int
    unit: Repeated[RepeatedKeyIndicator | Identifier]
    losses: unquoted.ThreeSigFigDecimal
    accumulated_losses: list[unquoted.ThreeSigFigDecimal]
    front: dict[unquoted.Int, Identifier]
    back: dict[unquoted.Int, Identifier]
    reserves: Repeated[RepeatedKeyIndicator | Identifier]
    irregular: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    infantry: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    guard: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    cavalry: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    cuirassier: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    dragoon: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    hussar: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    airplane: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    artillery: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    engineer: unquoted.ThreeSigFigDecimal = Decimal(0.000)
    armor: unquoted.ThreeSigFigDecimal = Decimal(0.000)


class NavalCombatSlot(BaseModel):
    attacker: Identifier
    distance: unquoted.ThreeSigFigDecimal
    stance: unquoted.Int
    total_damage_str: unquoted.ThreeSigFigDecimal
    total_damage_org: unquoted.ThreeSigFigDecimal
    icon: unquoted.Int
    name: quoted.PDXVariable
    killer_name: quoted.PDXVariable = ""
    tag: quoted.Tag


class NavalCombatant(Combatant):
    naval_combat_slot: Repeated[RepeatedKeyIndicator | NavalCombatSlot]
    penalty_factor: unquoted.ThreeSigFigDecimal
    # TODO: list out unit keys like in LandCombatant


class Siege(BaseModel):
    location: Annotated[unquoted.Int, "Province Id"]
    day: unquoted.Int = -1
    duration: unquoted.Int = 0
    attacker: Combatant = {}
    defender: Combatant = {}
    total: unquoted.Int


class LandBattle(BaseModel):
    location: Annotated[unquoted.Int, "Province Id"]
    day: unquoted.Int
    duration: unquoted.Int
    attacker: LandCombatant
    defender: LandCombatant


class NavalBattle(BaseModel):
    location: Annotated[unquoted.Int, "Province Id"]
    day: unquoted.Int
    duration: unquoted.Int
    attacker: NavalCombatant
    defender: NavalCombatant


class Colony(BaseModel):
    tag: quoted.Tag
    points: unquoted.Int
    invest: unquoted.Int
    date: quoted.PDXDate


class Region(BaseModel):
    index: unquoted.Int
    phase: unquoted.Int
    date: quoted.PDXDate
    temperature: unquoted.ThreeSigFigDecimal


class VicIISave(BaseModel):
    date: quoted.PDXDate
    player: quoted.Tag
    government: unquoted.Int
    automate_trade: PDXBoolean
    automate_sliders: unquoted.Int
    rebel: unquoted.Int
    unit: unquoted.Int
    state: unquoted.Int
    flags = dict[unquoted.PDXVariable, PDXBoolean]
    gameplaysettings = dict[Literal["setgameplayoptions"], list[unquoted.Int]]
    start_date: quoted.PDXDate
    start_pop_index: unquoted.Int
    worldmarket: WorldMarket
    great_wars_enabled: PDXBoolean
    world_wars_enabled: PDXBoolean
    overseas_penalty: Convoys
    unit_cost: dict[unquoted.RGO, unquoted.FiveSigFigDecimal]
    budget_balance: list[unquoted.FiveSigFigDecimal]
    player_monthly_pop_growth: Annotated[list[unquoted.Int], 30]
    player_monthly_pop_growth_tag: quoted.Tag
    player_monthly_pop_growth_date: quoted.PDXDate
    fascist: IdeologyEnabled
    socialist: IdeologyEnabled
    communist: IdeologyEnabled
    anarcho_liberal: IdeologyEnabled
    canals: list[unquoted.Int]
    id: Repeated[RepeatedKeyIndicator | Identifier] | Identifier
    fired_events: FiredEvent
    province_data: Annotated[dict[unquoted.Int, Province], "Collapse by one level"]
    nation_data: Annotated[dict[unquoted.Tag, Nation], "Collapse by one level"]
    rebel_faction: Repeated[RepeatedKeyIndicator | RebelFaction]
    diplomacy: Annotated[
        Repeated[
            RepeatedKeyIndicator
            | dict[
                Union[Literal["alliance"], Literal["vassal"], Literal["casus_belli"]],
                Union[Alliance, Vassalage, CasusBelli],
            ]
        ],
        "Keys are `alliance` `vassal` and `casus_belli`",
    ]
    combat: Annotated[
        Repeated[
            RepeatedKeyIndicator
            | dict[
                Union[
                    Literal["siege_combat"],
                    Literal["land_combat"],
                    Literal["naval_combat"],
                ],
                Union[Siege, LandBattle, NavalBattle],
            ]
        ],
        "keys are `siege_combat` `land_combat` and `naval_combat`]",
    ]
    # TODO: active_war
    # TODO: previous_war
    inventions: Optional[list[unquoted.Int]]
    great_nations: Annotated[list[unquoted.Int], 8]
    outliner: list[unquoted.Int]
    # TODO: news_collector, need to add support for parsing strings first
    region: Repeated[RepeatedKeyIndicator | Region]
