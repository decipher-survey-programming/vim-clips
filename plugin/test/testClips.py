# -*- coding: utf-8 -*-
from twisted.trial import unittest
from util import (NewSurvey,
                  CleanUp,
                  Rows,
                  Cols,
                  Choice,
                  Rates,
                  Case,
                  NoAnswer,
                  Resource,
                  MakeRadio,
                  MakeCheckbox,
                  MakeSelect,
                  MakeNumber,
                  MakeFloat,
                  MakeText,
                  MakeTextarea,
                  MakeHTML,
                  MakeRating,
                  MakeNets,
                  MakeGroups,
                  MakeExtras,
                  MakeOrs,
                  AddValuesLow,
                  AddValuesHigh,
                  Switcher,
                  SwitchRating,
                  AddGroups,
                  CommentQuestion,
                  HTMLComment,
                  AddAlts,
                  Strip,
                  Justify,
                  CleanNotes)


class TestClipFunctions(unittest.TestCase):
    """Tests all major functions in decipher_clips.vim"""

    def setUp(self):
        self.cells = ['Ham', 'foo. Spam', 'bar Eggs', '42. Bacon']
        self.cellsRatable = ['1. Spammy',
                             '2.',
                             '3.',
                             '4.',
                             '5. Very Spammy']

    def test_NewSurvey(self):
        xmlLines = NewSurvey(['<res label="dinner">SPAM HAM EGGS</res>'])

        xmlLinesExpected = ['<?xml version="1.0" encoding="UTF-8"?>',
                            '<survey name="Survey"',
                            '    alt=""',
                            '    autosave="0"',
                            '    extraVariables="source,list,url,record,ipAddress,userAgent"',
                            '    compat="113"',
                            '    state="testing"',
                            '    newVirtual="1"',
                            '    setup="time,quota,term"',
                            '    ss:disableBackButton="1"',
                            '    unmacro="0"',
                            '    displayOnError="all"',
                            '    unique="">',
                            '',
                            '',
                            '<samplesources default="1">',
                            '  <samplesource list="1" title="default">',
                            '    <exit cond="qualified"><b>Thanks again for completing the survey!<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>',
                            '    <exit cond="terminated"><b>Thank you for your selection!</b></exit>',
                            '    <exit cond="overquota"><b>Thank you for your selection!</b></exit>',
                            '  </samplesource>',
                            '</samplesources>',
                            '',
                            '',
                            '<res label="dinner">SPAM HAM EGGS</res>',
                            '',
                            '<marker name="qualified"/>',
                            '',
                            '</survey>']

        self.assertEqual(xmlLines, xmlLinesExpected)


    def test_CleanUp(self):
        linesCleaned = CleanUp(['‘“HAM”–“SPAM”&“EGGS”’…'])
        linesExpected = ['\'"HAM"-"SPAM"&amp;"EGGS"\'...']

        self.assertEqual(linesCleaned, linesExpected)


    def test_Rows(self):
        rowsMade = Rows(self.cells)
        rowsExpected = ['  <row label="r1">Ham</row>',
                        '  <row label="foo">Spam</row>',
                        '  <row label="r3">bar Eggs</row>',
                        '  <row label="r42">Bacon</row>',
                        '\n']

        self.assertEqual(rowsMade, rowsExpected)


    def test_Cols(self):
        colsMade = Cols(self.cells)
        colsExpected = ['  <col label="c1">Ham</col>',
                        '  <col label="foo">Spam</col>',
                        '  <col label="c3">bar Eggs</col>',
                        '  <col label="c42">Bacon</col>',
                        '\n']

        self.assertEqual(colsMade, colsExpected)


    def test_Choice(self):
        choicesMade = Choice(self.cells)
        choicesExpected = ['  <choice label="ch1">Ham</choice>',
                           '  <choice label="foo">Spam</choice>',
                           '  <choice label="ch3">bar Eggs</choice>',
                           '  <choice label="ch42">Bacon</choice>',
                           '\n']

        self.assertEqual(choicesMade, choicesExpected)


    def test_Rates(self):
        cellsMade = Rates(self.cellsRatable)
        cellsExpected = ['  <col label="c1">Spammy<br/>1</col>',
                         '  <col label="c2">2</col>',
                         '  <col label="c3">3</col>',
                         '  <col label="c4">4</col>',
                         '  <col label="c5">Very Spammy<br/>5</col>']

        self.assertEqual(cellsMade, cellsExpected)


    def test_Case(self):
        cellsMade = Case(self.cells)
        cellsExpected = ['<pipe label="" capture="">',
                        '  <case label="c1" cond="">Ham</case>',
                        '  <case label="foo" cond="">Spam</case>',
                        '  <case label="c3" cond="">bar Eggs</case>',
                        '  <case label="c42" cond="">Bacon</case>',
                        '  <case label="c99" cond="1">BAD PIPE</case>',
                        '</pipe>']

        self.assertEqual(cellsMade, cellsExpected)


    def test_NoAnswer(self):
        cellsMade = NoAnswer(self.cells)
        cellsExpected = ['  <noanswer label="r1">Ham</noanswer>',
                         '  <noanswer label="foo">Spam</noanswer>',
                         '  <noanswer label="r3">bar Eggs</noanswer>',
                         '  <noanswer label="r42">Bacon</noanswer>']

        self.assertEqual(cellsMade, cellsExpected)


    def test_Resource(self):
        cellsMade = Resource(self.cells)
        cellsExpected = ['<res label="">Ham</res>',
                         '<res label="foo">Spam</res>',
                         '<res label="">bar Eggs</res>',
                         '<res label="42">Bacon</res>']

        self.assertEqual(cellsMade, cellsExpected)


    def test_MakeRadio(self):
        vbuffer = ['Q1. What would you like to eat?']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeRadio(vbuffer)

        elementExpected = ['<radio label="Q1">',
                           '  <title>',
                           '    What would you like to eat?',
                           '  </title>',
                           '  <comment>Please select one</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</radio>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeCheckbox(self):
        vbuffer = ['Q1. What would you like to eat?']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeCheckbox(vbuffer)

        elementExpected = ['<checkbox label="Q1" atleast="1">',
                           '  <title>',
                           '    What would you like to eat?',
                           '  </title>',
                           '  <comment>Please select all that apply</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</checkbox>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeSelect(self):
        vbuffer = ['Q1. What would you like to eat?']
        rows = ['Course 1', 'Course 2', 'Course 3']
        vbuffer.extend(Rows(rows))
        vbuffer.extend(Choice(self.cells))

        elementMade = MakeSelect(vbuffer)

        elementExpected = ['<select label="Q1" optional="0">',
                        '  <title>',
                        '    What would you like to eat?',
                        '  </title>',
                        '  <comment>Please select one for each selection</comment>',
                        '  <row label="r1">Course 1</row>',
                        '  <row label="r2">Course 2</row>',
                        '  <row label="r3">Course 3</row>',
                        '  <choice label="ch1">Ham</choice>',
                        '  <choice label="foo">Spam</choice>',
                        '  <choice label="ch3">bar Eggs</choice>',
                        '  <choice label="ch42">Bacon</choice>',
                        '</select>',
                        '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeNumber(self):
        vbuffer = ['Q1. How many of each would you like?']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeNumber(vbuffer)

        elementExpected = ['<number label="Q1" optional="0" size="3">',
                           '  <title>',
                           '    How many of each would you like?',
                           '  </title>',
                           '  <comment>Please enter a whole number</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</number>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeFloat(self):
        vbuffer = ['Q1. How many of each would you like?']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeFloat(vbuffer)

        elementExpected = ['<float label="Q1" optional="0" size="3">',
                           '  <title>',
                           '    How many of each would you like?',
                           '  </title>',
                           '  <comment>Please enter a number</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</float>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeText(self):

        vbuffer = ['A. Please explain your love for the following...']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeText(vbuffer)

        elementExpected = ['<text label="A" optional="0">',
                           '  <title>',
                           '    Please explain your love for the following...',
                           '  </title>',
                           '  <comment>Please be as specific as possible</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</text>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeTextarea(self):
        vbuffer = ['A. Please explain your love for the following...']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeTextarea(vbuffer)

        elementExpected = ['<textarea label="A" optional="0">',
                           '  <title>',
                           '    Please explain your love for the following...',
                           '  </title>',
                           '  <comment>Please be as specific as possible</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</textarea>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeHTML(self):
        text = ["Spam spam spam spam. Lovely spam! Wonderful spam! Spam spa-a-a-a-a-am spam spa-a-a-a-a-am spam.",
                "Lovely spam! Lovely spam! Lovely spam! Lovely spam! Lovely spam! Spam spam spam spam!"]

        linesExpected = ['<html label="" where="survey">',
                        '  <p>',
                        '    Spam spam spam spam. Lovely spam! Wonderful spam! Spam spa-a-a-a-a-am spam spa-a-a-a-a-am spam.',
                        '    Lovely spam! Lovely spam! Lovely spam! Lovely spam! Lovely spam! Spam spam spam spam!',
                        '  </p>',
                        '</html>']

        linesMade = MakeHTML(text)

        self.assertEqual(linesMade, linesExpected)


    def test_MakeRating(self):
        vbuffer = ['Q1. What would you like to eat?']
        vbuffer.extend(Rows(self.cells))
        elementMade = MakeRating(vbuffer)

        elementExpected = ['<radio label="Q1" averages="cols" values="order" adim="rows" type="rating">',
                           '  <title>',
                           '    What would you like to eat?',
                           '  </title>',
                           '  <comment>Please select one</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</radio>',
                           '<suspend/>']

        self.assertEqual(elementMade, elementExpected)


    def test_MakeNets(self):
        linesMade = MakeNets(self.cells)
        linesExpected = ['  <net labels="">Ham</net>',
                         '  <net labels="">foo. Spam</net>',
                         '  <net labels="">bar Eggs</net>',
                         '  <net labels="">42. Bacon</net>']

        self.assertEqual(linesMade, linesExpected)


    def test_MakeGroups(self):
        linesMade = MakeGroups(self.cells)
        linesExpected = ['  <group label="g1">Ham</group>',
                         '  <group label="foo">Spam</group>',
                         '  <group label="g3">bar Eggs</group>',
                         '  <group label="g42">Bacon</group>']

        self.assertEqual(linesMade, linesExpected)
 

    def test_MakeExtras(self):
        linesMade = MakeExtras(Rows(self.cells))
        linesExpected = ['  <row label="r1"  cs:extra="Ham"     >Ham</row>',
                         '  <row label="foo" cs:extra="Spam"    >Spam</row>',
                         '  <row label="r3"  cs:extra="bar Eggs">bar Eggs</row>',
                         '  <row label="r42" cs:extra="Bacon"   >Bacon</row>']

        self.assertEqual(linesMade, linesExpected)


    def test_MakeOrs(self):
        pass

    def test_AddValuesLow(self):
        rowsMade = AddValuesLow(Rows(self.cells))

        rowsExpected = ['  <row label="r1" value="1">Ham</row>',
                        '  <row label="foo" value="2">Spam</row>',
                        '  <row label="r3" value="3">bar Eggs</row>',
                        '  <row label="r42" value="4">Bacon</row>',
                        '\n']

        self.assertEqual(rowsMade, rowsExpected)


    def test_AddValuesHigh(self):
        rowsMade = AddValuesHigh(Rows(self.cells))

        rowsExpected = ['  <row label="r1" value="4">Ham</row>',
                        '  <row label="foo" value="3">Spam</row>',
                        '  <row label="r3" value="2">bar Eggs</row>',
                        '  <row label="r42" value="1">Bacon</row>',
                        '\n']

        self.assertEqual(rowsMade, rowsExpected)


    def test_Switcher(self):
        pass

    def test_SwitchRating(self):
        pass

    def test_AddGroups(self):
        pass

    def test_CommentQuestion(self):
        pass

    def test_HTMLComment(self):
        pass

    def test_AddAlts(self):
        pass

    def test_Strip(self):
        pass

    def test_Justify(self):
        pass

    def test_CleanNotes(self):
        pass
