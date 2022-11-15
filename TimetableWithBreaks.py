from typing import List
from BasicTimetable import BasicTimetable
from bbreak import Break
from day import Day
from term import Term
from lesson import Lesson
from action import Action


class Timetable2(BasicTimetable):
    limits = [(8, 0, 20, 0), (8, 0, 20, 0), (8, 0, 20, 0), (8, 0, 20, 0), (8, 0, 17, 0), (8, 0, 20, 0), (17, 0, 20, 0)]

    def __init__(self, skipBreaks: bool, breaks: List[Break]):
        super().__init__()
        self.breaks = breaks
        self.skipBreaks = skipBreaks

    def sum(self, day):
        s = 0
        for l in list(self.lessons.values()):
            if l.term.day != day:
                continue
            s += l.term.duration
            e = l.term.end()
            b = self.get_break_end(e.hour, e.minute)
            if self.get(Term(day, b.hour, b.minute)) != None:
                s += b.duration
        return s

    def can_be_transferred_to(self, lesson: Lesson) -> bool:
        return lesson.Validate() and self.break_check_end(lesson) and self.break_check(lesson)

    def break_check(self, lesson) -> bool:
        b = self.get_break_end(lesson.term.hour, lesson.term.minute)
        if b == None:
            return True
        if not self.skipBreaks:
            return False
        t = Term(lesson.term.day, b.hour, b.minute, lesson.term.duration)
        if self.busy(t):
            return False
        lesson.term = t
        return True

    def break_check_end(self, lesson) -> bool:
        b = self.get_break_end(lesson.term.end().hour, lesson.term.end().minute, True, False)
        if b == None:
            return True
        if not self.skipBreaks:
            return False
        t = Term(lesson.term.day, lesson.term.hour, lesson.term.minute - b.duration, lesson.term.duration)
        if self.busy(t):
            return False
        lesson.term = t
        return True

    def get_break_end(self, h, m, e=False, re=True) -> Term:
        for b in self.breaks:
            if e:
                b = b.term.end()
            else:
                b = b.term
            if b.hour == h and b.minute == m:
                return b.end() if re else b
        return None

    def busy(self, term: Term) -> bool:
        return self.get(term) != None

    def __str__(self):
        s = f'{"":<14}| '

        for i in range(1, 8):
            s += f'{str(Day(i)):<17}|  '
        s += "\n"
        for i in range(0, 14):
            s += "-"
        s += "|"

        for i in range(1, 8):
            for j in range(0, 19):
                if i == 1 and j == 0:
                    continue
                s += "-"
            s += "|"
        s += "\n"

        duration = 90

        h = 8
        m = 0
        ho = duration // 60
        mo = duration % 60

        while h < 21:
            hd = h + ho
            md = m + mo

            if md >= 60:
                hd += 1
                md -= 60

            s += f'{h:02d}:{m:02d}-{hd:02d}:{md:02d}   | '

            for i in range(1, 8):
                found = False
                for l in list(self.lessons.values()):
                    if l.term.day.value == i and l.term.hour == h and l.term.minute == m:
                        s += f'{l.name:<17}|  '
                        found = True
                        break

                if not found:
                    s += f'{"":<17}|  '

            if h != 18:
                s += f'\n{"":<14}|{"":<18}|{"":<19}|{"":<19}|{"":<19}|{"":<19}|{"":<19}|{"":<19}|\n'
            else:
                s += "\n\n"

            h = hd
            m = md

            b = self.get_break_end(h, m)
            if b != None:
                h = b.hour
                m = b.minute
        return s
