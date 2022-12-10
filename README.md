## Project description

# UFC Data Scraper
**UFC Data Scraper** is a simple webscraping library.

## Scrape fighter pages
Easily scrape a fighters page and get a more convenient Fighter object to work with.

    >>> from ufc_data_scraper import ufc_scraper
    >>> fighter_url = "https://www.ufc.com/athlete/jan-blachowicz"
    >>> fighter = ufc_scraper.scrape_fighter_url(fighter_url)
	>>> type(fighter)
	'Fighter'
    >>> fighter_dict = fighter.to_dict()
or convert that Fighter object into a dictionary.
## Scrape event pages
Easily scrape an event page and get a more convenient Event object to work with.

Know the events internal event id(fmid)?

    >>> from ufc_data_scraper import ufc_scraper
    >>> event_fmid = 1124
    >>> event_data = ufc_scraper.scrape_event_fmid(1124)

or leave it to the library to figure out.

    >>> from ufc_data_scraper import ufc_scraper
    >>> event_url = "https://www.ufc.com/event/ufc-282"
    >>> event = ufc_scraper.scrape_event_url(event_url)
    >>> type(event)
	'Event'
 
    >>> event_dict = event.to_dict()

or convert that Event object into a dictionary.

## Fighter Object

 - **fighter_url** *- (str)* A link to the fighter on the UFC website.
 - **name** *- (str)* Full name.
 - **nickname** *- (str)* Nickname.
 - **status** *- (str)* Current status. i.e "Active"
 - **ranking** *- (str)* Ranking in their respective **weight** class. i.e "#1" or "Title Holder"
 - **pfp_ranking** *- (str)* Ranking in pound for pound **rankings**. i.e "#13 PFP" or "Unranked"
 - **weight_class** *- (str)* Current fighting weight class. i.e "Light Heavyweight Division"
 - **home_city** *- (str)* City the fighter currently fights out of.
 - **home_country** *- (str)* Country the fighter was born in.
 - **gym** *- (str)* Gym the fighter currently trains at.
 - **fighting_style** *- (str)* Name that best describes a fighters style. i.e "Boxing"
 - [**record** *- (Record object)*](#Record%20Object)
 - **win_method** *- (WinMethod object)* 
 - **physical_stats** *- (PhysicalStats object)* 
 - **striking** *- (Striking object)* 
 - **grappling** *- (Grappling object)* 

### Record Object
 - **win** *- (int)* Career wins.
 - **loss** *- (int)* Career losses.
 - **draw** *- (int)* Career draws.

### WinMethod Object
 - **knockout** *- (int)* Career knockout wins.
 - **knockout_per***- (int)* Percentage of career wins are knockouts.
 - **decision** *- (int)* Career decision wins.
 - **decision_per** *- (int)* Percentage of career wins are decisions.
 - **submission** *- (int)* Career submission wins.
 - **submission_per** *- (int)* Percentage of career wins are submissions.
 - **average_fight_time** *- (str)* Average fight length in *minutes*:*seconds*. i.e "12:20"

### PhysicalStats Object
 - **age** *- (int)* Current age.
 - **height** *- (int)* Height in inches.
 - **weight** *- (int)* Last weight in weight in pounds. i.e "205.50"
 - **reach** *- (int)* Reach in inches.
 - **leg_reach** *- (int)* Leg reach in inches.

### Striking Object
 - **striking_accuracy** *- (int)* Career striking accuracy as a percentage.
 - **strikes_landed** *- (int)* Career strikes landed.
 - **strikes_attempted** *- (int)* Career strikes attempted.
 - **strikes_average** *- (float)* Average strikes per 15 minutes.
 - **strikes_absorbed_average** *- (float)* Average strikes absorbed per 15 minutes.
 - **striking_defence** *- (int)* Percentage of strikes attempted against fighter that do not land.
 - **knockdown_average** *- (float)* Average knockdowns per 15 minutes.
 - **strike_position** *- (StrikePosition object)* 
 - **strike_target** *- (StrikeTarget object)*
 
#### StrikePosition Object
 - **standing** *- (int)* Strikes from standing position.
 - **standing_per***- (int)* Percentage of all strikes are from standing position.
 - **clinch** *- (int)* CStrikes from clinch position.
 - **clinch_per** *- (int)* Percentage of all strikes are from clinch position.
 - **ground** *- (int)* Strikes from ground position.
 - **ground_per** *- (int)* Percentage of all strikes are from ground position.

#### StrikeTarget Object
 - **head** *- (int)* Strikes targeted at opponents head.
 - **head_per***- (int)* Percentage of all strikes are targeted at the opponents head.
 - **body** *- (int)* Strikes targeted at opponents body.
 - **body_per***- (int)* Percentage of all strikes are targeted at the opponents body.
 - **leg** *- (int)* Strikes targeted at opponents legs.
 - **leg_per***- (int)* Percentage of all strikes are targeted at the opponents legs.

### Grappling Object
 - **takedown_accuracy** *- (int)* Career takedown accuracy as a percentage.
 - **takedowns_landed** *- (int)* Career takedowns landed.
 - **takedowns_attempted** *- (int)* Career takedowns attempted.
 - **takedowns_average** *- (float)* Average takedowns per 15 minutes.
 - **takedown_defence** *- (int)* Percentage of takedowns attempted against fighter that do not land.
 - **submission_average** *- (float)* Average submissions per 15 minutes.