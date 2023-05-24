# Victoria II Save File structure

# Notes

Sections are listed as they appear in the save file strucutre, so first 
comes global gamestate data, then province data etc.

## Syntax

Booleans are denoted as `yes` and `no`

Decmials are up to 5 decimal palces, i.e. `148.68872`

Dates are given as strings in `"YYYY.M.D"` format

Unlike `json`, keys are NOT unique. This fact is used to list multiple instances of the same class of object within an array. For example 

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

list of flags that have been enabled. It seems that the Clausewitz engine 
can not support arrays of variables so flags need to specified as the 
`flagname=yes`

TODO: document a list of all flags

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

## POP Data Sub-Structure

POPs are separately indexed by POP type, define within the array that defines the provinces the pop is located in. So every unique POP in a province has a separate Array to define them within the province structure. 

Except for `artisans`, pops seem to share the same keys.

### `id` (int)

UNCLEAR, perhaps every pop has unique ID

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


### `random` (int)

UNCLEAR

### `con_factor` (Decimal)

UNCLEAR

### `movement_issue` (string)

displayed rebel faction/voting issue on pop screen

### `days_of_loss` (int) (Craftsmen and clerks only)

UNCLEAR, might be days of unemployment since it seems to be craftsmen-exclusive


### `faction` (array of key-int pairs)

Probably indicates rebel faction, has `id` and `type` as keys

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

Tag of the country that owns the factory

### `building` (int)

presumably building type ID

### `input_goods` (Array of key-value pairs)

Information about factory input and monartary balances

#### `goods_demand` (Array of key-decimal pairs)


#### `input_goods` (Array of key-decimal pairs)

#### `money` (decimal)

