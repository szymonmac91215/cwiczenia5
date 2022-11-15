from typing import List
from day import Day
from term import Term
from lesson import Lesson
from action import Action


class BasicTimetable:
    def __init__(self):
        self.lessons = {}

    def get(self, term: Term) -> Lesson:
        return self.lessons[term.dict_key()] if term.dict_key() in self.lessons else None

    def put(self, lesson: Lesson) -> bool:
        if type(lesson) is not Lesson:
            raise TypeError("Argument 'put()' musi być typu 'Lesson'.")
        elif self.busy(lesson.term):
            raise ValueError("Wybrany termin jest już zajęty.")
        self.lessons[lesson.term.dict_key()] = lesson
        return True

    def parse(self, actions: List[str]) -> List[Action]:
        r = []
        for a in actions:
            if a == "d+":
                r.append(Action.DAY_LATER)
            elif a == "d-":
                r.append(Action.DAY_EARLIER)
            elif a == "t+":
                r.append(Action.TIME_LATER)
            elif a == "t-":
                r.append(Action.TIME_EARLIER)
            else:
                raise ValueError(f'Operacja {a} jest niepoprawna.')
        return r

    def perform(self, actions: List[Action]):
        i = 0

        for a in actions:
            if a == Action.DAY_EARLIER:
                list(self.lessons.values())[i].earlierDay()
            elif a == Action.DAY_LATER:
                list(self.lessons.values())[i].laterDay()
            elif a == Action.TIME_EARLIER:
                list(self.lessons.values())[i].earlierTime()
            elif a == Action.TIME_LATER:
                list(self.lessons.values())[i].laterTime()

            i = (i + 1) % len(list(self.lessons.values()))
