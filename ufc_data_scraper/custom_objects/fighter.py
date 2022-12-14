from ufc_data_scraper.custom_objects.base_object import _BaseObject


class Record(_BaseObject):
    def __init__(
        self,
        win: int,
        loss: int,
        draw: int,
    ) -> None:

        self.win = win
        self.loss = loss
        self.draw = draw

    def __str__(self) -> str:
        return f"{self.win}-{self.loss}-{self.draw}"


class WinMethod(_BaseObject):
    def __init__(
        self,
        knockout: int,
        knockout_per: int,
        decision: int,
        decision_per: int,
        submission: int,
        submission_per: int,
        average_fight_time: str,
    ) -> None:

        self.knockout = knockout
        self.knockout_per = knockout_per
        self.decision = decision
        self.decision_per = decision_per
        self.submission = submission
        self.submission_per = submission_per

        self.average_fight_time = average_fight_time


class PhysicalStats(_BaseObject):
    def __init__(
        self,
        age: int,
        height: float,
        weight: float,
        reach: float,
        leg_reach: float,
    ) -> None:

        self.age = age
        self.height = height
        self.weight = weight
        self.reach = reach
        self.leg_reach = leg_reach

    def __str__(self) -> str:
        return f"{self.height}, {self.weight}"


class StrikePosition(_BaseObject):
    def __init__(
        self,
        standing: int,
        standing_per: int,
        clinch: int,
        clinch_per: int,
        ground: int,
        ground_per: int,
    ) -> None:

        self.standing = standing
        self.standing_per = standing_per
        self.clinch = clinch
        self.clinch_per = clinch_per
        self.ground = ground
        self.ground_per = ground_per


class StrikeTarget(_BaseObject):
    def __init__(
        self,
        head: int,
        head_per: int,
        body: int,
        body_per: int,
        leg: int,
        leg_per: int,
    ) -> None:

        self.head = head
        self.head_per = head_per
        self.body = body
        self.body_per = body_per
        self.leg = leg
        self.leg_per = leg_per


class Striking(_BaseObject):
    def __init__(
        self,
        striking_accuracy: int,
        strikes_landed: int,
        strikes_attempted: int,
        strikes_average: float,
        strikes_absorbed_average: float,
        striking_defence: int,
        knockdown_average: float,
        strike_position: StrikePosition,
        strike_target: StrikeTarget,
    ) -> None:

        self.striking_accuracy = striking_accuracy
        self.strikes_landed = strikes_landed
        self.strikes_attempted = strikes_attempted
        self.strikes_average = strikes_average
        self.strikes_absorbed_average = strikes_absorbed_average
        self.striking_defence = striking_defence

        self.knockdown_average = knockdown_average

        self.strike_position = strike_position
        self.strike_target = strike_target


class Grappling(_BaseObject):
    def __init__(
        self,
        takedown_accuracy: int,
        takedowns_landed: int,
        takedowns_attempted: int,
        takedowns_average: float,
        takedown_defence: int,
        submission_average: float,
    ) -> None:

        self.takedown_accuracy = takedown_accuracy
        self.takedowns_landed = takedowns_landed
        self.takedowns_attempted = takedowns_attempted
        self.takedowns_average = takedowns_average
        self.takedown_defence = takedown_defence
        self.submission_average = submission_average

    def __str__(self) -> str:
        return self.takedown_accuracy


class Fighter(_BaseObject):
    def __init__(
        self,
        fighter_url: str,
        name: str,
        nickname: str,
        status: str,
        ranking: str,
        pfp_ranking: str,
        weight_class: str,
        home_city: str,
        home_country: str,
        gym: str,
        fighting_style: str,
        record: Record,
        win_method: WinMethod,
        physical_stats: PhysicalStats,
        striking: Striking,
        grappling: Grappling,
    ) -> None:

        super().__init__()

        self.fighter_url = fighter_url

        self.name = name
        self.nickname = nickname

        self.status = status
        self.ranking = ranking
        self.pfp_ranking = pfp_ranking
        self.weight_class = weight_class

        self.home_city = home_city
        self.home_country = home_country

        self.gym = gym
        self.fighting_style = fighting_style

        self.record = record
        self.win_method = win_method
        self.physical_stats = physical_stats
        self.striking = striking
        self.grappling = grappling

    def __str__(self) -> str:
        return self.name
