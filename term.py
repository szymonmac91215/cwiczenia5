from day import Day
from basicterm import BasicTerm
import re


class Term(BasicTerm):
    def __init__(self, d, h, m, duration=90):
        super().__init__(h, m, duration)
        self.__day = d

    @property
    def day(self):
        return self.__day

    def dict_key(self):
        return (self.__day, self.hour, self.minute)

    def __str__(self):
        hoursDelta = self.duration // 60
        minutesDelta = self.duration % 60
        if self.minute + minutesDelta > 59:
            hoursDelta += 1
            minutesDelta -= 60
        return f'{self.__day} {self.hour}:{self.minute:02d}-{self.hour + hoursDelta}:{self.minute + minutesDelta:02d}'

    def earlierThan(self, termin):
        if self.__day.difference(termin.__day) < 0:
            return False

        if self.__day.difference(termin.__day) > 0:
            return True

        if termin.__hour < self.__hour:
            return False

        if termin.__hour > self.__hour:
            return True

        if termin.__minute <= self.__minute:
            return False

        return True

    def laterThan(self, termin):
        if self.__day.difference(termin.__day) > 0:
            return False

        if self.__day.difference(termin.__day) < 0:
            return True

        if termin.__hour > self.__hour:
            return False

        if termin.__hour < self.__hour:
            return True

        if termin.__minute >= self.__minute:
            return False

        return True

    def equals(self, termin):
        return termin.__hour == self.__hour and termin.__minute == self.__minute and termin.__duration == self.__duration and self.__day == termin.__day

    def __lt__(self, termin):
        return self.earlierThan(termin)

    def __gt__(self, termin):
        return self.laterThan(termin)

    def __eq__(self, termin):
        return self.equals(termin)

    def __le__(self, termin):
        return self.earlierThan(termin) or self.equals(termin)

    def __ge__(self, termin):
        return self.laterThan(termin) or self.equals(termin)

    def __sub__(self, termin):
        return Term(termin.__day, termin.__hour, termin.__minute,
                    (self.__hour - termin.__hour) * 60 + (self.__minute - termin.__minute) + self.__duration)

