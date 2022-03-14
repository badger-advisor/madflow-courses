from typing import List
import requests
import json

# Types
Courses = List[dict]


url = "https://public.enroll.wisc.edu/api/search/v1"
terms = {"spring2022": "1224", "summer2022": "1226", "fall2022": "1232", "all": "0000"}
subjects = {"COMP SCI": "266"}
headers = {"Content-Type": "application/json"}

# no idea why this is needed for specific terms
magic_object = {
    "has_child": {
        "type": "enrollmentPackage",
        "query": {"match": {"published": True}},
    }
}


def get_courses(subject="COMP SCI", term="all") -> tuple[int, Courses] | None:
    """Returns a tuple of number of returned courses and a list of the courses"""

    # default payload for all requests
    payload = {
        "queryString": "*",
        "page": 1,
        "pageSize": 50,
        "sortOrder": "SCORE",
        "selectedTerm": terms.get(term),
        "filters": [{"term": {"subject.subjectCode": subjects.get(subject)}}],
    }

    if term != "all":
        payload["filters"].append(magic_object)

    # HTTP POST request
    res = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    # if bad request
    if not res.ok:
        print(res.json().get("message"))
        return

    found, courses, message, success = res.json().values()

    return found, courses if success else None


def main():
    # upcoming_courses = requests.request(
    #     "POST", url, headers=headers, data=payload
    # ).json()

    # print(upcoming_courses["hits"][0].keys())

    # with open("courses_raw.json", "w") as f:
    #     f.write(json.dumps(upcoming_courses))
    print(get_courses("COMP SCI")[0])


# get all courses
# get next semester courses
# update existing courses
if __name__ == "__main__":
    main()
