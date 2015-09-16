import unittest
from lxml import etree
import sys
import re

sys.path.append('plugin/deciphervimclips')

# noinspection PyUnresolvedReferences
from deciphervimclips import deciphervimclips


def clean_xml(text):
    return re.sub(r'>[\s\n]+<', '><', text, re.DOTALL)  # lxml doesn't clean the string?


ELEMENT_TEMPLATE = (
    '<{type} label="{label}"{extra}>'
    '  <title>{title}</title>'
    '  <comment>{comment}</comment>'
    '  {content}'
    '</{type}>'
    '<suspend/>'
)


class TestElementFactory(unittest.TestCase):

    def create_mock(self, *args):
        """Interpolate the `ELEMENT_TEMPLATE` with mock values to compare with factory results

        :param args:
        :return: :rtype:
        """
        label, title = args[0][0].split(' ', 1)

        content = '\n'.join(args[0][1:]) if args[0][1:] else ''

        if args[3]:  # add xml attrs if they exist
            attrs_str = ' ' + ' '.join('{0}="{1}"'.format(k, v) for k, v in args[3].items())
        else:
            attrs_str = ''

        return ELEMENT_TEMPLATE.format(type=args[1],
                                       label=label,
                                       extra=attrs_str,
                                       title=title,
                                       comment=args[2],
                                       content=content)

    def test_element_factory(self):

        test_elements = (
            (['Q1 SPAM'], 'radio', 'comment', {}),
            (['Q2 SPAM'], 'checkbox', '', {}),
            (['Q3 SPAM'], 'select', '', dict(optional='0')),
            (['Q1 HAM'], 'checkbox', 'SPAM', {'EGGS': 'MORNING!'}),
            (['Q2 EGG'], 'BACON', 'SPAM', dict(a=1, b=2, c=3)),
            (['Q3 Anything without spam?', '<row label="r1">Spam</row>'], 'spam', '', dict(a=1, b=2, c=3)),
        )

        for args in test_elements:
            mock_element_str = clean_xml(self.create_mock(*args))
            mock_element_xml = etree.fromstring('<root>{0}</root>'.format(mock_element_str))
            generated_element_str = clean_xml(''.join(deciphervimclips.element_factory(*args)))
            generated_element_xml = etree.fromstring('<root>{0}</root>'.format(generated_element_str))
            self.assertEqual(*map(etree.tostring, (mock_element_xml, generated_element_xml)))

        badElements = (
            (['SPAM'], 'radio', 'EGGS', {}),  # No label
        )

        for args in badElements:
            self.assertRaises(Exception, deciphervimclips.element_factory, args)


class TestCellFactory(unittest.TestCase):

    def test_cell_factory(self):
        template = '  <{0} label="{1}"{2}>{3}</{0}>'

        def create_mock(*args):
            if args[3]:
                attrs_str = ' ' + ' '.join('{0}="{1}"'.format(k, v) for k, v in args[3].items())
            else:
                attrs_str = ''

            rows = []
            for i, line in enumerate(args[0]):
                rows.append(template.format(args[1], args[2] + str(i + 1), attrs_str, line))
            return ' '.join(rows)

        test_cells = (
            (['SPAM BACON EGGS'], 'row', 'r', {}),
            (['SPAM', 'BACON', 'EGGS'], 'row', 'r', {}),
        )

        for args in test_cells:
            mock_xml = etree.fromstring('<root>{0}</root>'.format(create_mock(*args)))
            generated_xml = etree.fromstring('<root>{0}</root>'.format(''.join(deciphervimclips.cell_factory(*args))))
            mock_xml, generated_xml = map(etree.tostring, (mock_xml, generated_xml))
            mock_xml, generated_xml = map(clean_xml, (mock_xml, generated_xml))
            self.assertEqual(mock_xml, generated_xml)

    def test_label_rgx(self):
        test_titles = (
            'Q1. SPAM',
            'Q2: EGGS',
            '(Q3) HAM',
            'Q3.1 BACON',
            'Q4. Q4. Q4.'
        )

        generated_elements = []
        for title in test_titles:
            generated_elements.append(''.join(deciphervimclips.element_factory([title], 'radio', '', {})))

        expected_titles = (
            ('Q1', 'SPAM'),
            ('Q2', 'EGGS'),
            ('Q3', 'HAM'),
            ('Q3_1', 'BACON'),
            ('Q4', 'Q4. Q4.')
        )

        mock_xml_strs = []
        for label, title in expected_titles:
            mock_xml_strs.append(
                ELEMENT_TEMPLATE.format(type='radio', label=label, extra='', title=title, comment='', content='')
            )

        for generated_xml_str, mock_xml_str in zip(generated_elements, mock_xml_strs):
            self.assertEqual(clean_xml(generated_xml_str), clean_xml(mock_xml_str))

    def test_clean_attribute_spacing(self):
        unjustified_cells = [
            '  <row label="ham">HAM</row>',
            '  <row label="spam">SPAM</row>',
            '  <row label="r3">BACON</row>'
        ]

        justified_cells = [
            '  <row label="ham" >HAM</row>',
            '  <row label="spam">SPAM</row>',
            '  <row label="r3"  >BACON</row>'
        ]

        self.assertEqual(deciphervimclips.clean_attribute_spacing(unjustified_cells), justified_cells)

        unjustified_cells = [
            '  <row label="ham" cs:extra="HAM"  >HAM</row>',
            '  <row label="spam" cs:extra="SPAM" >SPAM</row>',
            '  <row label="r3" cs:extra="BACON" exclusive="1" randomize="0">BACON</row>'
        ]

        justified_cells = [
            '  <row label="ham"  cs:extra="HAM"  >HAM</row>',
            '  <row label="spam" cs:extra="SPAM" >SPAM</row>',
            '  <row label="r3"   cs:extra="BACON" exclusive="1" randomize="0">BACON</row>'
        ]

        self.assertEqual(deciphervimclips.clean_attribute_spacing(unjustified_cells), justified_cells)
