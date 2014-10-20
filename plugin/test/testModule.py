from twisted.trial import unittest
from lxml import etree
import sys
import re

sys.path.append('../decipherclips')

import decipherclips


def clean_xml(text):
    return re.sub(r'>[\s\n]+<', '><', text, re.DOTALL)  # lxml doesn't clean the string?


class TestFactories(unittest.TestCase):
    def setUp(self):
        self.elementTemplate = '\n'.join(('<{type} label="{label}"{extra}>',
                                          '  <title>{title}</title>',
                                          '  <comment>{comment}</comment>',
                                          '{content}',
                                          '</{type}>',
                                          '<suspend/>'))

    def testElementFactory(self):
        template = ('<{type} label="{label}"{extra}>'
                    '  <title>{title}</title>'
                    '  <comment>{comment}</comment>'
                    '  {content}'
                    '</{type}>'
                    '<suspend/>')

        def format_real(*args):
            label, title = args[0][0].split(' ', 1)  # Q1. Spamalot

            content = '\n'.join(args[0][1:]) if args[0][1:] else ''  # any extra lines in vbuffer?

            if args[3]:  # make xml attrs if they exist
                attrs_str = ' ' + ' '.join('%s="%s"' % (k, v) for k, v in args[3].items())
            else:
                attrs_str = ''

            return template.format(type=args[1],
                                   label=label,
                                   extra=attrs_str,
                                   title=title,
                                   comment=args[2],
                                   content=content)


        testElements = ((['Q1 SPAM'], 'radio', 'comment', {}),
                        (['Q2 SPAM'], 'checkbox', '', {}),
                        (['Q3 SPAM'], 'select', '', dict(optional='0')),
                        (['Q1 HAM'],  'checkbox', 'SPAM', {'EGGS': 'MORNING!'}),
                        (['Q2 EGG'],  'BACON', 'SPAM', dict(a=1, b=2, c=3)),
                        (['Q3 Anything without spam?', '<row label="r1">Spam</row>'],  'spam', '', dict(a=1, b=2, c=3)),
                        )

        for e in testElements:
            elTest = clean_xml(format_real(*e))
            xmlTest = etree.fromstring('<root>{0}</root>'.format(elTest))
            elReal = clean_xml(''.join(decipherclips.element_factory(*e)))
            xmlReal = etree.fromstring('<root>{0}</root>'.format(elReal))
            self.assertEqual(*map(etree.tostring, (xmlTest, xmlReal)))

        badElements = ((['SPAM'], 'radio', 'EGGS', {}),  # No label
                       )

        for e in badElements:
            self.assertRaises(Exception, decipherclips.element_factory, e)


    def testCellFactory(self):
        template = '  <{0} label="{1}"{2}>{3}</{0}>'

        def format_real(*args):
            if args[3]:
                attrs_str = ' ' + ' '.join('%s="%s"' % (k, v) for k, v in args[3].items())
            else:
                attrs_str = ''

            rows = []
            for i, line in enumerate(args[0]):
                rows.append(template.format(args[1], args[2] + str(i + 1), attrs_str, line))
            return ' '.join(rows)


        testCells = ((['SPAM BACON EGGS'], 'row', 'r', {}),
                     (['SPAM', 'BACON', 'EGGS'], 'row', 'r', {}),
                     )

        for e in testCells:
            elTest = format_real(*e)
            xmlTest = etree.fromstring('<root>{0}</root>'.format(elTest))
            elReal = ''.join(decipherclips.cell_factory(*e))
            xmlReal = etree.fromstring('<root>{0}</root>'.format(elReal))
            xmlTest, xmlReal = map(etree.tostring, (xmlTest, xmlReal))
            xmlTest, xmlReal = map(clean_xml, (xmlTest, xmlReal))
            self.assertEqual(xmlTest, xmlReal)

    def testCellFactoryLabelRgx(self):
        testTitles =   ('Q1. SPAM',
                        'Q2: EGGS',
                        '(Q3) HAM',
                        'Q3.1 BACON',
                        'Q4. Q4. Q4.')
        resultXMLs = []
        for title in testTitles:
            resultXMLs.append(decipherclips.element_factory([title], 'radio', '', {}))

        cleanedTitles =   (('Q1', 'SPAM'),
                           ('Q2', 'EGGS'),
                           ('Q3', 'HAM'),
                           ('Q3_1', 'BACON'),
                           ('Q4', 'Q4. Q4.'))

        expectedXMLs = []
        for label, title in cleanedTitles:
            formatDict = dict(type='radio', label=label, extra='', title=title, comment='', content='')
            expectedXMLs.append(self.elementTemplate.format(**formatDict).split('\n'))

        for madeXML, expectedXML in zip(resultXMLs, expectedXMLs):
            self.assertEqual(madeXML, expectedXML)


    def test_clean_attribute_spacing(self):
        inputCellsRegular =  ['  <row label="ham">HAM</row>',
                              '  <row label="spam">SPAM</row>',
                              '  <row label="r3">BACON</row>']

        expectedCellsRegular = ['  <row label="ham" >HAM</row>',
                                '  <row label="spam">SPAM</row>',
                                '  <row label="r3"  >BACON</row>']

        self.assertEqual(decipherclips.clean_attribute_spacing(inputCellsRegular), expectedCellsRegular)

        inputCellsExtra = ['  <row label="ham" cs:extra="HAM"  >HAM</row>',
                           '  <row label="spam" cs:extra="SPAM" >SPAM</row>',
                           '  <row label="r3" cs:extra="BACON" exclusive="1" randomize="0">BACON</row>']

        expectedCellsExtra = ['  <row label="ham"  cs:extra="HAM"  >HAM</row>',
                              '  <row label="spam" cs:extra="SPAM" >SPAM</row>',
                              '  <row label="r3"   cs:extra="BACON" exclusive="1" randomize="0">BACON</row>']

        self.assertEqual(decipherclips.clean_attribute_spacing(inputCellsExtra), expectedCellsExtra)
