import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    modules: int
    topics: int
    # duration: int
    course_type: CourseType


URL_MATE_BASE = "https://mate.academy/"


def get_single_course_info(course_common_info: BeautifulSoup, course_type: CourseType) -> Course:
    link_to_details_info = urljoin(URL_MATE_BASE,
                                   course_common_info.select_one("a.mb-16[href]")["href"])

    detailed_page = requests.get(link_to_details_info).content
    detailed_page_soup = BeautifulSoup(detailed_page, "html.parser")

    return Course(
        name=course_common_info.select_one(".typography_landingH3__vTjok").text,
        short_description=course_common_info.select_one(".CourseCard_courseDescription__Unsqj").text,
        modules=int(detailed_page_soup.select("p.CourseModulesHeading_text__EdrEk")[0].text.split()[0]),
        topics=int(detailed_page_soup.select("p.CourseModulesHeading_text__EdrEk")[1].text.split()[0]),
        course_type=course_type,
    )


def get_courses(soup_page: BeautifulSoup, time_type: str) -> [Course]:
    print(time_type)
    course_cards = soup_page.select(f"#{time_type} .CourseCard_cardContainer__7_4lK")
    return [get_single_course_info(course, time_type) for course in course_cards]


def get_all_courses() -> list[Course]:
    page = requests.get(URL_MATE_BASE).content
    mate_base_page_soup = BeautifulSoup(page, "html.parser")
    full_time = get_courses(mate_base_page_soup, CourseType.FULL_TIME.value)
    part_time = get_courses(mate_base_page_soup, CourseType.PART_TIME.value)

    return full_time + part_time


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
