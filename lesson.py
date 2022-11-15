from day import Day
from term import Term


class Lesson:
    def __init__(self, timetable, term, name, teacherName, year):
        self.__timetable = timetable
        self.__term = term
        self.__name = name
        self.__teacherName = teacherName
        self.__year = year
        self.__full_time = term.day == Day.SAT or term.day == Day.SUN
        timetable.put(self)

    @property
    def term(self):
        return self.__term

    @term.setter
    def term(self, value):
        self.__timetable.lessons.pop(self.__term.dict_key())
        self.__timetable.lessons[value.dict_key()] = self
        self.__term = value
        self.__full_time = self.term.day == Day.SAT or self.term.day == Day.SUN

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def teacherName(self):
        return self.__teacherName

    @teacherName.setter
    def teacherName(self, value):
        self.__teacherName = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def full_time(self):
        return self.__full_time

    def ValidateTime(self, hour, minute):
        lim = self.__timetable.limits[self.__term.day.value]
        return not (lim[0] > hour or lim[2] < hour or (lim[0] == hour and lim[1] > minute) or (
                    lim[2] == hour and lim[3] < minute))

    def Validate(self):
        return self.ValidateTime(self.__term.hour, self.__term.minute) and self.ValidateTime(
            self.__term.hour + self.__term.duration // 60, self.__term.minute + self.__term.duration % 60)

    def __str__(self):
        if self.__year == 1:
            y = 'Pierwszy rok'
        elif self.__year == 2:
            y = 'Drugi rok'
        elif self.__year == 3:
            y = 'Trzeci rok'
        elif self.__year == 4:
            y = 'Czwarty rok'
        elif self.__year == 5:
            y = 'Piąty rok'

        return f'{self.__name} ({self.__term})\n{y} studiów {"stacjonarnych" if self.__full_time else "niestacjonarnych"}\nProwadzący: {self.__teacherName}'

    def earlierDay(self):
        if self.__term.day == Day.MON or self.__term.day == Day.SAT:
            return False
        t = Term(Day(self.__term.day.value - 1), self.__term.hour, self.__term.minute, self.__term.duration)

        if self.__timetable.busy(t):
            return False

        self.term = t

        if not self.__timetable.can_be_transferred_to(self):
            self.laterDay()
            return False

        return True

    def laterDay(self):
        if self.__term.day == Day.FRI or self.__term.day == Day.SUN:
            return False
        t = Term(Day(self.__term.day.value + 1), self.__term.hour, self.__term.minute, self.__term.duration)

        if self.__timetable.busy(t):
            return False

        self.term = t

        if not self.__timetable.can_be_transferred_to(self):
            self.earlierDay()
            return False

        return True

    def earlierTime(self):
        ch = self.__term.hour
        cm = self.__term.minute

        hoursDelta = self.__term.duration // 60
        minutesDelta = self.__term.duration % 60

        h = ch
        m = cm
        h -= hoursDelta
        m -= minutesDelta

        if m < 0:
            h -= 1
            m += 60

        if self.__timetable.busy(Term(self.__term.day, h, m, 0)):
            return False

        self.term = Term(self.__term.day, h, m, self.__term.duration)

        if not self.__timetable.can_be_transferred_to(self):
            self.term = Term(self.__term.day, ch, cm, self.__term.duration)
            return False

        return True

    def laterTime(self):
        ch = self.__term.hour
        cm = self.__term.minute

        hoursDelta = self.__term.duration // 60
        minutesDelta = self.__term.duration % 60

        h = ch
        m = cm
        h += hoursDelta
        m += minutesDelta

        if m > 59:
            h += 1
            m -= 60

        if self.__timetable.busy(Term(self.__term.day, h, m, 0)):
            return False

        self.term = Term(self.__term.day, h, m, self.__term.duration)

        if not self.__timetable.can_be_transferred_to(self):
            self.term = Term(self.__term.day, ch, cm, self.__term.duration)
            return False

        return True

    def __eq__(self, l):
        return l != None and l.__term == self.__term and l.__name == self.__name and l.__teacherName == self.__teacherName and l.__year == self.__year
