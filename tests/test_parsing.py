# -*- coding: utf-8 -*-
from unittest import TestCase
from datetime import timedelta, date, datetime
from chatterbot.utils.parsing import datetime_parsing, this_week_day, previous_week_day, next_week_day, dateFromDuration

"""
  Output of the parser is an array of tuples
  [match, value, (start, end)]
"""

class DateTimeParsingTestCases(TestCase):
  def test_captured_patterns(self):
    base_date = datetime.now()

    input_text = 'The event is on Monday 12 January 2012'
    parser = datetime_parsing(input_text)
    self.assertIn('Monday 12 January 2012', parser[0])
    self.assertEqual(parser[0][1], datetime(2012, 1, 12))
    self.assertEqual(len(parser), 1)

    input_text = 'This monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), this_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = 'Last monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), previous_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = 'Next monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), next_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = '25 minutes from now'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), dateFromDuration(base_date, 25, 'minutes', 'from now').strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = '10 days later'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), dateFromDuration(base_date, 10, 'days', 'later').strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = '2010'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%Y'), input_text)
    self.assertEqual(len(parser), 1)

    input_text = 'today'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'tomorrow'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() + timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'yesterday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'day before yesterday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=2)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'day before today'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'day before tomorrow'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=0)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = '2 days before'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=2)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'Monday and Friday'
    parser = datetime_parsing(input_text)
    self.assertIn('Monday', parser[0])
    self.assertIn('Friday', parser[1])
    self.assertEqual(parser[0][1].strftime('%d'), this_week_day(base_date, 0).strftime('%d'))
    self.assertEqual(parser[1][1].strftime('%d'), this_week_day(base_date, 4).strftime('%d'))
    self.assertEqual(len(parser), 2)

    input_text = 'First quarter of 2016'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-01-2016')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-03-2016')
    self.assertEqual(len(parser), 1)

    input_text = 'Last quarter of 2015'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-09-2015')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-12-2015')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on January 1st.'
    parser = datetime_parsing(input_text)
    self.assertIn('January 1st', parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '01-01-2016')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on January 1st 2014.'
    parser = datetime_parsing(input_text)
    self.assertIn('January 1st 2014', parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '01-01-2014')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on 2nd January 2014.'
    parser = datetime_parsing(input_text)
    self.assertIn('2nd January 2014', parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '02-01-2014')
    self.assertEqual(len(parser), 1)