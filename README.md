## Project description

# UFC Data Scraper

**UFC Data Scraper** is a simple webscraping library.
## Scrape fighter pages

Easily scrape a fighters page and get a more convenient Fighter dataclass to work with.

    >>> from ufc_data_scraper import ufc_scraper

    >>> fighter_url = "https://www.ufc.com/athlete/jan-blachowicz"

    >>> fighter = ufc_scraper.scrape_fighter_url(fighter_url)

    >>> type(fighter)

    'Fighter'
    
or convert that Fighter or any other related dataclass into a dictionary using asdict.

    >>> from dataclasses import asdict
    >>> fighter_dict = asdict(fighter)
    >>> fighter_record_dict = asdict(fighter.record)
    
## Get event FMID

Find internal event id(fmid) using only the event page url. This can be used to get event data directly.

    >>> from ufc_data_scraper import ufc_scraper

    >>> event_url = "https://www.ufc.com/event/ufc-282"

    >>> event_fmid = ufc_scraper.get_event_fmid(event_url)

    >>> type(event)

    1124

## Scrape event pages

Easily scrape an event page and get a more convenient Event dataclass to work with.

Know the internal event id(fmid)?

    >>> from ufc_data_scraper import ufc_scraper

    >>> event_fmid = 1124

    >>> event_data = ufc_scraper.scrape_event_fmid(1124)

or leave it to the library to figure out.

    >>> from ufc_data_scraper import ufc_scraper

    >>> event_url = "https://www.ufc.com/event/ufc-282"

    >>> event = ufc_scraper.scrape_event_url(event_url)

    >>> type(event)

    'Event'


or convert that Event or any other related dataclass into a dictionary using asdict.

    >>> from dataclasses import asdict
    >>> event_dict = asdict(event)
    >>> event_location_dict = asdict(event.location)
    
## Installing Ufc Data Scraper

Requests is currently only available from git:

    $ python -m pip install git+https://gitlab.com/HeXeDMinD/ufc-data-scraper.git

## [Check out my other projects](http://www.mypersonalsite.co.za)

## Fighter Object

-  **fighter_url**  *- (str)* A link to the fighter on the UFC website.
-  **name**  *- (str)* Full name.
-  **nickname**  *- (str)* Nickname.
-  **status**  *- (str)* Current status. i.e "Active"
-  **ranking**  *- (str)* Ranking in their respective **weight** class. i.e "#1" or "Title Holder"
-  **pfp_ranking**  *- (str)* Ranking in pound for pound **rankings**. i.e "#13 PFP" or "Unranked"
-  **weight_class**  *- (str)* Current fighting weight class. i.e "Light Heavyweight Division"
-  **home_city**  *- (str)* City the fighter currently fights out of.
-  **home_country**  *- (str)* Country the fighter was born in.
-  **gym**  *- (str)* Gym the fighter currently trains at.
-  **fighting_style**  *- (str)* Name that best describes a fighters style. i.e "Boxing"
-  **record**  *- (Record object)* [Record object](#record-object)
-  **win_method**  *- (WinMethod object)* [WinMethod object](#winmethod-object)
-  **physical_stats**  *- (PhysicalStats object)* [PhysicalStats object](#physicalstats-object)
-  **striking**  *- (Striking object)* [Striking object](#striking-object)
-  **grappling**  *- (Grappling object)* [Grappling object](#grappling-object)

  

### Record Object

-  **win**  *- (int)* Career wins.
-  **loss**  *- (int)* Career losses.
-  **draw**  *- (int)* Career draws.

  

### WinMethod Object

-  **knockout**  *- (int)* Career knockout wins.
-  **knockout_per** *- (int)* Percentage of career wins are knockouts.
-  **decision**  *- (int)* Career decision wins.
-  **decision_per**  *- (int)* Percentage of career wins are decisions.
-  **submission**  *- (int)* Career submission wins.
-  **submission_per**  *- (int)* Percentage of career wins are submissions.
-  **average_fight_time**  *- (str)* Average fight length in *minutes*:*seconds*. i.e "12:20"

  

### PhysicalStats Object

-  **age**  *- (int)* Current age.
-  **height**  *- (float)* Height in inches.
-  **weight**  *- (float)* Last weight in weight in pounds. i.e "205.50"
-  **reach**  *- (float)* Reach in inches.
-  **leg_reach**  *- (float)* Leg reach in inches.

  

### Striking Object

-  **striking_accuracy**  *- (int)* Career striking accuracy as a percentage.
-  **strikes_landed**  *- (int)* Career strikes landed.
-  **strikes_attempted**  *- (int)* Career strikes attempted.
-  **strikes_average**  *- (float)* Average strikes per 15 minutes.
-  **strikes_absorbed_average**  *- (float)* Average strikes absorbed per 15 minutes.
-  **striking_defence**  *- (int)* Percentage of strikes attempted against fighter that do not land.
-  **knockdown_average**  *- (float)* Average knockdowns per 15 minutes.
-  **strike_position**  *- (StrikePosition object)* [StrikePosition object](#strikeposition-object)
-  **strike_target**  *- (StrikeTarget object)* [StrikeTarget object](#striketarget-object)

#### StrikePosition Object

-  **standing**  *- (int)* Strikes from standing position.
-  **standing_per** *- (int)* Percentage of all strikes are from standing position.
-  **clinch**  *- (int)* CStrikes from clinch position.
-  **clinch_per**  *- (int)* Percentage of all strikes are from clinch position.
-  **ground**  *- (int)* Strikes from ground position.
-  **ground_per**  *- (int)* Percentage of all strikes are from ground position.

  

#### StrikeTarget Object

-  **head**  *- (int)* Strikes targeted at opponents head.
-  **head_per** *- (int)* Percentage of all strikes are targeted at the opponents head.
-  **body**  *- (int)* Strikes targeted at opponents body.
-  **body_per** *- (int)* Percentage of all strikes are targeted at the opponents body.
-  **leg**  *- (int)* Strikes targeted at opponents legs.
-  **leg_per** *- (int)* Percentage of all strikes are targeted at the opponents legs.

  

### Grappling Object

-  **takedown_accuracy**  *- (int)* Career takedown accuracy as a percentage.
-  **takedowns_landed**  *- (int)* Career takedowns landed.
-  **takedowns_attempted**  *- (int)* Career takedowns attempted.
-  **takedowns_average**  *- (float)* Average takedowns per 15 minutes.
-  **takedown_defence**  *- (int)* Percentage of takedowns attempted against fighter that do not land.
-  **submission_average**  *- (float)* Average submissions per 15 minutes.

## Event Object

-  **fmid**  *- (int)* Events internal ID, used by private UFC api.
-  **name** *- (str)* Event name.
- **date** *- (datetime)* Event date, localised to GMT.
- **status** *- (str)* Events status. i.e "Upcoming"
- **location**  *- (Location object)* [Location object](#location-object)
- **card_segments**  *- (list)* A list of [CardSegment objects](#cardsegment-object)

### Location Object
-  **venue**  *- (str)* Venue where event is hosted. i.e "UFC Apex"
-  **city** *- (str)* City venue is located in. i.e "Las Vegas"
- **country** *- (str)* Country city is located in. i.e "United States of America"
- **tricode** *- (str)* Country's tricode. i.e "USA"

### CardSegment Object
- **name**  *- (str)* Card segment name. i.e "Main" or "Prelims1"
- **start_time** *- (datetime)* Card segment start time, localised to GMT.
- **broadcaster**  *- (str)* Broadcaster. i.e "UFC  Fight  Pass" or "PPV"
- **fights**  *- (list)* A list of [Fight objects](#fight-object)

### Fight Object
-  **fight_order**  *- (int)* Events internal ID, used by private UFC api.
-  **referee_name** *- (str)* Event name.
- **fighters_stats**  *- (list)* A list of [FighterStats objects](#fighterstats-object)
- **result**  *- (Result object)* [Result object](#result-object)
- **weight_class**  *- (WeightClass object)* [WeightClass object](#weightclass-object)
- **accolades**  *- (Accolade object)* [Accolade object](#accolade-object)
- **rule_set**  *- (RuleSet object)* [RuleSet object](#ruleset-object)
- **fight_scores**  *- (list)* A list of [FightScore objects](#fightscore-object)

#### Result Object
-  **fighter**  *- (Fighter object)* [Fighter  object](#fighter-object)
-  **corner** *- (int)* 
- **weigh_in** *- (float)* 
- **outcome** *- (str)* 
- **ko_of_the_night** *- (bool)* 
- **submission_of_the_night** *- (bool)* 
- **performance_of_the_night** *- (bool)* 

#### Result Object
-  **method**  *- (str)* 
-  **ending_round** *- (int)* 
- **ending_time** *- (str)* 
- **ending_strike** *- (str)* 
- **ending_target** *- (str)* 
- **ending_position** *- (str)* 
- **ending_submission** *- (str)* 
- **ending_notes** *- (str)* 
- **fight_of_the_night** *- (bool)* 

#### WeightClass Object
-  **description**  *- (str)* 
-  **abbreviation**  *- (str)* 
-  **weight**  *- (str)* 

#### Accolade Object
-  **description**  *- (str)* 
-  **type**  *- (str)* 

#### RuleSet Object
-  **description**  *- (str)* 
-  **possible_rounds**  *- (str)* 

#### FightScore Object
-  **judge_name**  *- (str)* 
-  **score_red**  *- (int)* 
-  **score_blue**  *- (int)* 