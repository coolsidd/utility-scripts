import openpyxl
import re


class Subject:
    instructors = []
    slots = []  # lectures, practicals and tutorials

    def __init__(this, comCode, courseCode, courseTitle, instructorInCharge,
                 creditAsLPU, compreDate):
        # credit as LPU should have format "x y z" where x is the no. of
        # lectures, y is the no. of practicals and so on..

        this.comCode = comCode
        this.courseCode = courseCode
        this.courseTitle = courseTitle
        this.LPU = creditAsLPU
        this.instructors[0] = instructorInCharge
        this.compreDate = compreDate

    def __str__(this):
        return "{} {} {}".format(this.comCode, this.courseCode,
                                 this.courseTitle)

    def __repr__(this):
        return "Subject({} {} {} {} {} {})".format(this.comCode,
                                                   this.courseCode,
                                                   this.courseTitle,
                                                   this.instructors[0],
                                                   this.LPU, this.department)

    def add_slot(this, slot):
        if slot.instructor not in this.instructors:
            this.instructors.append(slot.instructor)

        this.slots.append(slot)

    @classmethod
    def initializeFromCSV(cls, pathToCSV):
        with open(


class instructor:
    subjects=[]
    sections=[]

    def __init__(self, name, code):
        self.name=name
        self.code=code

    def __repr__(self):
        return "{} ({})".format(self.name, self.code)


class section:
    instructors=[]


    def __init__(self, subject, sectionNo, listOfInstructors, slotType,
                 roomNo, days, hours):
        # expects days and hours to be lists containing integers
        # expects slotType to be a single character string as follows :
        # 		"T": Tutorial
        # 		"L": Lecture
        # 		"P": Practical
        self.subject=subject
        self.sectionNo=sectionNo
        self.instructors=listOfInstructors
        self.slotType=slotType


if __name__ == "__main__":
    pass
