from datetime import date
from operator import itemgetter
from pathlib import Path

import toml
from more_itertools import chunked

from tm_parser.config import Config

rank_requirements = toml.load(Path(__file__).parent / "data" / "requirements.toml")

eagle_badges_by_name = {}

for requirement, data in rank_requirements["Eagle"]["requirements"]["03"].items():
    if len(requirement) < 2:  # the requirement is one of the single-letter variety
        for badge in data["text"].split(" OR "):
            eagle_badges_by_name[badge] = requirement

alternate_names = Config.MB_ALTERNATE_NAMES


def allocate_merit_badges(merit_badges):

    if len(merit_badges) == 0:
        return None, None, None

    eagle_badges, palm_badges = get_eagle_badges(merit_badges)

    life_badges = get_life_badges(merit_badges)
    star_badges = get_star_badges(merit_badges)

    return star_badges, life_badges, eagle_badges, palm_badges


def get_eagle_badges(merit_badges):
    eagle_badges = {}
    for badge in sorted(
        filter(itemgetter("Eagle Required"), merit_badges.values()),
        key=itemgetter("Date"),
    ):

        name = alternate_names.get(badge["Name"], badge["Name"])

        slot = eagle_badges_by_name.get(name)

        if slot not in eagle_badges:
            eagle_badges[slot] = badge

    remaining_badges = [
        badge for badge in merit_badges.values() if badge not in eagle_badges.values()
    ]

    for slot, badge in zip("opqrstu", sorted(remaining_badges, key=itemgetter("Date"))):
        eagle_badges[slot] = badge

    palm_badges = [
        badge for badge in remaining_badges if badge not in eagle_badges.values()
    ]

    if all(eagle_badges.get(slot) for slot in "abcdefghijklmnopqrstu"):
        eagle_badges["Completed"] = True
    else:
        eagle_badges["Completed"] = False

    return eagle_badges, palm_badges


def get_life_badges(merit_badges):
    eagle_badges = sorted(
        filter(itemgetter("Eagle Required"), merit_badges.values()),
        key=itemgetter("Date"),
    )
    life_badges = {}

    life_badges["Eagle Badges"] = eagle_badges[0:7]  # first 7 must be eagle required
    remaining_badges = sorted(
        [
            badge
            for badge in merit_badges.values()
            if badge not in life_badges.get("Eagle Badges")
        ],
        key=itemgetter("Date"),
    )

    life_badges["Elective Badges"] = remaining_badges[0:4]

    if (
        len(life_badges.get("Eagle Badges")) == 7
        and len(life_badges.get("Elective Badges")) == 4
    ):
        life_badges["Completed"] = True
    else:
        life_badges["Completed"] = False

    return life_badges


def get_star_badges(merit_badges):
    eagle_badges = sorted(
        filter(itemgetter("Eagle Required"), merit_badges.values()),
        key=itemgetter("Date"),
    )
    star_badges = {}

    star_badges["Eagle Badges"] = eagle_badges[0:4]  # first 4 must be eagle required
    remaining_badges = sorted(
        [
            badge
            for badge in merit_badges.values()
            if badge not in star_badges.get("Eagle Badges")
        ],
        key=itemgetter("Date"),
    )

    star_badges["Elective Badges"] = remaining_badges[0:2]

    if (
        len(star_badges.get("Eagle Badges")) == 4
        and len(star_badges.get("Elective Badges")) == 2
    ):
        star_badges["Completed"] = True
    else:
        star_badges["Completed"] = False

    return star_badges


def record_star_badges(badges, scout):
    scout["Advancement"]["Ranks"]["Star"]["Requirements"]["03"] = {}

    for badge, code in zip(badges["Eagle Badges"], "abcd"):
        scout["Advancement"]["Ranks"]["Star"]["Requirements"][f"03{code}"] = {
            "Date": badge.get("Date"),
            "Badge": badge,
        }

    for badge, code in zip(badges["Elective Badges"], "ef"):
        scout["Advancement"]["Ranks"]["Star"]["Requirements"][f"03{code}"] = {
            "Date": badge.get("Date"),
            "Badge": badge,
        }

    if badges["Completed"]:
        scout["Advancement"]["Ranks"]["Star"]["Requirements"]["03"]["Date"] = max(
            badge["Date"]
            for badge in (*badges["Eagle Badges"], *badges["Elective Badges"])
        )


def record_life_badges(badges, scout):
    scout["Advancement"]["Ranks"]["Life"]["Requirements"]["03"] = {}
    for badge, code in zip(badges["Eagle Badges"][4:7], "abc"):
        scout["Advancement"]["Ranks"]["Life"]["Requirements"][f"03{code}"] = {
            "Date": badge.get("Date"),
            "Badge": badge,
        }

    for badge, code in zip(badges["Elective Badges"][2:4], "de"):
        scout["Advancement"]["Ranks"]["Life"]["Requirements"][f"03{code}"] = {
            "Date": badge.get("Date"),
            "Badge": badge,
        }

    if badges["Completed"]:
        scout["Advancement"]["Ranks"]["Life"]["Requirements"]["03"]["Date"] = max(
            badge["Date"]
            for badge in (*badges["Eagle Badges"], *badges["Elective Badges"])
        )


def record_eagle_badges(badges, scout):
    scout["Advancement"]["Ranks"]["Eagle"]["Requirements"]["03"] = {}
    for code in "abcdefghijklmnopqrstu":
        if "Date" in badges.get(code, []):
            scout["Advancement"]["Ranks"]["Eagle"]["Requirements"][f"03{code}"] = {
                "Date": badges.get(code)["Date"],
                "Badge": badges.get(code),
            }

    if badges["Completed"]:
        scout["Advancement"]["Ranks"]["Eagle"]["Requirements"]["03"]["Date"] = max(
            badges.get(code)["Date"] for code in "abcdefghijklmnopqrstu"
        )

    elif eagle_complete_before_cit_society_required(scout):
        scout["Advancement"]["Ranks"]["Eagle"]["Requirements"]["03"]["Date"] = max(
            badges.get(code)["Date"] for code in "abcefghijklmnopqrstu"
        )


def record_palm_badges(badges, scout):
    badges.sort(key=itemgetter("Date"))
    for badge_group, name in zip(
        chunked(badges, 5), rank_requirements["Eagle Palms"]["names"]
    ):
        if name not in scout["Advancement"]["Ranks"]:
            scout["Advancement"]["Ranks"][name] = {}
            scout["Advancement"]["Ranks"][name]["Requirements"] = {}
        scout["Advancement"]["Ranks"][name]["Requirements"]["04"] = {}
        for badge, code in zip(badge_group, "abcde"):
            scout["Advancement"]["Ranks"][name]["Requirements"][f"04{code}"] = {
                "Date": badge["Date"],
                "Badge": badge,
            }

        if len(badge_group) == 5:
            scout["Advancement"]["Ranks"][name]["Requirements"]["04"]["Date"] = max(
                (badge["Date"] for badge in badge_group)
            )


def eagle_complete_before_cit_society_required(scout):
    # Does the scout have all non-merit badge requirements complete?
    if not all(
        (
            scout["Advancement"]["Ranks"]["Eagle"]["Requirements"].get(requirement)
            for requirement in ["01", "02", "04", "05", "06"]
        )
    ):
        return False

    # Does the scout have any of the requirements completed after 2022/07/01?
    if any(
        (
            scout["Advancement"]["Ranks"]["Eagle"]["Requirements"][requirement]["Date"]
            >= date(2022, 7, 1)
            for requirement in ["01", "02", "04", "05", "06"]
        )
    ):
        return False

    # Does the scout have all non-Citizenship in Society (Merit badge d) merit badge requirements complete?
    if not all(
        (
            scout["Advancement"]["Ranks"]["Eagle"]["Requirements"]["03"].get(code)
            for code in "abcefghijklmnopqrstu"
        )
    ):
        return False

    # Did the scout complete any of the merit badges after 2022/07/01?
    if any(
        (
            scout["Advancement"]["Ranks"]["Eagle"]["Requirements"]["03"][code].get(
                "Date"
            )
            >= date(2022, 7, 1)
            for code in "abcefghijklmnopqrstu"
        )
    ):
        return False

    # The scout had all requirements other than the board of review and citizenship in society completed before
    # 2021/06/01. Therefore, they do not need Citizenship in Society MB

    return True
