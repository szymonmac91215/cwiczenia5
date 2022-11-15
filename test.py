import unittest
from basicterm import BasicTerm
from BasicTimetable import BasicTimetable
from bbreak import Break
from day import Day
from term import Term
from lesson import Lesson
from TimetableWithBreaks import Timetable2


class Test(unittest.TestCase):
    def test_false(self):
        t = Timetable2(False, [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10)), Break(BasicTerm(12, 45, 5)),
                               Break(BasicTerm(14, 20, 20)), Break(BasicTerm(16, 10, 5)), Break(BasicTerm(17, 45, 5)),
                               Break(BasicTerm(19, 20, 10))])
        l1 = Lesson(t, Term(Day.TUE, 8, 00), "Angielski", "dr A", 1)
        l2 = Lesson(t, Term(Day.MON, 9, 30), "JTP", "dr B", 2)  # Nie został dodany, bo koliduje z przerwą
        l3 = Lesson(t, Term(Day.FRI, 16, 15), "MOWNiT", "dr C", 2)
        l4 = Lesson(t, Term(Day.MON, 8, 00), "Programowanie", "dr D", 1)
        print(str(t))

        self.assertFalse(l1.laterTime())  # Kolizja z przerwą
        self.assertFalse(l3.earlierTime())  # Kolizja z przerwą

        self.assertFalse(l4.laterDay())  # Kolizja z l1 (Angielski)
        self.assertFalse(l4.earlierDay())  # Rezultat: niedziela - tylko zaoczne

        self.assertTrue(l1.laterDay())
        self.assertTrue(l4.laterDay())

        print(str(t))

    def test_true(self):
        print()
        t = Timetable2(True, [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10)), Break(BasicTerm(12, 45, 5)),
                              Break(BasicTerm(14, 20, 20)), Break(BasicTerm(16, 10, 5)), Break(BasicTerm(17, 45, 5)),
                              Break(BasicTerm(19, 20, 10))])
        l1 = Lesson(t, Term(Day.TUE, 8, 00), "Angielski", "dr A", 1)
        l2 = Lesson(t, Term(Day.MON, 9, 30), "JTP", "dr B", 2)  # Nie został dodany, bo koliduje z przerwą
        l3 = Lesson(t, Term(Day.FRI, 16, 15), "MOWNiT", "dr C", 2)
        l4 = Lesson(t, Term(Day.MON, 8, 00), "Programowanie", "dr D", 1)
        print(str(t))

        self.assertTrue(l1.laterTime())
        self.assertTrue(l3.earlierTime())

        self.assertFalse(l2.earlierTime())  # Wyjście poza ograniczenia czasowe

        self.assertTrue(l4.laterDay())
        self.assertFalse(l4.laterTime())  # Kolizja z l1 (Angielski)

        self.assertTrue(l3.earlierDay())

        print(str(t))

    def test_exception(self):
        bt = BasicTimetable()
        with self.assertRaises(ValueError) as c:
            bt.parse(["a"])

        with self.assertRaises(ValueError) as c:
            Term(Day.MON, 28, 0, 20)

        with self.assertRaises(ValueError) as c:
            Term(Day.MON, 12, -8, 20)

        with self.assertRaises(ValueError) as c:
            Term(Day.MON, 12, 0, -20)


if __name__ == '__main__':
    unittest.main()
