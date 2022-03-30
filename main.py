from courses import *
import json
import re

paren_regex = "\(([^)]+)\)"
major_regex = "\b[A-Z]+(?:[/\s]+[A-Z]+)*\b"
double_major_regex = "\b[A-Z ]+(?:[/]+[A-Z ]+)+\b"


def logic_trans(prereqs, numbers):
    paren_groups = re.findall(paren_regex, prereqs)
    print(paren_groups)
    for group in paren_groups:
        if "or" in group:
            print("OR group")
        elif "and" in group:
            print("AND group")

    # print(paren_idx)
    # return None, paren_idx


def prereq_to_logic(prereqs, numbers):
    logic = []
    prereq_courseList = []

    for number in numbers:
        ind = prereqs.find(number)
        words_before = prereqs[:ind].split()
        if words_before[-1].isupper():
            subject = ""
            for word in reversed(words_before):
                if word.isupper():
                    subject += word + " "

                    if len(words_before) == 1:
                        subject = subject.replace("(", "")
                        prereq_courseList += [subject + number]
                        break
                    elif words_before.index(word) == 0:
                        subject = subject.split()
                        subject.reverse()
                        subject = " ".join(subject)
                        subject = subject.replace("(", "")
                        subject = subject.replace(")", "")
                        prereq_courseList += [subject + " " + number]
                        break
                else:
                    print("reverse")
                    subject = subject.split()
                    subject.reverse()
                    subject = " ".join(subject)
                    subject = subject.replace("(", "")
                    subject = subject.replace(")", "")
                    prereq_courseList += [subject + " " + number]
                    break
        elif (
            (words_before[-1] == "or")
            or (words_before[-1] == "and")
            or (words_before[-1][-1] == ",")
        ):
            subject = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", " ".join(words_before))[-1]
            prereq_courseList += [subject + " " + number]

        if " or " in prereqs:
            # TODO "(or" split
            or_split = prereqs.split(" or ")
            for i in range(0, len(or_split), 2):
                if " AP" in or_split[i]:
                    or_split[i] = or_split[i].replace(
                        "Score of 3 on Computer Science (A) AP\nExam, ", ""
                    )
                if (
                    (re.findall(r"\d+", or_split[i]) == [])
                    and (i != (len(or_split) - 1))
                    and (re.findall(r"\d+", or_split[i + 1]) == [])
                ):
                    # if or_split[i] or or_split[i+1] has no courses
                    continue

                elif (
                    (re.findall(r"\d+", or_split[i]) != [])
                    and (i != (len(or_split) - 1))
                    and (re.findall(r"\d+", or_split[i + 1]) == [])
                ):
                    # if or_split[i+1] has no courses
                    continue

                elif (
                    (re.findall(r"\d+", or_split[i]) != [])
                    and (i != (len(or_split) - 1))
                    and (re.findall(r"\d+", or_split[i + 1]) != [])
                ):
                    # if both [i] and [i+1] has courses

                    if "(" in or_split[i] and ")" in or_split[i + 1]:
                        start = or_split[i].split("(")[1]
                        end = or_split[i + 1].split(")")[0]
                        end_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", end)
                        if end_subj != []:
                            # print(end_num, '---', end_subj[-1])
                            end_num = re.findall(r"\d+", end)
                            end_logic = ' convertToBool("' + end_subj[-1] + " " + end_num[-1] + ")"
                        else:
                            # print(or_split[i], '---', or_split[i+1])
                            end_num = re.findall(r"\d+", end)[0]
                            start_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", start)[-1]
                            end_logic = ' convertToBool("' + start_subj + " " + end_num + '")'
                        start_nums = re.findall(r"\d+", start)
                        index = 0
                        start_logic = ""
                        for start_num in start_nums:
                            start_ind = start.find(start_num)
                            before_num = start[:start_ind]
                            temp_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", before_num)[-1]
                            if index == 0:
                                start_logic += (
                                    '(convertToBool("' + temp_subj + " " + start_num + '") ||'
                                )
                            else:
                                start_logic += (
                                    ' convertToBool("' + temp_subj + " " + start_num + '") ||'
                                )
                        logic += [start_logic + end_logic]

                    elif "," in or_split[i]:
                        end = or_split[i + 1]
                        start = or_split[i]
                        end_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", end)
                        if end_subj != []:
                            # print(end_num, '---', end_subj[-1])
                            end_num = re.findall(r"\d+", end)
                            end_logic = ' convertToBool("' + end_subj[-1] + " " + end_num[-1] + ")"
                        else:
                            end_num = re.findall(r"\d+", end)[0]
                            start_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", start)[-1]
                            end_logic = ' convertToBool("' + start_subj + " " + end_num + '")'

                        start_nums = re.findall(r"\d+", start)
                        index = 0
                        start_logic = ""
                        for start_num in start_nums:
                            start_ind = start.find(start_num)
                            before_num = start[:start_ind]
                            temp_subj = re.findall(r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", before_num)[-1]
                            if index == 0:
                                start_logic += (
                                    '(convertToBool("' + temp_subj + " " + start_num + '") ||'
                                )
                            else:
                                start_logic += (
                                    ' convertToBool("' + temp_subj + " " + start_num + '") ||'
                                )
                        logic += [start_logic + end_logic]

    return prereq_courseList, logic


def process_data(courses):
    course_data = []

    for course in courses:
        course_name = course["courseDesignation"]
        last_taught = course["lastTaught"]
        credits = course["creditRange"]
        description = course["description"]
        title = course["title"]
        repeatable_bool = course["repeatable"] == "Y"
        prereqs = course["enrollmentPrerequisites"]
        numbers = re.findall(r"\d+", prereqs)  # finds all '000' numbers in prereqs
        prereq_courseList = None
        logic = None

        print(numbers)
        # if course has other course prereqs
        if numbers:
            prereq_courseList, logic = prereq_to_logic(prereqs, numbers)

        formatted = {
            "courseNumber": course_name,
            "info": {
                "courseName": title,
                "description": description,
                "credits": credits,
                "lastTaught": last_taught,
                "repeatable": repeatable_bool,
                "designation": "",  # to be implemented
                "standing": "",  # to be implemented
            },
            "prerequisites": {
                "courseList": prereq_courseList,
                "text": prereqs,
                "logic": logic,
            },
        }

        print(f"appending: {formatted['courseNumber']}")
        course_data.append(formatted)

    return course_data


def main():
    subject = "COMP SCI"
    subject = "_".join(subject.split())
    file_name = f"courses_raw_{subject}.json"

    # get all courses
    # get next semester courses
    # update existing courses
    try:
        with open(file_name) as f:
            courses = json.load(f)
    except:
        n1, all_courses = get_courses()
        n2, upcoming_courses = get_courses(term="fall2022")
        with open(file_name, "x") as f:
            f.write(json.dumps(all_courses))

        courses = all_courses

    # parse courses and compute logic
    processed = process_data(courses[20:22])

    # write to output
    with open(f"output_{subject}.json", "w") as f:
        f.write(json.dumps(processed))

    # print(processed)


def test_parse():
    prereq = str(
        "MATH 376, (MATH 234 and 319), (MATH 234 and 320), (MATH 234 and 340), "
        "(MATH 234 and 341) or (MATH 234 and 375) or graduate/professional standing "
        "or member of the Pre-Masters Mathematics (Visiting International) program"
    )

    # prereqs = "(COMP SCI 300 or 302)"

    prereq = "Satisfied QR-A requirement and (COMP SCI 200, 220, 302, 310, or 301) or (COMP SCI/E C E 252 and E C E 203); graduate/professional standing; or declared in the Capstone Certificate in Computer Sciences. Not open to students with credit for COMP SCI 367."

    prereq = "MATH 222 and (COMP SCI/MATH 240 or MATH 234) and (COMP SCI 200, 300, 301, 302, or 310) or graduate/professional standing or declared in the Capstone Certificate in Computer Sciences for Professionals"

    numbers = re.findall(r"\d+", prereq)  # finds all 'xxx' numbers in prereqs
    logic = None

    if numbers:
        # prereq_courseList, logic = logic_trans(prereq, numbers)
        logic_trans(prereq, numbers)

    # print(prereq)
    # print(logic)


"Satisfied QR-A requirement and (COMP SCI 200, 220, 302, 310, or 301) or (COMP SCI/E C E 252 and E C E 203); graduate/professional standing; or declared in the Capstone Certificate in Computer Sciences. Not open to students with credit for COMP SCI 367."

if __name__ == "__main__":
    # main()
    test_parse()
