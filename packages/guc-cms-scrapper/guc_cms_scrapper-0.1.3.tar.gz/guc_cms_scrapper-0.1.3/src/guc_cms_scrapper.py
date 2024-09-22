from dataclasses import dataclass
import datetime
from enum import Enum
import re
from bs4 import BeautifulSoup
import requests
import requests_ntlm


@dataclass
class CourseMetadata:
    id: int
    code: str
    name: str

    semester: int
    """
    Current semester of the course. For example: 52.
    Used in the URL (`sid` query parameter) to get the course page.
    """


class InvalidCredentialsError(Exception):
    pass


def get_authenticated_session(username: str, password: str) -> requests.Session:
    session = requests.Session()
    session.auth = requests_ntlm.HttpNtlmAuth(username, password)

    response = session.get("https://cms.guc.edu.eg")

    if response.status_code == 401:
        raise InvalidCredentialsError()

    return session


def get_courses(authenticated_session: requests.Session) -> list[CourseMetadata]:
    url = "https://cms.guc.edu.eg/apps/student/HomePageStn.aspx"

    response = authenticated_session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    courses = []

    for row in soup.select("#ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses > tr:not(:first-child)"):
        cells = row.select("td")
        name_full = cells[1].text.strip()  # (|DMET901|) Computer Vision (571) => (|{CODE}|) {NAME} ({ID})
        code, name, id = re.match(r"\(\|(.*)\|\) (.*) \((.*)\)", name_full).groups()
        semester = int(cells[5].text.strip())

        courses.append(CourseMetadata(id=int(id), code=code, name=name, semester=semester))

    return courses


class CourseItemType(str, Enum):
    LECTURE_SLIDES = "Lecture Slides"
    ASSIGNMENT = "Assignment"
    OTHER = "Other"


@dataclass
class CourseItem:
    title: str
    type: CourseItemType
    description: str
    url: str


@dataclass
class CourseWeek:
    start_date: datetime.datetime
    description: str
    items: list[CourseItem]


@dataclass
class CourseData:
    announcements: str
    weeks: list[CourseWeek]


def infer_course_item_type(raw_type: str) -> CourseItemType:
    if "Lecture" in raw_type:
        return CourseItemType.LECTURE_SLIDES
    elif "Assignment" in raw_type:
        return CourseItemType.ASSIGNMENT
    else:
        return CourseItemType.OTHER


def get_course_data(authenticated_session: requests.Session, course_id: int, semester: int) -> CourseData:
    url = f"https://cms.guc.edu.eg/apps/student/CourseViewStn.aspx?id={course_id}&sid={semester}"
    response = authenticated_session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    announcements = soup.select_one("#ContentPlaceHolderright_ContentPlaceHoldercontent_desc").text.strip()

    weeks = []
    for weekSoup in soup.select(".weeksdata"):
        start_date_str = weekSoup.select_one("h2").text.strip()  # Week: 2024-9-14 => Week: {DATE}
        start_date = datetime.datetime.strptime(start_date_str, "Week: %Y-%m-%d")

        description = weekSoup.find("strong", text="Description").parent.find_next_sibling("p").text.strip()
        week_items = []

        for itemSoup in weekSoup.select(".card-body"):
            titleSoup = itemSoup.select_one("[id^=content] :first-child")
            title = titleSoup.text.strip()
            type_raw = titleSoup.next_sibling.strip()
            type = infer_course_item_type(type_raw)
            description = itemSoup.select_one("div:nth-child(2)").text.strip()
            url = "https://cms.guc.edu.eg/" + itemSoup.select_one("a")["href"]
            week_items.append(CourseItem(title=title, type=type, description=description, url=url))

        weeks.append(CourseWeek(start_date=start_date, description=description, items=week_items))

    return CourseData(announcements=announcements, weeks=weeks)
