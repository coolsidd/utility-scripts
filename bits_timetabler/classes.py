import sys
import ast
import csv
import string_distance
import re
import progressbar


def select_and_return(k, option="exit"):
    while True:
        for i in range(len(k)):
            print("{} {}".format(str(i), str(k[i])))
        print("-1 to {}".format(option))
        ans = input()
        if re.match(r"^[\-]?[0-9]+$", ans):
            if int(ans) == -1:
                return None
            elif -1 < int(ans) < len(k):
                return k[int(ans)]
            else:
                print("Enter a valid digit")


def prompt_yes():
    print("Are you sure?")
    while True:
        ans = input("Y/n ")
        ans = ans.lower().strip()
        if ans == 'y':
            return True
        elif ans == 'n':
            return False
        else:
            print("Please enter y/n")


class Subject:

    def __init__(self, comCode, courseCode, courseTitle,
                 lectureHours, practicalHours, units, compreDate):
        # credit as LPU should have format "x y z" where x is the no. of
        # lectures, y is the no. of practicals and so on..
        self.selected = False
        self.satisfied = False
        self.comCode = comCode
        self.courseCode = courseCode
        self.courseTitle = courseTitle
        self.lectureHours = lectureHours
        self.practicalHours = practicalHours
        self.units = units
        self.compreDate = compreDate
        self.instructors = []
        self.tutorials = []  # lectures, practicals and tutorials
        self.practicals = []
        self.lectures = []

    def __iter__(self):
        return iter(self.lectures+self.practicals+self.tutorials)

    def __str__(self):
        return "{:4} {:10} {}".format(self.comCode, self.courseCode,
                                      self.courseTitle)

    def __repr__(self):
        return "Subject: {} {}".format(self.courseCode, self.courseTitle)

    def __gt__(self, otherSubject):
        return self.courseCode > otherSubject.courseCode

    def __eq__(self, otherSubject):
        if otherSubject is not None:
            return self.courseTitle == otherSubject.courseTitle
        else:
            return False

    def __ge__(self, otherSubject):
        return self.courseTitle >= otherSubject.courseTitle

    def add_slot(self, slot):
        if slot.slotType == "Lecture" and slot not in self.lectures:
            self.lectures.append(slot)
        if slot.slotType == "Tutorial" and slot not in self.tutorials:
            self.tutorials.append(slot)
        if slot.slotType == "Practical" and slot not in self.practicals:
            self.practicals.append(slot)

    def add_instructor(self, instructor):
        if instructor not in self.instructors:
            self.instructors.append(instructor)

    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary["comCode"], dictionary["courseCode"],
                   dictionary["courseTitle"], int(dictionary["L"]),
                   int(dictionary["P"]), int(dictionary["U"]),
                   dictionary["compreDate"])

    def select(self):
        if self.selected is False:
            print("select {}?".format(self.courseCode))
            if prompt_yes():
                self.selected = True
                print("{} selected".format(self.courseCode))
                return (self)
            else:
                return None
        else:
            print("Already selected, remove?")
            if prompt_yes():
                self.selected = False
                print("{} Removed".format(self.courseCode))
                return None
            else:
                print("Nothing changed")
                return None


class Instructor:

    def __init__(self, name, code, department):
        self.name = self.return_formatted_name(name)
        self.code = code
        self.department = department
        self.subjects = []
        self.sections = []

    def __repr__(self):
        return "Instructor: {} ({})".format(self.name, self.code)

    def __str__(self):
        return self.name

    def add_slot(self, slot):
        if slot not in self.sections:
            self.sections.append(slot)

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    @staticmethod
    def return_formatted_name(string):
        return string.title().strip()

    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary["instructorName"], dictionary["instructorId"],
                   dictionary["department"])

    def select(self):
        print("{} takes ".format(self.name))
        selection = select_and_return(self.subjects)
        if isinstance(selection, Subject):
            return selection.select()


class Section:
    def __init__(self, subject, sectionNo, slotType,
                 roomNo, days, hours):
        self.subject = subject
        self.sectionNo = sectionNo
        self.slotType = slotType
        self.instructors = []
        self.days = days
        self.hours = hours
        self.priority = -1

    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary["courseCode"], dictionary["sectionNo"],
                   dictionary["slotType"], dictionary["roomNo"],
                   ast.literal_eval(dictionary["days"]), ast.literal_eval(dictionary["hours"]))

    def __repr__(self):
        return "{:4} {} {}\t".format(str(self.subject), self.sectionNo, self.slotType)+(str(self.priority) if self.priority >= 0 else "")

    def add_instructor(self, instuctor):
        if instuctor not in self.instructors:
            self.instructors.append(instuctor)


class Timetable:
    def __init__(self):
        self.table = [[None for x in range(10)] for y in range(6)]
        self.slots = []

    def add_slot(self, slot):
        if slot.priority < 0:
            return False
        for day in slot.days:  # checking if conflicts are there
            for hour in slot.hours:
                if self.table[day][hour] is None:
                    continue
                else:
                    return False
        self.slots.append(slot)  # adding the slot to the timetable
        for day in slot.days:
            for hour in slot.hours:
                self.table[day][hour] = slot
        return self.seems_good()

    def seems_good(self):
        # Makes sure the time table has a lunch break and no other inconsistencies
        for day in self.table:
            if day[2] is None or day[3] is None or day[4] is None:
                continue
            else:
                return False
        else:
            return True

    @property
    def priority(self):
        priority = 0
        for slot in self.slots:
            priority += slot.priority
        return priority

    def write_into_csv(self, csvWriter):
        csvWriter.writerow(
            [self.priority]+[x for x in range(10)])
        for row in self.table:
            csvWriter.writerow(
                ['']+["{} {} {}".format(x.subject.courseCode, x.slotType, x.sectionNo)
                      for x in row if x is not None])
        csvWriter.writerow([" " for x in range(6)])


if __name__ == "__main__":
    total_timetables = 1000
    with open("./timetable_data.csv", "r") as csvData:
        csvReader = csv.DictReader(csvData)
        print("Loading the csv file into memory")
        print(csvReader.fieldnames)
        sections_dict = {}
        subjects_dict = {}
        instructor_dict = {}
        this_sub = None
        ins_name = None
        this_section = None

        def search(string, num_results=10):
            string = string.lower()
            results = []
            for k in instructor_dict.values():
                if string in k.name.lower():
                    heuristic = -1
                else:
                    heuristic = (string_distance.osa_distance(
                        string, k.name.lower(), ignore_case=True) - (
                            len(k.name)-len(string)))
                results.append((heuristic, k))

            for k in subjects_dict.values():
                if string in str(k).lower():
                    heuristic = -1
                else:
                    heuristic = string_distance.osa_distance(
                        string, str(k), ignore_case=True) - (
                            len(str(k))-len(string))
                results.append((heuristic, k))

            results.sort(key=lambda i: i[0])
            return results[:num_results]

        def search_and_select(selected_array):
            key = input("search for?\n")
            res = search(key)
            print("Results")
            choice = select_and_return([x for y, x in res])
            if choice is None:
                for k in selected_array:
                    if k.selected is False:
                        selected_array.remove(k)
                return
            else:
                selection = choice.select()
                selected_array += [selection] if (
                    (selection is not None) and
                    (selection not in selected_array)) else []
                for k in selected_array:
                    if k.selected is False:
                        selected_array.remove(k)
                return

        def generate_timetable(selected_array):
            requirements_list = []
            print("Please assign priority to sections in each subject")
            print("Higher values of the priority give more preference to that slot")
            print("Assigning negative values will make the program exlude that section")
            for subject in selected_array:
                print("Subject {}".format(str(subject)))
                slot = select_and_return(list(subject))
                while slot is not None:
                    priority = None
                    print("Priority for {}".format(slot))
                    print("Taken by:")
                    print(*(slot.instructors), sep="\n")
                    print("D {} H {}".format(
                        [x+1 for x in slot.days], [x+1 for x in slot.hours]))
                    while True:
                        priority = input(
                            """Number (Higher means better,negative values means never) """)
                        if not re.match(r"^[\-]?[0-9]+$", priority):
                            continue
                        else:
                            try:
                                priority = int(priority)
                                break
                            except ValueError:
                                continue
                    slot.priority = priority
                    slot = select_and_return(list(subject))
                requirements_list.append(subject.lectures)
                requirements_list.append(subject.tutorials)
                requirements_list.append(subject.practicals)
            while True:
                try:
                    requirements_list.remove([])
                except ValueError:
                    break
            tree_size = 1
            for x in requirements_list:
                tree_size *= len(x)
                print("{} {}".format(x[0].subject.courseCode, x[0].slotType))
                x.sort(key=lambda my_list: my_list.priority, reverse=True)
            print("Total requirements (LPU) = {}".format(len(requirements_list)))
            print("Tree size ~ {}".format(tree_size))
            print("Sorting Tree")
            tree_traverser = [tuple(0 for x in requirements_list)]
            print("Generating best {} Timetables".format(total_timetables))

            # For more info on how the timetables are generated google X+Y problem
            # and this stackexchange answer https://cs.stackexchange.com/questions/46910/efficiently-finding-k-smallest-elements-of-cartesian-product

            my_bar = progressbar.ProgressBar()
            # for i in progressbar.iterable(total_timetables):
            threshold = 1000000
            break_loop_after_iter = 0
            while len(timetable_list) < total_timetables:
                if break_loop_after_iter <= 0:
                    my_bar.__exit__()
                    print(
                        "Even after trying for 1 million iterations, we could not generate adequate amount of timetables...")
                    print("Giving up now :(")
                    print("Hopefully dtc will help ;P")
                    break
                break_loop_after_iter += 1
                tree_traverser.sort(key=lambda t: sum(
                    requirements_list[p][t[p]].priority for p in range(len(t))),
                    reverse=True)

                timetable = Timetable()
                try:
                    last = tree_traverser.pop(0)
                except IndexError:
                    break_loop_after_iter = threshold
                    continue
                for i in range(len(requirements_list)):
                    # Try attemting to build the timetable
                    if timetable.add_slot(requirements_list[i][last[i]]):
                        continue
                    # In case the timetable fails (clashes by overlapping slots etc) discard that timetable
                    else:
                        break
                else:
                    timetable_list.append(timetable)
                for k in range(len(last)):
                    tree_traverser.append(
                        tuple(last[p] if (p != k) or ((last[p]+1) >= len(requirements_list[k])) else last[p]+1 for p in range(len(last))))

                # Remove duplicates
                tree_traverser = list(set(tree_traverser))
                while True:
                    try:
                        tree_traverser.remove(last)
                    except ValueError:
                        break
                # Update loading bar
                my_bar.fraction(
                    max(len(timetable_list)/total_timetables, break_loop_after_iter/threshold))
            else:
                my_bar.__exit__()
            return timetable_list

        for row in csvReader:   # Loads the data from the csvFile
            this_sub = row["courseCode"]
            if this_sub not in subjects_dict:
                subjects_dict[this_sub] = Subject.from_dict(row)

            ins_name = Instructor.return_formatted_name(row["instructorName"])

            if ins_name not in instructor_dict:
                instructor_dict[ins_name] = Instructor.from_dict(row)

            this_section = " ".join((
                row["courseCode"], row["slotType"], row["sectionNo"]))

            if this_section not in sections_dict:
                sections_dict[this_section] = Section.from_dict(row)

            instructor_dict[ins_name].add_slot(
                sections_dict[this_section])
            instructor_dict[ins_name].add_subject(subjects_dict[this_sub])

            subjects_dict[this_sub].add_instructor(
                instructor_dict[ins_name])
            subjects_dict[this_sub].add_slot(
                sections_dict[this_section])

            sections_dict[this_section].subject = subjects_dict[this_sub]
            sections_dict[this_section].add_instructor(
                instructor_dict[ins_name])

        print("Data Loaded")
        selected_array = []
        timetable_list = []
        while True:
            print("You have selected:")
            for k in selected_array:
                print(k)
            print("Do you want to edit?")
            if prompt_yes:
                opt = ["add entries", "delete entries"]
                ch = select_and_return(opt, "continue")
                if ch == opt[0]:
                    search_and_select(selected_array)

                elif ch == opt[1]:
                    k = select_and_return(selected_array)
                    try:
                        selected_array.remove(k)
                        k.selected = False
                    except ValueError:
                        pass
                    continue
                elif ch is None:
                    timetable_list = generate_timetable(selected_array)
                    break
            else:
                timetable_list = generate_timetable(selected_array)
                break
        print("Save where?")
        location = input("Enter name ")
        with open(location+".csv", "w") as csvFile:
            writer = csv.writer(csvFile)
            for table in timetable_list:
                table.write_into_csv(writer)
        print("Thanks for using bits-timetabler!!:]")
