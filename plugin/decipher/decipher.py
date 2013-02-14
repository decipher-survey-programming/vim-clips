"""
Utility module for decipher_clips.vim
"""
import re


def element_factory(selection, elType='radio', comment='', attrs=None):
    """This function returns a v2 xml Element as a string

    Args:
        selection (list): Lines of text to be processed
    Kwargs:
        elType  (string): The name of the main xml element. i.e. radio
        comment (string): Text to be used as the comment
        attrs     (dict): Attributes to be added to the main xml element
    Returns:
        string. The formatted v2 xml Element
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

    label = re.sub(r'(\.$|[\(\)])', '', label)
    label = re.sub(r'[-\.]', '_', label)

    template = '\n'.join(("<%(elType)s label=\"%(label)s\">",
                          "  <title>",
                          "    %(title)s",
                          "  </title>",
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
    """This function returns a v2 xml Cell as a string

    Args:
        selection (list): Lines of text to be processed
        cellType  (string): The name of the v2 Cell. i.e. row/col
    Kwargs:
        prefix (string): Text to be prefixed to the cell's label i.e. r1/c1
    Returns:
        string. The formatted Decipher xml Cell
    """
    attrs = {} if attrs is None else attrs
    selection = [line.strip() for line in selection if line.strip()]
    label_rgx = re.compile("^([a-zA-Z0-9_]{1,6})\.\s{1,}")

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
        cells.append("""  <%(cellType)s label="%(label)s">%(cell)s</%(cellType)s>""" %
                     dict(cellType=cellType, label=label, cell=cell))

    attrs_str = " ".join('%s="%s"' % (k, v) for k, v in attrs.items())

    if attrs_str:
        for i, cell in enumerate(cells):
            cells[i] = cell.replace('">', '" ' + attrs_str + ">", 1)

    return cells


def exclusify(lines):
    """This function guesses and adds appropriate attributes for exclusive cells
    It only processes the last v2 Cell in a v2 Element

    Args:
        lines (list): Lines of text constituting a v2 Element
    Returns:
        string. v2 Element with possibly exclusified last Cell
    """
    rgx = re.compile("""(.*None of.*)|(.*Decline to answer.*)|(.*>None<.*)|(.*Don't know.*)|(.*Not sure.*)""", re.I)
    if rgx.match(lines[-3]):
        lines[-3] = lines[-3].replace('>', ' exclusive="1" randomize="0">', 1)
    return lines


def openify(lines):
    """This function guesses and adds appropriate attributes for open-end cells

    Args:
        lines (list): Lines of text constituting a v2 Element
    Returns:
        string. v2 Element with possibly openified last Cell
    """
    rgx = re.compile(r'.*Other.*\(?\s*Specify[\s:]*\)?.*', re.I)
    for i, line in enumerate(lines):
        if rgx.match(line):
            line = re.sub('_{2,}', '', line)
            lines[i] = line.replace('>', ' open="1" openSize="25" randomize="0">', 1)
    return lines


def get_visual_selection(lines, start, end):
    r"""This function takes a list of lines and two coordinates
     ``e.g. (1,0) denoting first line, first char``. 
     It then collapses the lines into a \n joined string and splits
     into before, inside, and after the coordinates' intersection.
     *Supports multiple lines*

    Args:
        lines (list): Lines of text to be processed
        start (tuple): Coordinates of the start of a selection 
        end (tuple): Coordinates of the end of a selection 
    Returns:
        tuple of strings. (before, inside, after)
    """
    before = lines[0][:start[1]]
    after = lines[-1][end[1] + 1:]
    inside = '\n'.join(lines)[len(before):(-len(after)) or None]
    return (before, inside, after)
