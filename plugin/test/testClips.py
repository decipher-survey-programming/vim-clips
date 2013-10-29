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
                  CleanNotes,
                  CommentBlocks)


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
                            '    extraVariables="source,list,url,record,ipAddress,userAgent,decLang"',
                            '    compat="115"',
                            '    state="testing"',
                            '    newVirtual="1"',
                            '    setup="time,quota,term,decLang"',
                            '    ss:disableBackButton="1"',
                            '    unmacro="0"',
                            '    displayOnError="all"',
                            '    unique="">',
                            '',
                            '',
                            '<samplesources default="1">',
                            '  <samplesource list="1" title="default">',
                            '    <exit cond="qualified"><b>Thanks again for completing the survey!'
                            '<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>',
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
                           '  <title>What would you like to eat?</title>',
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
                           '  <title>What would you like to eat?</title>',
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
                        '  <title>What would you like to eat?</title>',
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
                           '  <title>How many of each would you like?</title>',
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
                           '  <title>How many of each would you like?</title>',
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
                           '  <title>Please explain your love for the following...</title>',
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
                           '  <title>Please explain your love for the following...</title>',
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
                           '  <title>What would you like to eat?</title>',
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
        linesExpected = ['  <row label="r1" cs:extra="Ham"     >Ham</row>',
                         '  <row label="foo" cs:extra="Spam"    >Spam</row>',
                         '  <row label="r3" cs:extra="bar Eggs">bar Eggs</row>',
                         '  <row label="r42" cs:extra="Bacon"   >Bacon</row>']

        self.assertEqual(linesMade, linesExpected)


    def test_MakeOrs(self):
        args = ('', 'Q1', '1-3,4,5-10', 'r', 'or')
        argsSpaced = ('', 'Q1', '1-3, 4  ,5-10', 'r', 'or')
        expected = ''.join(("Q1.r1 or Q1.r2 or Q1.r3 or Q1.r4 or Q1.r5 ",
                            "or Q1.r6 or Q1.r7 or Q1.r8 or Q1.r9 or Q1.r10"))
        self.assertEqual(MakeOrs(*args), expected)
        self.assertEqual(MakeOrs(*argsSpaced), expected)


        args = ('', 'Q2', 'A-C,K,W-DD', '', 'and')
        argsSpaced = ('', 'Q2', 'A-C , K ,   W-DD', '', 'and')
        expected = ''.join(("Q2.A and Q2.B and Q2.C and Q2.K and Q2.W and ",
                            "Q2.X and Q2.Y and Q2.Z and Q2.AA and Q2.BB and Q2.CC and Q2.DD"))
        self.assertEqual(MakeOrs(*args), expected)
        self.assertEqual(MakeOrs(*argsSpaced), expected)

        args = ('', 'Q3', 'A-C,3,W-DD', '', 'or')
        self.assertRaises(SyntaxError, MakeOrs, *args)

        args = ('', 'Q4', 'A--C', '', 'ham')
        self.assertRaises(SyntaxError, MakeOrs, *args)

        args = ('', 'Q5', '3-1', '', 'spam')
        self.assertRaises(ValueError, MakeOrs, *args)

        args = ('', 'Q6', 'C-A', '', 'eggs')
        self.assertRaises(ValueError, MakeOrs, *args)

        args = ('', 'Q7', 'CC-A', '', 'bacon')
        self.assertRaises(ValueError, MakeOrs, *args)


        condLine = 'cond="" rowCond="" colCond=""'

        args = (condLine, 'C1', '1-3', 'r', 'or')
        expectedLine = 'cond="C1.r1 or C1.r2 or C1.r3" rowCond="" colCond=""'
        self.assertEqual(MakeOrs(*args), expectedLine)

        args = (condLine, 'C1[row]', '1-3', 'c', 'or')
        expectedLine = 'cond="" rowCond="C1[row].c1 or C1[row].c2 or C1[row].c3" colCond=""'
        self.assertEqual(MakeOrs(*args), expectedLine)

        args = (condLine, 'C1[col]', '1-3', 'r', 'or')
        expectedLine = 'cond="" rowCond="" colCond="C1[col].r1 or C1[col].r2 or C1[col].r3"'
        self.assertEqual(MakeOrs(*args), expectedLine)


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
        rows = ['<row label="r1">Ham</row>',
                '<row label="r2">Spam</row>',
                '<row label="r3">Eggs</row>',
                '<row label="r4">Bacon</row>']

        cols = ['<col label="c1">Ham</col>',
                '<col label="c2">Spam</col>',
                '<col label="c3">Eggs</col>',
                '<col label="c4">Bacon</col>']

        self.assertEqual(Switcher(rows[:]), cols)
        self.assertEqual(Switcher(cols[:]), rows)


    def test_SwitchRating(self):
        byColsTag = '<radio label="Q1" averages="cols" values="order" adim="rows" type="rating">'
        byRowsTag = '<radio label="Q1" averages="rows" values="order" adim="cols" type="rating">'
        self.assertEquals(SwitchRating(byColsTag[:]), byRowsTag)
        self.assertEquals(SwitchRating(byRowsTag[:]), byColsTag)


    def test_AddGroups(self):
        rows = ['<row label="r1">Ham</row>',
                '<row label="r2">Spam</row>',
                '<row label="r3">Eggs</row>',
                '<row label="r4">Bacon</row>']

        rowsWithGroups = ['<row label="r1" groups="g1">Ham</row>',
                          '<row label="r2" groups="g1">Spam</row>',
                          '<row label="r3" groups="g1">Eggs</row>',
                          '<row label="r4" groups="g1">Bacon</row>']
        self.assertEqual(AddGroups(rows), rowsWithGroups)


    def test_CommentQuestion(self):
        text = 'Select all the Spam'
        commentedText = ['  <comment>{text}</comment>'.format(text=text)]

        self.assertEqual(CommentQuestion([text]), commentedText)


    def test_HTMLComment(self):
        self.assertEqual(HTMLComment(self.cells), ['<!--'] + self.cells + ['-->'])


    def test_AddAlts(self):
        element = ['<radio label="Q1" averages="cols" values="order" adim="rows" type="rating">',
                   '  <title>What would you like to eat?</title>',
                   '  <comment>Please select one</comment>',
                   '  <row label="r1">Ham</row>',
                   '  <row label="foo">Spam</row>',
                   '  <row label="r3">bar Eggs</row>',
                   '  <row label="r42">Bacon</row>',
                   '</radio>',
                   '<suspend/>']

        elementExpected = ['<radio label="Q1" averages="cols" values="order" adim="rows" type="rating">',
                           '  <title>What would you like to eat?</title>',
                           '  <alt>What would you like to eat?</alt>',
                           '  <comment>Please select one</comment>',
                           '  <row label="r1"><alt>Ham</alt>Ham</row>',
                           '  <row label="foo"><alt>Spam</alt>Spam</row>',
                           '  <row label="r3"><alt>bar Eggs</alt>bar Eggs</row>',
                           '  <row label="r42"><alt>Bacon</alt>Bacon</row>',
                           '</radio>',
                           '<suspend/>']
        
        self.assertEquals(AddAlts(element), elementExpected)


    def test_Strip(self):
        groups = ['  <group label="g1">Ham</group>',
                  '  <group label="foo">Spam</group>',
                  '  <group label="g3">bar Eggs</group>',
                  '  <group label="g42">Bacon</group>']

        rows = ['  <row label="r1">Ham</row>',
                '  <row label="foo">Spam</row>',
                '  <row label="r3">bar Eggs</row>',
                '  <row label="r42">Bacon</row>']

        cols = ['  <col label="c1">Ham</col>',
                '  <col label="foo">Spam</col>',
                '  <col label="c3">bar Eggs</col>',
                '  <col label="c42">Bacon</col>']


        choices = ['  <choice label="ch1">Ham</choice>',
                   '  <choice label="foo">Spam</choice>',
                   '  <choice label="ch3">bar Eggs</choice>',
                   '  <choice label="ch42">Bacon</choice>']

        linesExpected = ['Ham', 'Spam', 'bar Eggs', 'Bacon']

        for cells in (groups, rows, cols, choices):
            self.assertEqual(Strip(cells), linesExpected)


    def test_Justify(self):
        someText = '    Well, there\'s egg and bacon; egg sausage and bacon; egg and spam;' \
                   ' egg bacon and spam; egg bacon     sausage and spam; spam bacon sausage' \
                   ' and spam; spam egg spam spam bacon    and spam; spam sausage spam spam' \
                   ' bacon             spam            tomato            and           spam'

        justifiedText = ['    Well, there\'s egg and bacon; egg sausage and bacon; egg and spam; egg bacon and spam; egg bacon sausage',
                         '    and spam; spam bacon sausage and spam; spam egg spam spam bacon and spam; spam sausage spam spam bacon',
                         '    spam tomato and spam']

        self.assertEqual(Justify(someText), justifiedText)


    def test_CleanNotes(self):
        notes = ['<!-- XXX [Q1]: Not enough Spam -->',
                 '<!-- XXX [Q2]: Bacon doesn\'t have Spam on it -->',
                 '<!-- XXX [Q3]: Spam, then Eggs, then Spam -->']

        notesExpected =  ['[Q1]: Not enough Spam',
                          '[Q2]: Bacon doesn\'t have Spam on it',
                          '[Q3]: Spam, then Eggs, then Spam']

        self.assertEqual(CleanNotes(notes), notesExpected)


    def test_CommentBlocks(self):
        elementExpected = ['<survey>',
                           '<block label="spam_block" randomizeChildren="0" cond="1">',
                           '<radio label="Q1">',
                           '  <title>What would you like to eat?</title>',
                           '  <comment>Please select one</comment>',
                           '  <row label="r1">Ham</row>',
                           '  <row label="foo">Spam</row>',
                           '  <row label="r3">bar Eggs</row>',
                           '  <row label="r42">Bacon</row>',
                           '</radio>',
                           '<suspend/>',
                           '</block>',
                           '<!-- EO spam_block -->',
                           '</survey>']

        elementSent = ['<survey>',
                       '<block label="spam_block" randomizeChildren="0" cond="1">',
                       '<radio label="Q1">',
                       '  <title>What would you like to eat?</title>',
                       '  <comment>Please select one</comment>',
                       '  <row label="r1">Ham</row>',
                       '  <row label="foo">Spam</row>',
                       '  <row label="r3">bar Eggs</row>',
                       '  <row label="r42">Bacon</row>',
                       '</radio>',
                       '<suspend/>',
                       '</block>',
                       '</survey>']

        self.assertEqual(CommentBlocks(elementSent), elementExpected)
        self.assertEqual(CommentBlocks(elementExpected), elementExpected)
