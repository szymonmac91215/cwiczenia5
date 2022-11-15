from day import Day
import re


class BasicTerm:
    def __init__(self, h, m, duration=90):
        if h < 0 or h > 23 or m < 0 or m > 59:
            raise ValueError("Nieprawidłowy czas rozpoczęcia.")
        if duration < 0:
            raise ValueError("Długość zajęć musi być dodatnia.")
        self.__hour = h
        self.__minute = m
        self.__duration = duration

    @property
    def hour(self):
        return self.__hour

    @property
    def minute(self):
        return self.__minute

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if value < 0:
            raise ValueError("Długość zajęć musi być dodatnia.")
        self.__duration = value

    def is_between(self, t1, t2):
        if t1.__hour > self.__hour or t2.__hour < self.__hour:
            return False
        if t1.__hour == self.__hour and t1.__minute > self.__minute:
            return False
        if t2.__hour == self.__hour and t2.__minute < self.__minute:
            return False
        return True

    def end(self):
        hoursDelta = self.__duration // 60
        minutesDelta = self.__duration % 60
        h = self.__hour + hoursDelta
        m = self.__minute + minutesDelta

        if m > 59:
            h += 1
            m -= 60

        return BasicTerm(h, m, self.__duration)

    def __str__(self):
        hoursDelta = self.__duration // 60
        minutesDelta = self.__duration % 60
        if self.__minute + minutesDelta > 59:
            hoursDelta += 1
            minutesDelta -= 60
        return f'{self.__hour}:{self.__minute:02d}-{self.__hour + hoursDelta}:{self.__minute + minutesDelta:02d}'
