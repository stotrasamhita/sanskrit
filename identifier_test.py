#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Data structures that store matching metres for known patterns."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

# TODO(shreevatsa): Change this back
# import match_result
import metrical_data as match_result

# TODO(shreevatsa): Change this back
# import identifier
import sscan as identifier


class BadInput(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(BadInput, self).__init__(*args, **kwargs)
    self.identifier = identifier.Identifier()

  def testEmpty(self):
    """Identifier should fail with empty input."""
    # self.assertRaises(identifier.EmptyInputError,
    #                   self.identifier.IdentifyFromLines, [])
    self.assertIsNone(self.identifier.IdentifyFromLines([]))

  def testNoSyllables(self):
    """Identifier should return no result, for input containing no syllabes."""
    self.assertIsNone(self.identifier.IdentifyFromLines(['t', 't', 't', 't']))


class KnownValues(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(KnownValues, self).__init__(*args, **kwargs)
    self.identifier = identifier.Identifier()

  def AssertSingleMatchResultEquals(self, results, metre_name, match_type,
                                    issues):
    try:
      assert isinstance(results, list)
      assert len(results) == 1
      result = results[0]
      assert result.metre_name == metre_name
      assert result.match_type == match_type
      assert set(result.issues) == set(issues)
    except AssertionError:
      print('\n\nMismatch: Got results')
      print(match_result.Description(results))
      print('instead of')
      print('\tMetre name: %s' % metre_name)
      print('\tMatch type: %s' % match_type)
      print('\tIssues: %s' % issues)
      raise self.failureException

  def testFineAnustubh(self):
    """Good anuṣṭubh should be recognized."""
    verse = ['agajānana padmārkaṃ',
             'gajānanam aharniṣam',
             'anekadantam bhaktānām',
             'ekadantam upāsmahe']
    self.AssertSingleMatchResultEquals(self.identifier.IdentifyFromLines(verse),
                                       'Anuṣṭup (Śloka)',
                                       match_result.MATCH_TYPE.FULL,
                                       [])

  def testFirstOffAnustubh(self):
    """Anuṣṭubh with first pāda wrong should be recognized."""
    verse = ['तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।',
             'नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ।। 1.1.1 ।।']
    self.AssertSingleMatchResultEquals(
        self.identifier.IdentifyFromLines(verse),
        'Anuṣṭup (Śloka)',
        match_result.MATCH_TYPE.FULL,
        [match_result.ISSUES.FIRST_PADA_OFF,
         match_result.ISSUES.VISAMA_PADANTA_LAGHU])

  def testFineMandakranta(self):
    """A valid example of Mandākrāntā should be recognized."""
    verse = ['kazcit kAntAvirahaguruNA svAdhikArAt pramattaH $',
             'zApenAstaMgamitamahimA varSabhogyeNa bhartuH &',
             'yakSaz cakre janakatanayAsnAnapuNyodakeSu %',
             'snigdhacchAyAtaruSu vasatiM rAmagiryAzrameSu // 1.1 //']
    self.AssertSingleMatchResultEquals(
        self.identifier.IdentifyFromLines(verse),
        'Mandākrāntā',
        match_result.MATCH_TYPE.FULL,
        [])

  def testMandakrantaWithVpl(self):
    """Mandākrāntā with viṣama-pādānta-laghu."""
    verse = ['tvayy AdAtuM jalam avanate zArGgiNo varNacaure $',
             'tasyAH sindhoH pRthum api tanuM dUrabhAvAt pravAham &',
             'prekSiSyante gaganagatayo nUnam Avarjya dRSTir %',
             'ekaM bhuktAguNam iva bhuvaH sthUlamadhyendranIlam // 1.49 //']
    self.AssertSingleMatchResultEquals(
        self.identifier.IdentifyFromLines(verse),
        'Mandākrāntā',
        match_result.MATCH_TYPE.FULL,
        [match_result.ISSUES.VISAMA_PADANTA_LAGHU])

  def testArya(self):
    """Test some examples of Arya."""
    pass

  def testBreakUp(self):
    """Test all the above by inserting random breaks in the list."""
    pass


if __name__ == '__main__':
  unittest.main()
