"""
Utility module for decipher_clips.vim
"""
import re


def element_factory(selection, elType='radio', comment='', attrs=None):
    """Return an xml v2-Element as a list of strings

    Args:
        selection (list): Lines of text to be processed
    Kwargs:
        elType  (string): The name of the main xml element. e.g. `radio`
        comment (string): Text to be used in the comment cell
        attrs     (dict): Attributes to be added to the main xml element
    Return:
        list. List of strings making up the formatted v2-Element
    """
    attrs = {} if attrs is None else attrs
    selection = [line.rstrip() for line in selection if line.strip()]
    firstLine = selection.pop(0).strip()
    selection = '\n'.join(selection) if selection else ''

    try:
        label, title = firstLine.split(' ', 1)
    except ValueError:
        raise Exception("Question should be in format: Q1 Title")

    if label[0].isdigit():
        label = 'Q' + label

    # remove possible label delimiters
    label = re.sub(r'(\.$|[\(\):])', '', label)

    # dashes and periods become underscores
    label = re.sub(r'[-\.]', '_', label)

    template = '\n'.join(("<%(elType)s label=\"%(label)s\">",
                          "  <title>%(title)s</title>",
                          "%(selection)s",
                          "</%(elType)s>",
                          "<suspend/>"))

    if selection.find("<comment") == -1:
        selection = "  <comment>%s</comment>\n" % comment + selection

    element = (template % (dict(elType=elType,
                                label=label,
                                title=title,
                                selection=selection))).split("\n")

    attrs_str = " ".join('%s="%s"' % (k, v) for k, v in attrs.items())

    if attrs_str:
        element[0] = element[0].replace('">', '" ' + attrs_str + ">", 1)

    return element


def cell_factory(selection, cellType, prefix='', attrs=None):
    """Return a series of xml v2-Cells as a list of strings

    Args:
        selection (list): Lines of text to be processed
        cellType  (string): The name of the v2-Cell. e.g. `row/col`
    Kwargs:
        prefix (string): Text to be prefixed to the
        v2-Cell's label e.g. `r1/c1`
    Return:
        list. List of strings making up the formatted v2-Cells
    """
    cellTemplate = ('  <%(cellType)s label="%(label)s">'
                    '%(cell)s'
                    '</%(cellType)s>')

    attrs = {} if attrs is None else attrs
    selection = [line.strip() for line in selection if line.strip()]
    label_rgx = re.compile("^\[?([a-zA-Z0-9_]{1,6})\]?\.\s{1,}")

    cells = []
    for i, cell in enumerate(selection):
        label = label_rgx.search(cell)
        if label:
            label = label.groups()[0]
            cell = label_rgx.sub('', cell)
            if label[0].isdigit():
                label = prefix + label
        else:
            label = prefix + str(i + 1)
        cells.append(cellTemplate %
                     dict(cellType=cellType, label=label, cell=cell))

    attrs_str = " ".join('%s="%s"' % (k, v) for k, v in attrs.items())

    if attrs_str:
        for i, cell in enumerate(cells):
            cells[i] = cell.replace('">', '" ' + attrs_str + ">", 1)

    return cells


def exclusify(lines):
    """Add exclusive attributes to applicable v2-Cells
    Only processes the last v2-Cell (third to last line)

    Args:
        lines (list): Lines of text constituting a v2-Element
    Return:
        list. List of strings making up the formatted v2-Element
    """
    exclusiveTxts = ('None of.*',
                     'Decline to answer',
                     'None',
                     'Don\'t know',
                     'Not sure')

    rgxString = '|'.join('(>{0}<)'.format(text) for text in exclusiveTxts)
    rgx = re.compile(rgxString, re.I)

    if rgx.search(lines[-3]):
        lines[-3] = lines[-3].replace('>', ' exclusive="1" randomize="0">', 1)

    return lines


def openify(lines):
    """Add open-end attributes to applicable v2-Cells

    Args:
        lines (list): Lines of text constituting a v2-Element
    Return:
        list. List of strings making up the formatted v2-Element
    """
    openAttrs = ' open="1" openSize="25" randomize="0">'

    rgx = re.compile(r'.*Other.*\(?\s*Specify[\s:]*\)?.*', re.I)

    for i, line in enumerate(lines):
        if rgx.match(line):

            # remove place holder underscores
            line = re.sub('_{2,}', '', line)

            lines[i] = line.replace('>', openAttrs, 1)

    return lines


def get_visual_selection(lines, start, end):
    """Split an arbitrary selection of text between lines

    Args:
        lines  (list): Lines of text to be processed
        start (tuple): Coordinates of the start of a selection
                       in format (line, char)
        end   (tuple): Coordinates of the end of a selection
                       in format (line, char)
    Return:
        tuple of strings. (before, inside, after)
    """
    before = lines[0][:start[1]]
    after = lines[-1][end[1] + 1:]
    inside = '\n'.join(lines)[len(before):(-len(after)) or None]
    return (before, inside, after)


def clean_attribute_spacing(lines):
    """Justify the spacing of attributes accross multiple xml elements

    This is accomplished by adding spaces to the attributes smaller
    than the largest of its type.

    Args:
        lines (string): Lines of xml to process
    Return:
        list. Lines of text/xml with justified attributes
    """
    lines = [re.sub(r'\s+>', '>', line) for line in lines if line.strip()]

    if not lines:
        return []

    margin = (len(lines[0]) - len(lines[0].lstrip())) * ' '

    lines = [re.sub('\s{2,}', ' ', line) for line in lines]

    attributes_rgx = re.compile(r'([\w:]+)="([^"]+)"')

    attrDict = {}
    for line in lines:
        attrs = attributes_rgx.findall(line)
        if attrs:
            for name, value in attrs:
                largestValue = attrDict.setdefault(name, len(value))
                if len(value) > largestValue:
                    attrDict[name] = len(value)

    xmlOut = []
    for line in lines:
        attrs = attributes_rgx.findall(line)
        for name, value in attrs:
            maxValueLen = attrDict[name]
            if len(value) < maxValueLen:
                attr = '{0}="{1}"'.format(name, value)
                padding = (maxValueLen - len(value)) * ' '
                line = line.replace(attr, attr + padding)
        xmlOut.append(margin + line.lstrip())

    return xmlOut
