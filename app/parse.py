import requests

from bs4 import BeautifulSoup, Tag
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
    duration: int | None
    course_type: CourseType


URL_MATE_BASE = "https://mate.academy/"


def get_details_info_of_course(link: str, time_type: CourseType) -> tuple:
    detailed_page = requests.get(link).content
    detailed_page_soup = BeautifulSoup(detailed_page, "html.parser")

    detailed_info = detailed_page_soup.select("p.CourseModulesHeading_text__EdrEk")
    modules, topics = [name.text.split()[0] for name in detailed_info[:2]]

    if time_type.value == time_type.FULL_TIME.value:
        duration = detailed_info[-1].text.split()[0]
    else:
        duration = None

    return modules, topics, duration


def get_info_about_course(course_common_info: Tag, time_type: CourseType) -> Course:

    link_to_details_info = urljoin(URL_MATE_BASE,
                                   course_common_info.select_one("a.mb-16[href]")["href"])

    modules, topics, duration = get_details_info_of_course(link_to_details_info, time_type)

    return Course(
        name=course_common_info.select_one(".typography_landingH3__vTjok").text,
        short_description=course_common_info.select_one(".CourseCard_courseDescription__Unsqj").text,
        modules=modules,
        topics=topics,
        duration=duration,
        course_type=time_type
    )


def get_courses(soup_page: BeautifulSoup, time_type: CourseType) -> [Course]:
    course_cards = soup_page.select(f"#{time_type.value} .CourseCard_cardContainer__7_4lK")
    return [get_info_about_course(course, time_type) for course in course_cards]


def get_all_courses() -> list[Course]:
    mate_base_page = requests.get(URL_MATE_BASE).content
    mate_base_page_soup = BeautifulSoup(mate_base_page, "html.parser")

    full_time = get_courses(mate_base_page_soup, CourseType.FULL_TIME)
    part_time = get_courses(mate_base_page_soup, CourseType.PART_TIME)

    return full_time + part_time


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
