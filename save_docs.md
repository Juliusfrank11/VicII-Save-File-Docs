# Victoria II Save File structure

# Notes

Sections are listed as they appear in the save file strucutre, so first 
comes global gamestate data, then province data etc. Not all values are listed in the order they appear in the save file, this will be change if it turns out that they must be in order to generate a save file.

## Syntax

Booleans are denoted as `yes` and `no`

Decmials are up to 5 decimal palces, i.e. `148.68872`

Dates are given as strings in `"YYYY.M.D"` format

Unlike `json`, keys are NOT unique. This fact is used to list multiple instances of the same class of object within an array. For example `last_price_history` is listed multiple times so that the game can display the price history.

## Production tab

The Production *tab* on the Production *screen* (thanks PDX) seems to be 
broken in VicII. There are several keys in the save file structure that 
allude to storing supply and demand data such as `supply_poll` and 
`actual_sold`, but this isn't initalized on game start. 

If you enter that tab before the unpausing after loading a save game, it will show that you 
produce no goods, only updating after a day ticks by. Because of this, I 
assume these metrics are stored in the save file because originally this WAS 
supposed to be initalized on game start, but for whatever reason that 
functionality was scrapped.

It seems that a lot of these metrics are duplicated on the Trade screen as 
well.

## `id`

There is an array defined in many structures called `id` with the keys `id` and `type`. This seems to be used so that structures can reference each other (for example, assign pops to a regiment). 

# Macro Game State Data

## `date` (string)

Current game date, formatted as `"YYYY.M.D"`

## `player` (string)

Three-letter tag of the player country

## `government` (int)

UNCLEAR (party or government type?)

## `automate_trade` (boolean)

Option for trade automation, specified as `yes` or `no`

## `automate_sliders` (int)

UNCLEAR

## `rebel` (int)

UNCLEAR

## `unit` (int)

UNCLEAR, *might* be the number of rebel brigades willing to rise up, 
expressed in thousands (number of soliders). I.e. if 64 briages are ready to 
rise up, then `unit` should be a bit more than 6400

## `state` (int)

UNCLEAR, does not seem to be a province ID

## `flags` (array of keys)

list of flags that have been enabled. It seems that the Clausewitz engine can not support arrays of variables so flags need to specified as `flagname=yes`. Seems to be only used for canals.

List of flags:

- 'kiel_canal'
- 'panama_canal'
- 'suez_canal'

## `gameplaysettings` (array of keys)

UNCLEAR beyond having to do with gameplay settings

### `setgameplayoptions` (array of ints)

## `start_date` (string)

Start date of the game formatted in `"YYYY.M.D"`

## `start_pop_index` (int)

UNCLEAR

## `worldmarket` (array of keys)

Array containing information about trade prices, supply, and demand

TODO: List names used for goods and localizations

### `worldmarket_pool` (array of keys-decimal pairs)

UNCLEAR

### `price_pool` (array of key-decimal pairs)

Current price of goods

### `last_price_history` (array of key-decimal pairs)

Screenshot of prices taken at `price_history_last_update`.

### `supply_poll` (array of key-decimal pairs)

UNCLEAR, but *might* be the total number shown on the Production Tab on the 
Production screen. If so, it does not seem to actually initalize on game 
load, a day must tick for information to display in that tab.

Also shown on trade screen, no confirmed if these are infact the same.

### `last_supply_pool` (array of key-decimal pairs)

UNCLEAR, but if `supply_poll` does re

### Several instances of `price_history` (Array of key-decimal pairs)

up to 36 `price_history` arrays, presumably spaced one month apart. 
Used to display price history on the trade screen for the last 36 month. Not 
confirmed, but probably safe the guess they are taken on the first of the 
month.

### `price_history_last_update` (Date)

Date where `last_price_history` screenshot was taken. Presumably the 
`price_history` arrays are also updated at this date

### `price_change` (Array of key-decimal pairs)

Array with values of `price_poll - laste_price_history`. Goods that have not 
changed price are simply not included in the array as keys. It seems the 
only acceptable balues are `-0.01001` and `0.01001`

### `discovered_goods` (Array of key-decimal pairs)

List of goods that display on the trade screen. Contrary to it's name, it 
only takes into account "man-made" goods, later game materials like Oil are 
still listed. Non-"discovered" goods are unlisted and "discovered" goods are 
give the value `1.0000`

### `actual_sold` (Array of key-decimal pairs)

Seems to be the *"actually sold"* metric found on the trade screen when you 
hover over a good. Might be the same metric seen on the trade screen.

### `actual_sold_world` (Array of key-decimal pairs)

Seems to be the *"Exported"* metric found when you hover over a good on the 
production tab. Might be unused, see, the *Production tab* in *Notes*

### `real_demand` (Array of key-decimal pairs)

Seem to be the *"Demand"* displayed when you hover over a good on the trade 
screen. Unlike in the production tab, this IS initalized on game start.

### `demand` (Array of key-decimal pairs)

UNCLEAR

### `player_balance` (Array of key-decimal pairs)

UNCLEAR, seems to be unrelated to stockpiles

### Several instances of `player_pops_consumption_cache`

UNCLEAR, seems to have 13 instances consistently. Might be used to display 
Pop consumption needs on the Population screen

## `great_wars_enabled` (boolean)

Tells if great wars have been enabled in the save file

## `world_wars_enabled` (boolean)

UNCLEAR, possible unused feature for "even greater" great wars?

## `overseas_penalty` (Array of key-decimal pairs)

UNCLEAR, has keys `clipper_convoy` and `steamer_convoy`. Maybe attrition?

## `unit_cost` (Array of key-decimal pairs)

Total price to maintain the country's current army/navy. Display a the "Need 
\_\_\_ for Government" on the Trade Screen.

TODO: check if duplicated from trade information

## `budget_balance` (Array of decimals)

Government budget balance. Seems to be limited to 32 days. Not confirmed if 
it's supposed to be forwards or backwards to display on the HUD.

## `player_monthly_pop_growth` (Array of ints)

Population deltas, seems to be limited to 31 days? It might be that the 
number shown on the HUD for population change is the sum of these numbers. 
Would make sense since it changes everyday.

## `player_monthly_pop_growth_tag` (String)
Tag of the player when the last population delta was recorded (i.e. 31 days 
ago). Probably used as a fail safe for when tag flips happen.

## `player_monthly_pop_growth_date` (Date)

Date of the last record population Delta.

## `fascist`, `socialist`, `communist`, `anarcho-liberal` (Array of key-date pair)

Has key `enable` with value of the date the ideology was enabled if the 
ideology has been enabled, otherwise empty

## `id` (Array of key-int pairs)

Seemingly a stray event ID that is included in every single save file. It is 
always

```
id=
{
        id=16468
        type=4713
}
```

## `fired_event` (Array of arrays of key-int pairs)

All arrays follow the structure of `id`, including all used the key `id` for 
the event.

```
fired_events=
{
	id = {
		id=event_id
		type=event_type
	}
	...
}
```

it seems `event_type` is always `39`.


# Province Data Structure

Provinces are stored as Arrays of key-value pairs. The key of the province's 
array is the province's ID as defined by the game files.

## `name` (String, required)

String representing the name of the province. Unknown how this interacts 
with localization. Only time this is used as far as I recall is when the 
Ottomans/Turkey can rename Constantople to Istanbul.

## `owner` (String)

Tag of the owner of the province

## `controller` (String)

Tag of the controller (i.e. occupier) of the province

## `core` (String)

Tag of a country that has a core on the province. Multiple cores are 
represented by multiple `core` keys

## `garrison` (Decimal)

Garrison size in the province

TODO: find out range and where/if this is displayed in-game

## `fort` (Array of Decimals)

Two values indicating fort level. Maybe current and max fort level for when 
forts are still in construction?

Unlike most decimals there are only three decimal spaces specified in this array.


## `Railroad` (Array of Decimals)

As above, but for railroads

## `life_rating` (int)

Life rating of the province

## `infrastructure` (Decimal)

Infrastructure of the province. Unlike most decimals, this value is only specified to three decimal places

## `last_imigration` (date)

Presumably, the date that an individual (or Pop?) last immigrated to the province. The typo is intentional: that's how it is in the save file.

## `last_controller_change` (date)

Presumably, the province was last occupied/unoccupied.

## `crime` (int)

Type of crime in province

TODO: Document correpondense

## `party_loyalty` (Array of key-value pairs)

Loyalty to a specific _ideology_ rather than party, despite the name

Has a string-valued `ideology` to specify ideology and decimal-valued `loyalty_value` to specify the value.

## `modifier` (Array of key-value pairs)

Active province modifier. has two keys `modifier` (string) and `date` (date). Unknown if date is start date or expiration date

TODO: list all modifiers avaliable


## POP Data Sub-Structure

POPs are separately indexed by POP type, defined within the array that defines the provinces the pop is located in. So every unique POP in a province has a separate Array to define them within the province structure. 

Except for `artisans`, pops seem to share the same keys.

### `id` (int)

UNCLEAR, perhaps every pop has a unique ID

### `size` (int)

The number of people in the pop

### Culture/Religion

Culture and relgion is specified in a very strange way, it so done by making 
the culture the key and the religion the value. For example, to make a pop 
French Catholics, you would specify the key-value pair

```
french=catholic
```

### `money` (decimal)

Referred to as "Cash Reserves" in-game

### `ideology` (Array of int-decimal pairs)

Ideological distribution of the pop, using numbers to index the ideologies. The numbers are 

1. Fascist (Bruh)
2. Reactionary
3. Conservative
4. Socialist
5. Communist
6. Liberal
7. Anarcho-Liberal

TODO: Verify the mechanism of how percentages are allocated if their numbers don't add to 100.

### `issues` (Array of int-decimal pairs)

Issue concerns of the pop, with issues represented by numbers.

TODO: Document maps between ids and issues
TODO: Verify mechanisms of how percentages are allocated if they don't add 
up to 100

### `con` (decimal)

Consciousness of the pop, between 0.00000 and 10.00000

### `mil` (decimal)

Militancy of the pop, between 0.00000 and 10.00000

### `literacy` (decimal)

Literacy is represented as a fraction. Between 0.0000 and 1.0000

### `bank` (decimal)

Referred to as "Savings in Bank" in-game

### `con_factor` (decimal)

UNCLEAR

### `promoted` (Decimal)

Number of individuals in pop due to be promoted this month.

### `demoted` (Decimal)

Number of individuals in pop due to be demoted this month.

### `life_needs`, `everyday_needs`, and `luxury_needs` (decimal)

Percentage of needs filled, always less than 1. It seems that if needs are 100% filled, this key is just not listed

### `size_changes` (Array of ints)

UNCLEAR

### `converted` (int)

UNCLEAR

### `random` (int)

UNCLEAR

### `con_factor` (Decimal)

UNCLEAR

### `movement_issue` (string)

displayed rebel faction/voting issue on pop screen

### `days_of_loss` (int)

UNCLEAR, might be days of unemployment since it seems to be craftsmen-exclusive. Seems to be lower-class exclusive (craftsman, farmers, clerks)


### `faction` (array of key-int pairs)

Probably indicates rebel faction, has `id` and `type` as keys

### `local_migration` (int)

Probably number of individuals emigrating to another province within the country

### `external_migration` (int)

Probably number of individuals emigrating a province outside of the country

### `movement_tag` (string)

Tag specified for the *home country* of the pop, which need not exist. For example, Polish pops in Russia can have `movement_tag="PLC"` even if the PLC hasn't been released.  

### `colonial_migration` (int)

UNCLEAR

### `assimilated` (int)

UNCLEAR

### `artisans` exclusive keys

#### `production_type` (string)

Determines RGO output of pop

TODO: Document all production types

#### `stockpile` (Array of key-decimal pairs)

UNCLEAR, has RGOs as keys

#### `need` (Array of key-decimal pairs)

UNCLEAR, has RGOs as keys

#### `last_spending` (Decimal)

UNCLEAR

#### `current_producing` (Decimal)

UNCLEAR

#### `percent_afforded` (Decimal)

UNCLEAR

#### `percent_sold_domestic` (Decimal)

UNCLEAR

#### `percent_sold_export` (Decimal)

UNCLEAR

#### `leftover` (Decimal)

UNCLEAR


#### `leftover` (Decimal)

UNCLEAR

#### `throttle` (Decimal)

UNCLEAR

#### `needs_cost` (Decimal)

UNCLEAR

#### `production_income` (Decimal)

UNCLEAR

## `rgo` (Array of key-value pairs)

Contains RGO data

### `last_income` (decimal)

Number of pounds RGO output made last month

### `goods_type` (string)

RGO type

### `employment` (Array of key-value pairs)

Specifies the employment activity in the province

#### `province_id` (int)

Respecified province idea, because?????

#### `employees` (Array of Arrays)

Arrays follow the structure:

```
{
	province_pop_id= {
		province_id=0
		index=0
		type=0
	}
	count=0
}
```

All values are ints. Seems pops are fetched by province (which means `province_id` is fetched three times in the province structure)

## `unit_names` (array of key-value pairs)

Seems to contain data on units stationed in the province. Uses an array of arrays called `data`, seeming to index unit type by the position within `data`.

Lots of documentation needed.


## `building_construction` (Array of key-value pairs)

Contains information about factories being constructed

### `id` (Array of key-value pairs)

Two keys: `id` and `type`, both take on int values

### `start_date` (date)

Date when construction started

### `date` (date)

Date when construction is expected to finish

### `location` (int)

Duplicate of province id

### `country` (string)

Tag of the country that owns(?) the factory.

TODO: verify this still the case for 

### `building` (int)

presumably building type ID

### `input_goods` (Array of key-value pairs)

Information about factory input and monetary balances

#### `goods_demand` (Array of key-decimal pairs)


#### `input_goods` (Array of key-decimal pairs)

#### `money` (decimal)



## `military_construction` (Array of key-value pairs)

list information about units being constructed in the province

### `id` (Array of key-int pairs)

UNCLEAR, has keys `id` and `type`

### `start_date` (date)

The date that construction started

### `date` (date)

Date that the construction is set to finish

### `location` (int)

Province id

### `country` (string)

Tag of the country constructing a unit

### `name` (string)

Name of the unit

### `type` (string)

Unit type

### `unit` (Array of key-int pairs)

UNCLEAR, has keys `id` and `type`

### `regiment` (Array of key-int pairs)

UNCLEAR, has keys `id` and `type`

### `pop` (Array of key-int pairs)

UNCLEAR, likely points to the pop id but `type` is unclear, has keys `id` and `type`

### `count` (int)

UNCLEAR, but probably just the number of troops ordered?

### `rally_point` (int)

UNCLEAR, has values `-1`, `0` and `1`

# Country-level data

Arrays that define country data have the country's three-letter tag as its key (i.e. `ENG` for the UK)

## `human` (boolean)

`yes` if country is player countrolled

## `tax_base` (decimal)

UNCLEAR, it is NOT total income and is different from total income even if all taxes are set to their highest value and admin efficiency is at 100%

## `flags` (Array of key-boolean pairs)

Flags set by the nation to determine if events have happened

TODO: list out all flags

## `variables` (Array)

UNCLEAR

## `capital` (int)

Province ID of the capital of the country

## `ignore_descision` (string)

Name of ignored decisions. assuming This key is repeatable

## `technology` (Array of key-array pairs)

List of technologies discovered by the country, techs not discovered are not listed. Keys take on the name of tech (i.e. `machine_guns`) and values are always the array `{1 0.000}`


## `research` (Array of key-value pairs)

Stores currently active research

### `technology` (non-quoted string)

String stating the name of the technology currently being researched

### `cost` (decimal)

Despite the name, represents the amount of research points *already* allocated to the current tech. Specified to three decimal places

### `max_producing` (decimal)

The total number of research point required to finish the tech, *from scratch*. As in, this does not change with the value of `cost`. Specified to three decimal places


### `last_spending` (decimal)

Daily generated research points

### `active` (boolean)

Indicates if research is currently active. Not clear what this will do if set to `no`

## `last_reform` (date)

Date last reform was passed

## `last_election` (date)

Date last election occurred

## Reforms

reforms each have their separate key which is assign to a non-quoted string, i.e. `wage_reform=acceptable_minimum_wage`

TODO: list out names of keys and possible values

## `upper_house` (array of key-decimal pairs)

distribution of the upper house indexed by ideology name, (i.e. `liberal`)

## `last_lost_war` (date)

Unclear if date when the last war the country lost stared or ended.

## `ruling_party` (int)

ID of the currently ruling party, see `active_party` below for details

## `active_party` (int)

Repeatable key showing what parties are currently active. Importantly, the IDs of parties do NOT match the ideology ids in the POP data structure. Unknown how these IDs are generated, specially for countries with more than two political parties of the same ideology.

## `naval_need` (array of key-decimal pairs)

UNCLEAR, it does not seem to be either the amount of naval goods bought since that is `naval_supply_cost`

## `land_supply_cost` (array of key-decimal pairs)

Seems to be the *current day's* cost of supplying land units, as it does not match the "Last Day's estimated costs" shown on the Budget screen

## `naval_supply_cost` (array of key-decimal pairs)

Same as above but for navy

## `diplomatic_points` (decimal)

Amount of diplo points saved up, specified to three decimal places

## `religion` (string)

Accepted religion of the country

## `government` (non-quoted string)

Country's form of government (i.e. `hms_government`)

## `plurality` (decimal)

Plurality of the country, specified to three decimal places


## `revanchism` (decimal)

Revanchism of the country, specified to three decimal places


## `modifier` (array of key-value pairs)

Has string-valued `modifier` stating the modifier name and `date` which takes on strings that don't follow the usual date format. It consists of three numbers separated by periods, i.e. `"1.7.8"`

This key can repeat to show different modifiers

## `rich_tax`, `middle_tax`, and `poor_tax` (array of key-value pairs)

Represent the current tax levels for each strata

### `current` (decimal)

Current tax level as number between `0.00000` and `1.00000`

### `tax_income` (array of decimals)

12-entry array containing the amount of tax revenue obtained from each type of POP. The indexes of the array correspond to POP types

The pops not included in the strata will be set to `0.00000`. For example, in the `poor_tax.tax_income` array, the index representing capitalists will be have the value `0.00000`, but will be filled in the `rich_tax.tax_income` array. The index representing slaves will also be `0.00000` in countries where slavery is banned

TODO: list which indexes correspond to which pop types

### `tax_eff` (array of decimals)

As above but for tax efficency. Values of this array are not percentages.

### `total` (decimal)

UNCLEAR, as it doesn't seem to correspond to the total tax revenue for the strata

### `rangeLimitMax` (decimal)

Maximum allowed tax as a percent

### `rangeLimitMin` (decimal)

Minimum allowed tax as a percent

### `max_tax` (int)

Seems to be an older, now unused form of `rangeLimitMin`

### `min_tax` (int)

Seems to be an older, now unused form of `rangeLimitMax`

## `education_spending`, `crime_fighting`, `social_spending`, `military_spend` (Array of key-decimal pairs)

Stores information about sliders on the budget screen. `crime_fighting` is referred to as "Administration" in game

### `settings` (decimal)

Current percent allocation to the spending catagory


### `temp_settings` (decimal)

UNCLEAR, maybe used to store settings when ruling party changes?

### `factor` (decimal)

UNCLEAR, seems to always be set to `0.00998`

### `reserve` (decimal)

UNCLEAR, seems to always be set to `0.00000`


### `maxValue` (decimal)

UNCLEAR, might be a overflow prevention variable

### `rangeLimitMax` (decimal)

maximum level slider is allowed to be set to

### `rangeLimitMin` (decimal)

Minimum level slider is allowed to be set to

###  `max_tax`, `min_tax` (int)

Seems to be unused as in the tax arrays

## `overseas_penalty` (decimal)

UNCLEAR

## `leadership` (decimal)

Leadership points of the country

## `auto_assign_leaders` (boolean)

Auto-assign leaders setting

## `auto_create_leaders` (boolean)

Auto-create leaders setting

## `leader` (Array of key-value pairs)

contains information on (currently active?) leaders of the country. Repeated key

### `name` (string)

Name of the leader

### `date` (date)

Presumably, the date the leader was generated

### `type` (non-quoted string)

Type of leader, either `land` or `sea`

### `personality` (string)

Personality of general

TODO: list all personality values


### `background` (string)

Background of the general

TODO: list values


### `country` (string)

Country the general belongs to


### `picture` (string)

Image file used for the leader


### `prestige` (decimal)

Prestige of the leader, specified to three decimal places

### `id` (Array of key-int pairs)

UNCLEAR, has keys `id` and `type`


## `army` and `navy` (Array of key-value pairs)

repeated key containing data on land armies and naval units

### `id` (array of key-int pairs)

UNCLEAR, has keys `id` and `type`

### `name` (string)

Unit name

### `leader` (array of key-int pairs)

Presumably used to link the leader to the army, has keys `id` and `type`. 

### `previous` (int)

Province ID of the last province the unit was placed at

### `movement_progress` (3 sig fig decimal)

Movement progress of troop

### `location` (int)

Province ID of the province the unit is currently located in. If a navy is docked in a port, this is set to land province's ID

### `dig_in_last_date`

UNCLEAR, date when dig in progress progressed last?

### `supplies` (3 sig fig decimal)

Percent of needed supplies received by the unit

### `regiment` and `ship` (array of key-value pairs)

repeated key storing information about the regiments 

### `at_sea` (int, navy only)

If unit is currently in a sea province

### `no_supply_days` (int, navy only)

Naval attrition value?

#### `id` (array of key-int pairs)

Identifier for the regiment

#### `name`

Regiment name

#### `pop` (`id` reference) (`army` only)

Reference to a POP ID

#### `organisation` (3 sig fig decimal)

Organization value of the regiment

#### `strength` (3 sig fig decimal)

Strength value of the regiment

#### `experience` (3 sig fig decimal)

Experience value of the regiment

#### `count` (int)

Always set to `1`

#### `type` (non-quoted string)

Unit type of regiment/ship

## Relations

relations with countries has indexed by the three-letter tag of the country

Unlike the top-level arrays, countries that don't exist in the save file are not included as keys within these arrays.

The array of the tag of the country just has the single pair `value=0`

### `value` (int)

Relations value to the country the relation array belongs to

### `last_send_diplomat` (date)

Date a diplomat was last sent to coutnry

### `level_changed_date` (date)

Date the influence level with the country was last changed

### `level` (int)

Influence level

TODO: list what values correspond to what influence lever

### `influence_value` (3 sig fig decimal)

Influence points value 

### `last_war` (date)

Date that last war with country (ended?) (started?)


### `truce_until` (date)

Date truce expires with country

## `active_inventions`, `possible_inventions`, `illegal_inventions` (array of ints)

List IDs of active (already discovered), possible, and illegal (not possible) inventions

## `government_flag` (array of string-string pairs)

UNCLEAR, Seems to have the previous government type as they "key" and current government type as the "value" for countries that have had a revolution

## `last_mission_cancel` (date)


UNCLEAR, unused feature?

## `ai` and `ai_hard_strategy` (array of key-value pairs)

Stores variables for AI depending on difficulty. 

### `initialized` (boolean)

If the AI has been activated (at least once?) in the campaign

### `consolidate` (boolean)

UNCLEAR

### `date` (date)

UNCLEAR

### `static` (boolean)

UNCLEAR

### `personality` (non-quoted string)

AI behaviour characteristic, unknown what these value mean exactly

TODO: list all values

### `conquer_prov` (array of key-int pairs)

Repeated key to list provinces that the AI show want to conquer, like an implicit "strategic interest" from EU4. Has keys `id` for the province ID and `value`


### `threat`, `antagonize`, `befriend`, `protect` and `rival` (array of key-value pairs)

Repeated keys for relation attributes to other countries. Has keys `id` with the three-letter tag of the country and `value` which is given an int (not clear if bounded)

Countries can repeat for at least some attitudes, for example `threat` and `rival`. Not clear if any attributes are actually mutually exclusive.


## `foreign_investment` (array of decimals)

UNCLEAR, notiable for using index of an array instead of country tags if this is listing out foreign investment *to* countries

## `schools` (string)

Research school of the country

## `primary_culture` (string)

Primary culture of the country


## `culture` (array of strings)

Accepted cultures of the country.

## `prestige` (3 sigfig decimal)

Prestige of the country

## `bank` (array of key-decimal pairs)

UNCLEAR, has keys `money` and `money_lent`

## `last_bankrupt` (date)

Date the country last went bankrupt, set to `"1.1.1"` if the country has never gone bankrupt

## `movement` (array of key-value pairs)

Repeated key showing active movements in the country, has string-valued `issue` stating the reform and decimal-valued `cache` which is unclear

## `stockpile` (array of key-decimal pairs)

Stockpile of goods (including non-military goods). Goods with no stockpile are not included as keys

## `national_value` (string)

national value of the country

## `buy_domestic` (array)

UNCLEAR, always empty in samples, maybe a player setting?

## `trade` (array of arrays of key-value pairs)

Trade settings, indexed by the name of the good. The arrays of goods have keys:

- `limit` (decimal)
- `buy` (boolean)
- `automate_trade` (boolean)

## `civilized` (boolean)

If the country is civilized, there is no special value for partially westernized nations

## `last_greatness_date` (date)

Last date when the country was a great power. Current date if country is a great power

## `state` (array of key-value pairs)

stores state information, including building information

### `id` (identifier)
UNCLEAR, but assuming `id.id` is the state id?

### `provinces` (array of ints)
ids of provinces included in the state
### `state_buildings` (repeated array of key-value pairs)
Contains factory information

#### `building` (string)
Type of factory
#### `level` (int)
Factory level
#### `stockpile` (array of key-int pairs)
Current stockpile of factory inputs
#### `employment` (array of key-value pairs)
Contains employment information
##### `state_province_id` (int)
UNCLEAR
###### `employees` (array of key-value pairs)
UNCLEAR, has an int valued `count` along with the repeated array `province_pop_id` with int-valued keys 

- `province_id`
- `index`
- `type` 

#### `money` (float)
#### `last_spending` (float)
#### `last_income` (float)
#### `pops_paychecks` (float)
#### `last_investment` (float)
#### `unprofitable_days` (int)
#### `subsidised` (boolean)
If the factory is subsidized or not
#### `leftover` (float)
#### `injected_money` (float)
#### `injected_days` (int)
#### `produces` (float)
#### `profit_history_days` (int)
#### `profit_history_current` (int)
#### `profit_history_entry` (array of ints)
### `savings` (float)

### `interest` (float)
### `flashpoint` (boolean)
If the state can spawn a crisis
### `crisis` (string)
Tag of the country that would receive territory if the current owner backs down from a crisis
## `badboy` (3 sigfig decimal)
Infamy
## `trade_cap_land` (decimal)
## `trade_cap_naval` (decimal)
## `trade_cap_projects` (decimal)
## `max_tariff` (decimal)
## `domestic_supply_poll` (array of key-decimal pairs)
Keys are the RGO name
## `sold_supply_poll` (array of key-decimal pairs)
## `domestic_demand_pool` (array of key-decimal pairs)
## `actual_sold_domestic` (array of key-decimal pairs)
## `saved_country_supply` (array of key-decimal pairs)
## `max_bought` (array of key-decimal pairs)
## `national_focus` (array of string-string pairs)
oddly enough, the "strings" used as keys are actually ints (state ids?) wrapped in quotes
## `influence` (array of string-string pairs)
also odd, the keys are quoted country tags, but the values are quoted ints
## `expenses` (array of decimals)
## `incomes` (array of decimals)
## `interesting_countries` (array of ints)
## `next_quarterly_pulse` (date)
## `next_yearly_pulse` (date)
## `suppression` (3 sigfig decimal)
## `railroads` (repeated array of key-array pairs)
Contains an array called `path` whos value is an array of province ids
## `is_releasable_vassal` (boolean)