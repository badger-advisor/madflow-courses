from typing import List
import requests
import json

# Types
Courses = List[dict]

# https://public.enroll.wisc.edu/search
url = "https://public.enroll.wisc.edu/api/search/v1"
terms = {"spring2022": "1224", "summer2022": "1226", "fall2022": "1232", "all": "0000"}
subjects = {"COMP SCI": "266", "MATH": "600"}
headers = {"Content-Type": "application/json"}

# no idea why this is needed for specific terms
magic_object = {
    "has_child": {
        "type": "enrollmentPackage",
        "query": {"match": {"published": True}},
    }
}


def get_courses(subject="COMP SCI", term="all") -> tuple[int, Courses] | None:
    """Returns a tuple of (number of returned courses, and a list of the courses)"""

    try:
        subject_code = subjects[subject]
    except:
        raise KeyError("Subject doesn't exist")

    # default payload for all requests
    payload = {
        "queryString": "*",
        "page": 1,
        "pageSize": 900,
        "sortOrder": "SCORE",
        "selectedTerm": terms.get(term),
        "filters": [{"term": {"subject.subjectCode": subject_code}}],
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
    subject = "MATH"
    _, courses = get_courses(subject)

    try:
        file_name = "_".join(subject.split())
        with open(f"courses_raw_{file_name}.json", "x") as f:
            f.write(json.dumps(courses))
    except:
        print("file exists")


if __name__ == "__main__":
    main()
