from datetime import date, datetime
from enum import Enum
from os.path import dirname, join
import random

from openpyxl import Workbook

from openpyxl_templates.columns import ChoiceColumn, CharColumn, DateColumn, TextColumn, BooleanColumn, IntegerColumn, \
    FloatColumn, TimeColumn, DateTimeColumn
from openpyxl_templates.workbook import WorkbookTemplate
from openpyxl_templates.worksheet import SheetTemplate

DIR = dirname(__file__)


class Sexes(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Person:
    def __init__(self, first_name, last_name, date_of_birth, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex


persons = (
    Person(
        "Jane",
        "Doe",
        date(year=1983, month=3, day=10),
        Sexes.FEMALE
    ),
    Person(
        "John",
        "Doe",
        date(year=1992, month=9, day=3),
        Sexes.MALE
    ),
    Person(
        "Mickey",
        "Mouse",
        date(year=1972, month=3, day=10),
        Sexes.MALE
    ),
    Person(
        "Goofy",
        "",
        date(year=1972, month=3, day=10),
        Sexes.MALE
    ),
)


class SexColumn(ChoiceColumn):
    hidden = False
    choices = (
        ("Male", Sexes.MALE),
        ("Female", Sexes.FEMALE),
        ("Other", Sexes.OTHER)
    )
    add_list_validation = True


class PersonsSheet(SheetTemplate):
    columns = [
        CharColumn(
            object_attr="first_name",
            header="First name",
            width=15,
        ),
        CharColumn(
            object_attr="last_name",
            header="Last name",
            width=15,
        ),
        SexColumn(
            object_attr="sex",
            header="Sex"
        ),
        DateColumn(
            object_attr="date_of_birth",
            header="Date of birth",
            width=20
        )
    ]


class ElementObject:
    def __init__(self, char, text, boolean, i, f, choice, time, date, datetime):
        self.char = char
        self.text = text
        self.boolean = boolean
        self.i = i
        self.f = f
        self.choice = choice
        self.time = time
        self.date = date
        self.datetime = datetime


class ElementsSheet(SheetTemplate):
    title = "Title"
    description = "This is the description. It can be a couple of sentences long."

    columns = [
        CharColumn(object_attr="char", header="CharColumn", width=15),
        # TextColumn(object_attr="text", header="TextColumn",  width=20, hidden=True),
        BooleanColumn(object_attr="boolean", header="BooleanColumn", width=18),
        IntegerColumn(object_attr="i", header="IntegerColumn", width=18),
        FloatColumn(object_attr="f", header="FloatColumn", width=15),
        ChoiceColumn(object_attr="choice", header="ChoiceColumn", width=15,
                     choices=(("Choice 1", 1), ("Choice 2", 2), ("Choice 3", 3))),
        TimeColumn(object_attr="time", header="TimeColumn", width=18),
        DateColumn(object_attr="date", header="DateColumn", width=20),
        DateTimeColumn(object_attr="datetime", header="DateTimeColumn", width=20, hidden=True)
    ]


def generate_element_objects(count=100):
    from_date = datetime(year=1990, month=1, day=1).timestamp()
    to_date = datetime(year=2020, month=12, day=31).timestamp()

    dates = list(datetime.fromtimestamp(random.uniform(from_date, to_date)) for i in range(0, count))
    dates.sort()

    for i in range(0, count):
        float = random.random() * 1000
        date = dates[i]

        yield ElementObject(
            "Object %d" % (i + 1),
            "This is a text which\n will wrap by default",
            random.choice((True, False)),
            float,
            float,
            random.randint(1, 3),
            date,
            date,
            date
        )


class DemoTemplate(WorkbookTemplate):
    sheets = (
        PersonsSheet(sheetname="Persons", title="Persons"),
        ElementsSheet(sheetname="Elements")
    )
    active_sheet = "Elements"


if __name__ == "__main__":
    workbook = Workbook()
    template = DemoTemplate(workbook)
    template.remove_all_sheets()
    template.write_sheet("Persons", persons)
    template.write_sheet("Elements", generate_element_objects(count=100))
    workbook.save(join(DIR, "demo.xlsx").replace('\\', '/'))