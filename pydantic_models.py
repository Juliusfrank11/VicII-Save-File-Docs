from pydantic import BaseModel
from datetime import date
from typing import Annotated, Literal, Union, Tuple
from decimal import Decimal

# pesudo-primitive" PDX-exclusive classes
Tag = Annotated[str, "Country tag"]
ThreeSigFigDecimal = Annotated(Decimal, "only to three sigfigs")
FiveSigFigDecimal = Annotated(Decimal, "only to five sigfigs")
Variable = Annotated[str, "unquoted string"]
Flag = Annotated[Variable, "global event flag"]
RGO = Annotated[Variable, "RGO name"]
Tech = Annotated[Variable, "Technology"]
Ideology = Annotated[Variable, "Ideology"]
Repeated = list  # used for keys that repeat


class Convoys(BaseModel):
    clipper_convoy: FiveSigFigDecimal
    steamer_convoy: FiveSigFigDecimal


class WorldMarket(BaseModel):
    worldmarket_pool: dict[RGO, FiveSigFigDecimal]
    price_pool: dict[RGO, FiveSigFigDecimal]
    last_price_history: dict[RGO, FiveSigFigDecimal]
    supply_pool: dict[RGO, FiveSigFigDecimal]
    last_supply_pool: dict[RGO, FiveSigFigDecimal]
    price_history: Repeated[dict[RGO, FiveSigFigDecimal]]
    price_history_last_update: date
    price_change: dict[RGO, FiveSigFigDecimal]
    discovered_goods: dict[RGO, 1.00000]
    actual_sold: dict[RGO, FiveSigFigDecimal]
    actual_sold_world: dict[RGO, FiveSigFigDecimal]
    real_demand: dict[RGO, FiveSigFigDecimal]
    demand: dict[RGO, FiveSigFigDecimal]
    player_balance: dict[RGO, FiveSigFigDecimal]
    player_pops_consumption_cache: Repeated[dict[RGO, FiveSigFigDecimal]]


class IdeologyEnabled(BaseModel):
    enabled = date


class Identifier(BaseModel):
    id: int
    type: int


class IndexedIdentifier(Identifier):
    index: int


class FiredEvent(BaseModel):
    id: Repeated[Identifier]


class Culture(BaseModel):
    name: Variable
    religion: Variable


class Pop(BaseModel):
    id: int
    pop_type: Variable
    size: int
    culture: Culture
    money: FiveSigFigDecimal
    ideology: dict[int, FiveSigFigDecimal]
    issues: dict[int, FiveSigFigDecimal]
    con: FiveSigFigDecimal
    literacy: FiveSigFigDecimal
    bank: FiveSigFigDecimal
    con_factor: FiveSigFigDecimal
    demoted: int
    promoted: int
    life_needs: FiveSigFigDecimal
    everyday_needs: FiveSigFigDecimal
    luxury_needs: FiveSigFigDecimal
    size_changes: list[int]
    converted: int
    random: int
    faction: Identifier
    local_migration: int
    external_migration: int
    movement_tag: Tag
    colonial_migration: int
    assimilated: int


class Worker(Pop):
    days_of_loss = int


class Artisans(Pop):
    production_type: str
    stockpile: dict[RGO, FiveSigFigDecimal]
    need: dict[RGO, FiveSigFigDecimal]
    last_spending: FiveSigFigDecimal
    current_producing: FiveSigFigDecimal
    percent_afforded: FiveSigFigDecimal
    percent_sold_domestic: FiveSigFigDecimal
    percent_sold_export: FiveSigFigDecimal
    leftover: FiveSigFigDecimal
    throttle: FiveSigFigDecimal
    needs_cost: FiveSigFigDecimal
    production_income: FiveSigFigDecimal
    con_factor: FiveSigFigDecimal


class EmployeeData(BaseModel):
    province_pop_id: Repeated[IndexedIdentifier]
    count: int


class Employment(BaseModel):
    province_id: int
    employees: EmployeeData
    last_income: FiveSigFigDecimal
    goods_type: str


class UnitNameData(BaseModel):
    # need more verification on this one
    # very unclear how it works
    count: int
    id: list[int]


class PartyLoyalty(BaseException):
    ideology: str
    loyalty_value: FiveSigFigDecimal


class BuildingConstruction(BaseModel):
    id: Identifier
    state_date: date
    date: date
    location: Annotated[int, "Province ID"]
    country: Tag
    building: int


class MilitaryInputGoodsData(BaseModel):
    goods_demand: dict[RGO, FiveSigFigDecimal]
    input_demand: dict[RGO, FiveSigFigDecimal]
    money: FiveSigFigDecimal


class MilitaryConstruction(BaseModel):
    id: Identifier
    start_date: date
    date: date
    location: Annotated[int, "Province ID"]
    country: Tag
    input_goods: MilitaryInputGoodsData
    name: str
    type: str
    unit: Identifier
    regiment: Identifier
    pop: Identifier
    count: int
    rally_point: int


class Province(BaseModel):
    name: str
    owner: Tag
    controller: Tag
    core: Repeated[Tag]
    garrison: ThreeSigFigDecimal
    fort: Annotated[list[ThreeSigFigDecimal], 2]
    railroad: Annotated[list[ThreeSigFigDecimal], 2]
    naval_base: Annotated[list[ThreeSigFigDecimal], 2]
    pops: list[Pop]
    rgo: Employment
    life_rating: int
    infrastructure: ThreeSigFigDecimal
    last_imigration: date
    last_controller_change: date
    unit_names: UnitNameData
    party_loyalty: Repeated[PartyLoyalty]
    nationalism: ThreeSigFigDecimal
    building_construction: Repeated[BuildingConstruction]
    military_construction: Repeated[MilitaryConstruction]
    crime: int


class Research(BaseModel):
    technology: Tech
    cost: ThreeSigFigDecimal
    max_producing: ThreeSigFigDecimal
    last_spending: ThreeSigFigDecimal
    active: bool


class CountryModifier(BaseModel):
    modifier: str
    date: date


class TaxBracket(BaseModel):
    current: FiveSigFigDecimal
    tax_income: list[FiveSigFigDecimal, 13]
    tax_eff: list[FiveSigFigDecimal, 13]
    total: FiveSigFigDecimal
    rangeLimitMax: FiveSigFigDecimal
    rangeLimitMin: FiveSigFigDecimal
    max_tax: int
    min_tax: int


class SpendingSetting(BaseModel):
    settings: FiveSigFigDecimal
    temp_settings: FiveSigFigDecimal
    factor: FiveSigFigDecimal
    reserve: FiveSigFigDecimal
    maxValue: FiveSigFigDecimal
    rangeLimitMax: FiveSigFigDecimal
    rangeLimitMin: FiveSigFigDecimal
    max_tax: int
    min_tax: int


class Leader(BaseModel):
    name: str
    date: date
    type: Annotated[Variable, "`land` or `sea`"]
    personality: str
    background: str
    country: Tag
    picture: str
    prestige: ThreeSigFigDecimal
    id: Identifier


class Ship(BaseModel):
    id: Identifier
    name: str
    pop: Identifier
    organisation: ThreeSigFigDecimal
    strength: ThreeSigFigDecimal
    experience: ThreeSigFigDecimal
    count: int
    type: Variable


class Regiment(Ship):
    pop: Identifier


class Army(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[int, "Province ID"]
    movement_progress: ThreeSigFigDecimal
    location: Annotated[int, "Province ID"]
    dig_in_last_date: date = date(2, 1, 1)
    supplies: ThreeSigFigDecimal
    regiment: Repeated[Regiment]


class Navy(BaseModel):
    id: Identifier
    name: str
    leader: Identifier
    previous: Annotated[int, "Province ID"]
    movement_progress: ThreeSigFigDecimal
    location: Annotated[int, "Province ID"]
    dig_in_last_date: date = date(2, 1, 1)
    supplies: ThreeSigFigDecimal
    ship: Repeated[Ship]


class ForeignRelation(BaseModel):
    value: int
    last_send_diplomat: date
    last_war: date
    truce_until: date
    level: int
    level_changed_date: date
    influence_value: ThreeSigFigDecimal


class ProvinceDesire(BaseModel):
    id: int
    value: int


class DiplomaticAttitude(BaseModel):
    id: Tag
    value: int


class AIStrategy(BaseModel):
    initialized: bool
    consolidate: bool
    date: date
    static: bool
    personality: Variable
    conquer_prov: Repeated[ProvinceDesire]
    threat: Repeated[DiplomaticAttitude]
    antagonize: Repeated[DiplomaticAttitude]
    befriend: Repeated[DiplomaticAttitude]
    protect: Repeated[DiplomaticAttitude]
    rival: Repeated[DiplomaticAttitude]


class PoliticalMovement(BaseModel):
    support: int
    cache: FiveSigFigDecimal


class IndependenceMovement(PoliticalMovement):
    tag: Tag


class PolicyMovement(PoliticalMovement):
    issue: str


class TradePolicy(BaseModel):
    limit: FiveSigFigDecimal
    buy: bool
    automate_trade: bool


class State(BaseModel):
    id: Identifier
    provinces: list[int]
    is_colonial: int
    savings: FiveSigFigDecimal
    interest: FiveSigFigDecimal
    flashpoint: bool
    tension: ThreeSigFigDecimal
    crisis: Tag


class NationalBank(BaseModel):
    money: FiveSigFigDecimal
    money_lent: FiveSigFigDecimal


class Railroad(BaseModel):
    path: list[Annotated[int, "Province ID"]]


class Nation(BaseModel):
    human: bool
    tax_base: FiveSigFigDecimal
    flags: dict[Flag, True]
    variables: dict = {}
    capital: Annotated[int, "Province ID"]
    research_points: ThreeSigFigDecimal
    technology: dict[Tech, Tuple[1, 0.000]]
    research: Research
    last_reform: date
    last_election: date
    wage_reform: Variable
    work_hours: Variable
    safety_regulations: Variable
    unemployment_subsidies: Variable
    pensions: Variable
    health_care: Variable
    school_reforms: Variable
    slavery: Variable
    vote_franschise: Variable
    voting_system: Variable
    public_meetings: Variable
    press_rights: Variable
    trade_unions: Variable
    political_parties: Variable
    upper_house: dict[Ideology, FiveSigFigDecimal]
    last_party_change: date
    ruling_party: int
    active_party: int
    naval_need: Convoys
    land_supply_cost: dict[RGO, FiveSigFigDecimal]
    naval_supply_cost: dict[RGO, FiveSigFigDecimal]
    diplomatic_points: ThreeSigFigDecimal
    religion: str
    government: Variable
    plurality: ThreeSigFigDecimal
    revanchism: ThreeSigFigDecimal
    modifier: Repeated[CountryModifier]
    poor_tax: TaxBracket
    middle_tax: TaxBracket
    rich_tax: TaxBracket
    education_spending: SpendingSetting
    crime_fighting: SpendingSetting
    social_spending: SpendingSetting
    military_spending: SpendingSetting
    overseas_penalty: FiveSigFigDecimal
    leadership: FiveSigFigDecimal
    auto_assign_leaders: bool
    auto_create_leaders: bool
    leader: Repeated[Leader]
    army: Repeated[Army]
    navy: Repeated[Navy]
    relations: dict[Tag, ForeignRelation]
    active_inventions: list[int]
    possible_inventions: list[int]
    illegal_inventions: list[int]
    government_flag: dict[str, str]
    last_mission_cancel: date = date(1, 1, 1)
    ai_hard_strategy: AIStrategy
    ai_strategy: AIStrategy
    foreign_investment: list[FiveSigFigDecimal]
    schools: str
    primary_culture: str
    culture: list[str] = []
    bank: NationalBank
    money: FiveSigFigDecimal
    last_bankrupt: date = date(1, 1, 1)
    prestige: ThreeSigFigDecimal
    movement: Repeated[Union[PoliticalMovement, IndependenceMovement]]
    stockpile: dict[RGO, FiveSigFigDecimal]
    national_value: str
    buy_domestic: dict = {}
    trade: dict[RGO, TradePolicy]
    civilized: bool
    state: Repeated[State]
    badboy: ThreeSigFigDecimal
    trade_cap_land: FiveSigFigDecimal
    trade_cap_naval: FiveSigFigDecimal
    trade_cap_projects: FiveSigFigDecimal
    max_tariff: FiveSigFigDecimal
    domestic_supply_pool: dict[RGO, FiveSigFigDecimal]
    sold_supply_pool: dict[RGO, FiveSigFigDecimal]
    domestic_demand_pool: dict[RGO, FiveSigFigDecimal]
    actual_sold_domestic: dict[RGO, FiveSigFigDecimal]
    saved_country_supply: dict[RGO, FiveSigFigDecimal]
    max_bought: dict[RGO, FiveSigFigDecimal]
    national_focus: dict[Annotated[str, "Quoted Province ID"], str]
    expenses: list[FiveSigFigDecimal]
    incomes: list[FiveSigFigDecimal]
    interesting_countries: list[int]
    next_quarterly_pulse: date
    next_yearly_pulse: date
    suppression: ThreeSigFigDecimal
    railroads = Repeated[Railroad]
    is_releasable_vassal: bool = True


class RebelFaction(BaseModel):
    id: Identifier
    type: str
    name: str
    country: Tag
    independence: Union[Tag, Literal["---"]] = "---"
    culture: str
    religion: str
    government: str
    province: int
    leader: Identifier
    organization: FiveSigFigDecimal
    pop: Repeated[Identifier]


class Alliance(BaseModel):
    first: Tag
    second: Tag
    end_date: date = date(1949, 1, 1)
    start_date: date


class Vassalage(BaseModel):
    first: Tag  # Overlord
    second: Tag  # Vassal
    end_date: date = date(1949, 1, 1)
    start_date: date = date(1795, 1, 1)


class CasusBelli(BaseModel):
    type: str
    first: Tag
    second: Tag
    start_date: date


class Combatant(BaseModel):
    dice: int
    unit: Repeated[Identifier]
    losses: ThreeSigFigDecimal
    accumulated_losses: list[ThreeSigFigDecimal]
    front: dict[int, Identifier]
    back: dict[int, Identifier]


class LandCombatant(BaseModel):
    dice: int
    unit: Repeated[Identifier]
    losses: ThreeSigFigDecimal
    accumulated_losses: list[ThreeSigFigDecimal]
    front: dict[int, Identifier]
    back: dict[int, Identifier]
    reserves: Repeated[Identifier]
    irregular: ThreeSigFigDecimal = Decimal(0.000)
    infantry: ThreeSigFigDecimal = Decimal(0.000)
    guard: ThreeSigFigDecimal = Decimal(0.000)
    cavalry: ThreeSigFigDecimal = Decimal(0.000)
    cuirassier: ThreeSigFigDecimal = Decimal(0.000)
    dragoon: ThreeSigFigDecimal = Decimal(0.000)
    hussar: ThreeSigFigDecimal = Decimal(0.000)
    airplane: ThreeSigFigDecimal = Decimal(0.000)
    artillery: ThreeSigFigDecimal = Decimal(0.000)
    engineer: ThreeSigFigDecimal = Decimal(0.000)
    armor: ThreeSigFigDecimal = Decimal(0.000)


class NavalCombatSlot(BaseModel):
    attacker: Identifier
    distance: ThreeSigFigDecimal
    stance: int
    total_damage_str: ThreeSigFigDecimal
    total_damage_org: ThreeSigFigDecimal
    icon: int
    name: str
    killer_name: str = ""
    tag: Tag


class NavalCombatant(Combatant):
    naval_combat_slot: Repeated[NavalCombatSlot]
    penalty_factor: ThreeSigFigDecimal
    # TODO: list out unit keys like in LandCombatant


class Siege(BaseModel):
    location: Annotated[int, "Province Id"]
    day: int = -1
    duration: int = 0
    attacker: Combatant = {}
    defender: Combatant = {}
    total: int


class LandBattle(BaseModel):
    location: Annotated[int, "Province Id"]
    day: int
    duration: int
    attacker: LandCombatant
    defender: LandCombatant


class NavalBattle(BaseModel):
    location: Annotated[int, "Province Id"]
    day: int
    duration: int
    attacker: NavalCombatant
    defender: NavalCombatant


class Region(BaseModel):
    index: int
    phase: int
    date: date
    temperature: ThreeSigFigDecimal


class VicIISave(BaseModel):
    date: date
    player: Tag
    government: int
    automate_trade: bool
    automate_slider: int
    rebel: int
    unit: int
    state: int
    flags = dict[Flag, bool]
    gameplaysettings = dict[Variable, list[int]]
    start_date: date
    start_pop_index: int
    worldmarket: WorldMarket
    great_wars_enabled: bool
    world_wars_enabled: bool
    overseas_penalty: Convoys
    unit_cost: dict[RGO, FiveSigFigDecimal]
    budget_balance: Annotated[list[FiveSigFigDecimal], 30]
    player_monthly_pop_growth: Annotated[list[int], 30]
    player_monthly_pop_growth_tag: Tag
    player_monthly_pop_growth_date: date
    fascist: IdeologyEnabled
    socialist: IdeologyEnabled
    communist: IdeologyEnabled
    anarcho_liberal: IdeologyEnabled
    canals: list[Union[0, 1]]
    id: Identifier
    fired_events: FiredEvent
    province_data: Annotated[dict[int, Province], "Collapse by one level"]
    nation_data: Annotated[dict[Tag, Nation], "Collapse by one level"]
    rebel_faction: Repeated[RebelFaction]
    diplomacy: Annotated[
        Repeated[dict[Variable, Union[Alliance, Vassalage, CasusBelli]]],
        "Keys are `alliance` `vassal` and `casus_belli`",
    ]
    combat: Annotated[
        Repeated[dict[Variable, Union[Siege, LandBattle, NavalBattle]]],
        "keys are `siege_combat` `land_combat` and `naval_combat`]",
    ]
    # TODO: active_war
    # TODO: previous_war
    invention: list[int]
    great_nation: Annotated[list[int], 8]
    outliner: list[int]
    # TODO: news_collector, need to add support for parsing strings first
    region: Repeated[Region]
