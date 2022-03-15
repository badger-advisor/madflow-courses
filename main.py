from courses import *
import json
import re


def process_data(courses):
    mongo_data = []
    for course in courses:
        course_name = course["courseDesignation"]
        last_taught = course["lastTaught"]
        credits = course["creditRange"]
        description = course["description"]
        title = course["title"]
        repeatable_bool = course["repeatable"] == "Y"
        prereqs = course["enrollmentPrerequisites"]
        numbers = re.findall(r"\d+", prereqs)
        prereq_courseList = []
        logic = []
        if len(numbers) > 0:
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
                                prereq_courseList += [subject + " " + number]
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
                    subject = re.findall(
                        r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", " ".join(words_before)
                    )[-1]
                    prereq_courseList += [subject + " " + number]

                if " or " in prereqs:
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
                            continue

                        elif (
                            (re.findall(r"\d+", or_split[i]) != [])
                            and (i != (len(or_split) - 1))
                            and (re.findall(r"\d+", or_split[i + 1]) == [])
                        ):
                            continue

                        elif (
                            (re.findall(r"\d+", or_split[i]) != [])
                            and (i != (len(or_split) - 1))
                            and (re.findall(r"\d+", or_split[i + 1]) != [])
                        ):
                            if "(" in or_split[i] and ")" in or_split[i + 1]:
                                start = or_split[i].split("(")[1]
                                end = or_split[i + 1].split(")")[0]
                                end_subj = re.findall(
                                    r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", end
                                )
                                if end_subj != []:
                                    # print(end_num, '---', end_subj[-1])
                                    end_num = re.findall(r"\d+", end)
                                    end_logic = (
                                        ' convertToBool("'
                                        + end_subj[-1]
                                        + " "
                                        + end_num[-1]
                                        + ")"
                                    )
                                else:
                                    # print(or_split[i], '---', or_split[i+1])
                                    end_num = re.findall(r"\d+", end)[0]
                                    start_subj = re.findall(
                                        r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", start
                                    )[-1]
                                    end_logic = (
                                        ' convertToBool("'
                                        + start_subj
                                        + " "
                                        + end_num
                                        + '")'
                                    )
                                start_nums = re.findall(r"\d+", start)
                                index = 0
                                start_logic = ""
                                for start_num in start_nums:
                                    start_ind = start.find(start_num)
                                    before_num = start[:start_ind]
                                    temp_subj = re.findall(
                                        r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", before_num
                                    )[-1]
                                    if index == 0:
                                        start_logic += (
                                            '(convertToBool("'
                                            + temp_subj
                                            + " "
                                            + start_num
                                            + '") ||'
                                        )
                                    else:
                                        start_logic += (
                                            ' convertToBool("'
                                            + temp_subj
                                            + " "
                                            + start_num
                                            + '") ||'
                                        )
                                logic += [start_logic + end_logic]

                            elif "," in or_split[i]:
                                end = or_split[i + 1]
                                start = or_split[i]
                                end_subj = re.findall(
                                    r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", end
                                )
                                if end_subj != []:
                                    # print(end_num, '---', end_subj[-1])
                                    end_num = re.findall(r"\d+", end)
                                    end_logic = (
                                        ' convertToBool("'
                                        + end_subj[-1]
                                        + " "
                                        + end_num[-1]
                                        + ")"
                                    )
                                else:
                                    end_num = re.findall(r"\d+", end)[0]
                                    start_subj = re.findall(
                                        r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", start
                                    )[-1]
                                    end_logic = (
                                        ' convertToBool("'
                                        + start_subj
                                        + " "
                                        + end_num
                                        + '")'
                                    )

                                start_nums = re.findall(r"\d+", start)
                                index = 0
                                start_logic = ""
                                for start_num in start_nums:
                                    start_ind = start.find(start_num)
                                    before_num = start[:start_ind]
                                    temp_subj = re.findall(
                                        r"\b[A-Z]+(?:[/\s]+[A-Z]+)*\b", before_num
                                    )[-1]
                                    if index == 0:
                                        start_logic += (
                                            '(convertToBool("'
                                            + temp_subj
                                            + " "
                                            + start_num
                                            + '") ||'
                                        )
                                    else:
                                        start_logic += (
                                            ' convertToBool("'
                                            + temp_subj
                                            + " "
                                            + start_num
                                            + '") ||'
                                        )
                                logic += [start_logic + end_logic]

        if len(logic) > 0:
            logic = logic[0]
        else:
            logic = ""
        mongo_entry = {
            "courseNumber": course_name,
            "info": {
                "courseName": title,
                "description": description,
                "credits": credits,
                "lastTaught": last_taught,
                "repeatable": str(repeatable_bool),
                "designation": "",
                "standing": "",
            },
            "prerequisites": {
                "courseList": prereq_courseList,
                "text": prereqs,
                "logic": logic,
            },
        }

        mongo_data += [mongo_entry]

    return mongo_data


def main():
    # get all courses
    # get next semester courses
    # update existing courses
    try:
        with open("courses_raw.json") as f:
            courses = json.load(f)
    except:
        n1, all_courses = get_courses()
        n2, upcoming_courses = get_courses(term="fall2022")
        with open("courses_raw.json", "x") as f:
            f.write(json.dumps(all_courses))

        courses = all_courses

    processed = process_data(courses)
    with open("output.json", "w") as f:
        f.write(json.dumps(processed))
    print(processed)


if __name__ == "__main__":
    main()
