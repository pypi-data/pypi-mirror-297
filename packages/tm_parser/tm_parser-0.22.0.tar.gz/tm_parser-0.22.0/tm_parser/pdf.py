"""
pdf.py

contains utilities for parsing specifically 
troopmaster pdf files

"""

import re

# pymupdf
import fitz
from more_itertools import grouper, split_after, split_before

from .activity import get_activity_totals
from .config import Config
from .leadership import get_leadership_dates
from .merit_badge import get_full_merit_badges
from .merit_badge_allocation import (
    allocate_merit_badges,
    record_eagle_badges,
    record_life_badges,
    record_palm_badges,
    record_star_badges,
)
from .oa import get_oa_status
from .partial_merit_badge import get_partials
from .rank import get_rank_advancement
from .scout import get_scout_data
from .utils import get_date, section_markers_test

# get rid of ending colon and dot
CLEAN = "".maketrans("", "", ":.*")
SCOUT_DIVIDER = "Name:"

full_date_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")


def assemble_scout_info(scout_info, data):
    """take the information we found and assemble a scout dict object"""
    scout = {}
    scout["Data"] = scout_info
    for item in data:
        # the rank section doesn't have a title - insert one now
        if item[0] == "Scout":
            scout["Ranks"] = item
        elif item[0].startswith("Merit Badges : "):
            scout["Merit Badges"] = item[1:]
        else:
            # first item in the list is the section name
            scout[item[0]] = item[1:]
    scout["Advancement"] = {}
    return scout


def separate_scout_bio_section(lines):
    """split out the initial scout bio section from the rest"""
    first, rest = split_after(lines, lambda x: x.startswith("BSA ID"), 1)
    return first, rest


def parse_scout(data):
    """take a big list of data for one scout, split out the bio section,
    and the rest of the sections into lists
    then take each section and turn the list of data
    into a properly formatted dict of information
    """
    scout_info, rest = separate_scout_bio_section(data)
    rest = split_before(rest, section_markers_test)
    scout = assemble_scout_info(scout_info, rest)
    if "Data" in scout:
        scout["Data"] = get_scout_data(scout["Data"])

    if "Ranks" in scout:
        scout["Advancement"]["Ranks"] = get_rank_advancement(scout["Ranks"])
        del scout["Ranks"]

    if "Merit Badges" in scout:
        scout["Advancement"]["Merit Badges"] = get_full_merit_badges(
            scout["Merit Badges"]
        )
        star_badges, life_badges, eagle_badges, palm_badges = allocate_merit_badges(
            scout["Advancement"]["Merit Badges"]
        )

        del scout["Merit Badges"]

        if star_badges:
            record_star_badges(star_badges, scout)

        if life_badges:
            record_life_badges(life_badges, scout)

        if eagle_badges:
            record_eagle_badges(eagle_badges, scout)

        if palm_badges:
            record_palm_badges(palm_badges, scout)

    if "Activity Totals" in scout:
        scout["Activity Totals"] = get_activity_totals(scout["Activity Totals"])
    if "Order of the Arrow" in scout:
        scout["OA"] = get_oa_status(scout["Order of the Arrow"])
        del scout["Order of the Arrow"]
    if "Leadership" in scout:
        output = []
        for position, value in grouper(scout["Leadership"], 2):
            output.append({position: get_leadership_dates(value)})
        scout["Leadership"] = output
    for field in ["Training Courses", "Special Awards", "National Outdoor Awards"]:
        if field in scout:
            scout[field] = {
                item1: get_date(item2) for item1, item2 in grouper(scout[field], 2)
            }
    if "Partial Merit Badges" in scout:
        scout["Advancement"]["Merit Badge Requirements"] = get_partials(
            scout["Partial Merit Badges"]
        )
        del scout["Partial Merit Badges"]
    return scout


def parse_file(infile=None, stream=None):
    """parse the file and get the merit badges and names"""

    if infile:
        with fitz.open(infile) as in_file:
            raw_scouts = get_unparsed_scouts(in_file)
            return parse_scouts(raw_scouts)
    elif stream:
        with fitz.open(stream=stream) as in_file:
            raw_scouts = get_unparsed_scouts(in_file)
            return parse_scouts(raw_scouts)
    else:
        raise ValueError("no incoming filename or stream given")


def parse_scouts(raw_scouts):
    scouts = {}
    for scout in raw_scouts:
        scout_data = parse_scout(scout)
        scouts[scout_data["Data"]["Name"]] = scout_data
    return scouts


def get_unparsed_scouts(file):
    """take a file handle that's been opened
    strip out all the bad lines
    and return lists of lines - each list is one scout's information
    """
    lines = get_good_lines(file)
    return separate_scouts(lines)


def good_line(line):
    """a filter that rejects lines that should not be
    in the final report

    no blank lines
    no lines starting with "Page"
    no lines starting with "Verified
    no lines with "Individual History"
    no lines with "Position not credited toward rank"
    no lines with "(continued)"
    no lines with ________________
    no lines with a first digit and then more than 8 digits:
    this is to get rid of the date code like 03/04/2020
    since it does not correspond to any rank or other signoff,
    it's just the date of the report
    no lines that start with "Troop" unless they have  "Guide"
    """

    return all(
        (
            bool(line),
            not line.startswith("Page"),
            not line.startswith("Verified"),
            "Individual History" not in line,
            "Position not credited toward rank" not in line,
            "(continued)" not in line,
            "_________________" not in line,
            not re.match(full_date_pattern, line),
            not line.startswith("Troop") or "Guide" in line,
            not ("Council" in line and "Troop" in line),
            "Council Circle" not in line,
            "Pack" not in line,
            "Council MDSC" not in line,
        )
    )


def get_good_lines(file_obj):
    """take all the lines and reject the ones that are not needed in the data"""
    return (
        line
        for page in file_obj
        for line in page.get_textbox(Config.WHOLE_PAGE).split("\n")
        if good_line(line)
    )


def separate_scouts(lines):
    """take the collection of all lines and divide them into groups of information
    pertaining to an individual scout"""
    return split_before(lines, lambda x: x.startswith("Name:"))
