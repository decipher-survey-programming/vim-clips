import vim
import re
import deciphervimclips
import sys

if sys.version_info[0] < 3:
    from urllib import quote
else:
    from urllib.parse import quote



def get_current_range():
    return vim.current.range[:]


def set_current_range(new_range):
    vim.current.range[:] = new_range

def position_cursor(start, end):
    # This acts a bit strange with the addition of newlines in elements
    return ( vim.current.range.start + start, end )


def NewSurvey():
    """
    Surround vbuffer in new-survey template with sane defaults
    """
    vbuffer = vim.current.buffer[:]
    COMPAT = 138

    header = [  '<?xml version="1.0" encoding="UTF-8"?>',
                '<survey alt=""',
                '    autosave="0"',
                '    browserDupes="safe"',
                '    compat="%d"' % COMPAT,
                '    displayOnError="all"',
                '    extraVariables="source,record,ipAddress,decLang,list,userAgent"',
                '    fir="on"',
                '    mobile="compat"',
                '    mobileDevices="smartphone,tablet,featurephone,desktop"',
                '    name="Survey"',
                '    setup="decLang,quota,term,time"',
                '    ss:disableBackButton="1"',
                '    ss:hideProgressBar="0"',
                '    ss:listDisplay="1"',
                '    ss:logoFile=""',
                '    ss:logoPosition="left"',
                '    unmacro="0"',
                '    unique=""',
                '    state="testing">',
                '',
                '<samplesources default="0">',
                '  <samplesource list="0" title="">',
                '    <completed>It seems you have already entered this survey.</completed>',
                '    <invalid>You are missing information in the URL. Please verify the URL with the original invite.</invalid>',
                '    <exit cond="qualified">Thank you for taking our survey. Your efforts are greatly appreciated!</exit>',
                '    <exit cond="terminated">Thank you for taking our survey.</exit>',
                '    <exit cond="overquota">Thank you for taking our survey.</exit>',
                '  </samplesource>',
                '</samplesources>',
                '']

    footer = '\n</survey>'.split('\n')

    vim.current.buffer[:] = header + vbuffer + footer


def CleanUp():
    """
    Replaces common utf chars with ascii
    also reduces and normalizes tabs and newlines
    """
    selection = '\n'.join(vim.current.range[:])

    selection = re.sub(r'\t+', ' ', selection)
    selection = re.sub(r'\n\s+\n', '\n\n', selection)
    selection = re.sub(r'\n{2,}', '\n\n', selection)
    selection = re.sub(r'\r', '', selection)

    transTable = {  '–': '-',
                    '”': '"',
                    '“': '"',
                    '‘': "'",
                    '’': "'",
                    '…': '...',
                    '&': '&amp;'}

    for k, v in transTable.items():
        selection = selection.replace(k, v)

    [line.lstrip() for line in selection.split('\n')]


def Rows():
    """
    Makes ``row`` Cells with vrange lines as text nodes

    .. code-block::xml

        1. Spam

        <row label="r1">Spam</row>
    """
    set_current_range( deciphervimclips.cell_factory( get_current_range(), "row", "r" ) + ['\n'] )


def Cols():
    """
    Makes ``col`` Cells with vrange lines as text nodes

    .. code-block::xml

        2. Ham

        <col label="c2">Ham</col>
    """
    set_current_range( deciphervimclips.cell_factory( get_current_range(), "col", "c" ) + ['\n'] )


def Choice():
    """
    Makes ``choice`` Cells with vrange lines as text nodes

    .. code-block::xml

        3. Eggs

        <choice label="ch3">Eggs</choice>
    """
    set_current_range( deciphervimclips.cell_factory( get_current_range(), "choice", "ch") + ['\n'] )


def Rates():
    """
    Makes ``col`` Cells with vrange lines as text nodes
    also, if the line leads with an integer it is placed at the
    end of a <br/>

    .. code-block::xml

        1. Very Spammy
        2.
        3. Not at all Spammy

        <col label="c1">Very Spammy<br/>1</col>
        <col label="c2">2</col>
        <col label="c3">Not at all Spammy<br/>3</col>
    """

    lines = [line.strip() for line in get_current_range() if line.strip()]

    row_rgx = re.compile(r"^(?P<num>[a-zA-Z0-9-_]+)\.?\s+(?P<text>\w.*)")

    poleTemplate  =  "{num}. {text}<br/>{num}"
    innerTemplate =  "{num}. {num}"

    for i, line in enumerate(lines):
        if row_rgx.match(line):
            lines[i] = poleTemplate.format(**row_rgx.match(line).groupdict())
        else:
            num = re.match(r"(?P<num>\d+)\.?", line)
            lines[i] = innerTemplate.format(**num.groupdict())

    set_current_range( deciphervimclips.cell_factory(lines, "col", "c") )


def Case():
    """
    Creates a ``pipe`` Element with each line of vrange becoming
    a case with an empty cond

    .. code-block::xml

        Spam
        Ham
        Eggs

        <pipe label="" capture="">
            <case label="c1" cond="">Spam</case>
            <case label="c2" cond="">Ham</case>
            <case label="c3" cond="">Eggs</case>
            <case label="c99" cond="1">BAD PIPE</case>
        </pipe>
    """
    print('test')

    cases = deciphervimclips.cell_factory( get_current_range(), "case", "c", attrs={'cond': ''} )

    cases.append("""  <case label="c99" cond="1">BAD PIPE</case>""")

    cases = ['<pipe label="" capture="">'] + cases + ['</pipe>']

    # set_current_range( cases )

    print(dir(vim.current.range.start))
    # cursor = vim.current.window.cursor
    # vim.current.window.cursor = cursor[0], cursor[1] + 12


def NoAnswer():
    """
    Makes ``noanswer`` Cells with vrange lines as text nodes

    .. code-block::xml

        99. Ni!

        <noanswer label="r99">Ni!</noanswer>
    """
    set_current_range( deciphervimclips.cell_factory(get_current_range(), "noanswer", "r") )


def Resource():
    """
    Makes ``res`` Cells with vrange lines as text nodes

    .. code-block::xml

        dp. Dead Parrot

        <res label="dp">Dead Parrot</res>
    """
    lines = [line for line in get_current_range() if line.strip()]

    label_rgx = re.compile('^(?P<label>\w*)\. (?P<text>.*)\s*$')

    resTemplate   = '<res label="{label}">{text}</res>'

    output = []
    for line in lines:
        hasLabel = label_rgx.match(line)
        if hasLabel:
            output.append(resTemplate.format(**hasLabel.groupdict()))
        else:
            output.append(resTemplate.format(label='', text=line))

    set_current_range( output )

    # cursor = vim.current.window.cursor
    # vim.current.window.cursor = cursor[0], 11


def MakeRadio():
    """
    """
    position = position_cursor(2, 999)
    questionText = '\n'.join(get_current_range())

    hasRow = questionText.find('<row') != -1
    hasCol = questionText.find('<col') != -1

    comment1D = "Please select one"
    comment2D = "Please select one for each row"

    if hasRow and hasCol:
        comment = comment2D
    else:
        comment = comment1D

    element = deciphervimclips.element_factory(get_current_range(),
                                        elType="radio",
                                        comment=comment)
    element = deciphervimclips.openify(element)


    set_current_range( element )
    vim.current.window.cursor = position


def MakeCheckbox():
    """
    """
    position = position_cursor(3, 999)
    comment = "Please select all that apply"
    attrs = dict(atleast=1)
    element = deciphervimclips.element_factory(get_current_range(),
                                        attrs=attrs,
                                        elType="checkbox",
                                        comment=comment)

    element = deciphervimclips.exclusify(element)
    element = deciphervimclips.openify(element)

    set_current_range( element )
    vim.current.window.cursor = position


def MakeSelect():
    """
    """
    position = position_cursor(3, 999)
    questionText = '\n'.join(get_current_range())

    hasRow = questionText.find('<row') != -1
    hasCol = questionText.find('<col') != -1

    comment1D = "Please select one"
    comment2D = "Please select one for each selection"

    if hasRow or hasCol:
        comment = comment2D
    else:
        comment = comment1D

    attrs = dict(optional=0)

    output = deciphervimclips.element_factory(get_current_range(),
                                    attrs=attrs,
                                    elType="select",
                                    comment=comment)

    set_current_range( output )
    vim.current.window.cursor = position


def MakeNumber():
    """
    """
    position = position_cursor(4, 999)
    attrs = dict(size=3, optional=0)
    comment = "Please enter a whole number"

    output = deciphervimclips.element_factory(get_current_range(),
                                    elType="number",
                                    attrs=attrs,
                                    comment=comment)
    set_current_range( output )
    vim.current.window.cursor = position


def MakeFloat():
    """
    """
    position = position_cursor(4, 999)
    attrs = dict(size=3, optional=0)
    comment = "Please enter a number"

    output = deciphervimclips.element_factory(get_current_range(),
                                    elType="float",
                                    attrs=attrs,
                                    comment=comment)
    set_current_range( output )
    vim.current.window.cursor = position


def MakeText():
    """
    """
    position = position_cursor(3, 999)
    attrs = dict(optional=0)
    comment = "Please be as specific as possible"

    output = deciphervimclips.element_factory(get_current_range(),
                                    elType="text",
                                    attrs=attrs,
                                    comment=comment)

    set_current_range( output )
    vim.current.window.cursor = position


def MakeTextarea():
    """
    """
    position = position_cursor(3, 999)
    comment = "Please be as specific as possible"
    attrs = dict(optional=0)

    output = deciphervimclips.element_factory(get_current_range(),
                                    attrs=attrs,
                                    elType="textarea",
                                    comment=comment)

    set_current_range( output )
    vim.current.window.cursor = position


def MakeHTML():
    """
    """
    position = position_cursor(1, 13)
    INDENT = 4

    lines = '\n'.join(' ' * INDENT + line for line in get_current_range() if line.strip())
    htmlTemplate = ('<html label="" where="survey">',
                    '%s',
                    '</html>')
    htmlTemplate = '\n'.join(htmlTemplate)

    output = (htmlTemplate % lines).split('\n')

    set_current_range( output )
    vim.current.window.cursor = position


def MakeRating():
    """
    """
    position = position_cursor(6, 999)
    questionText = '\n'.join(get_current_range())

    hasRow = questionText.find('<row') != -1
    hasCol = questionText.find('<col') != -1

    comment1D = "Please select one"
    comment2D = "Please select one for each row"

    if hasRow and hasCol:
        comment = comment2D
    else:
        comment = comment1D

    attrs = dict(type="rating", values="order", averages="cols", adim="rows")

    output = deciphervimclips.element_factory(get_current_range(),
                                    attrs=attrs,
                                    elType="radio",
                                    comment=comment)

    set_current_range( output )
    vim.current.window.cursor = position


def MakeNets():
    """
    """
    position = position_cursor(1, 12)
    set_current_range( ['  <net labels="">%s</net>' % res.strip() for res in get_current_range() if res.strip()])
    vim.current.window.cursor = position



def MakeGroups():
    """
    """
    output =  deciphervimclips.cell_factory(get_current_range(), "group", "g")

    set_current_range( output )


def MakeExtras():
    """
    Pulls text-node into cs:extra attribute
    Also attempts to make spacing uniform within xml

    .. code-block::xml

        <row label="r1">SPAM SPAM SPAM</row>
        <row label="r2">SPAM</row>

        <row label="r1" cs:extra="SPAM SPAM SPAM">SPAM SPAM SPAM</row>
        <row label="r2" cs:extra="SPAM"          >SPAM</row>
    """
    vrange = [line for line in get_current_range() if line.strip()]
    textNode_rgx = re.compile('>(.*?)<')

    selection = vrange

    textNodes = [textNode_rgx.findall(line)[0] for line in selection]
    maxWidth = max(len(text) for text in textNodes) + 1
    attrTemplate = '{0:<%d}>' % maxWidth

    newSelection = []
    for row, node in zip(selection, textNodes):
        csExtra = ' cs:extra="' + attrTemplate.format(node + '"')
        newRow = row.replace('>', csExtra, 1)
        newSelection.append(newRow)

    set_current_range( newSelection )


def MainMakeOrs():

    def MakeOrs(line, label, indices, element, joinType='or'):
        """
        """
        import re

        indices = indices.strip()
        if indices.find('--') != -1:
            raise SyntaxError("Cannot have multiple dashes in range")

        firstChar = indices[0]
        elementTest  = re.sub('[-,\s]', '', indices)
        indices = (i.strip() for i in indices.split(','))
        joinType = ', ' if joinType == ',' else ' %s ' % joinType

        syntaxMsg = "Unknown input. Ranges should numeric 1-10, or alpha A-F, but not both"
        valueMsg = "Range is backwards: {0}-{1}"

        res = []

        if firstChar.isdigit():
            if not re.match(r'^\d+$', elementTest):
                raise SyntaxError(syntaxMsg)

            for i in indices:
                if '-' in i:
                    start, end = map(int, i.split('-'))
                    if start > end:
                        raise ValueError(valueMsg.format(start, end))
                    rng = list(range(start, end + 1))
                    res.extend(map(str, rng))
                else:
                    res.append(i)

        if firstChar.isalpha():
            if not (re.match(r'^[a-z]+$', elementTest) or re.match(r'^[A-Z]+$', elementTest)):
                raise SyntaxError("Cannot mix case. All letters must be UPPER or lower")

            for c in indices:
                case = string.uppercase if firstChar.isupper() else string.lowercase

                if '-' in c:
                    start, end = c.split('-')
                    if len(start) > len(end):
                        raise ValueError(valueMsg.format(start, end))
                    for c in (start, end):
                        if c.count(c[0]) != len(c):
                            raise SyntaxError("Labels must be uniform: AA BB CC, not AC")
                    startIndex = case.index(start[0])
                    if len(start) == len(end):
                        endIndex = case.index(end[0])
                        if endIndex < startIndex:
                            raise ValueError(valueMsg.format(start, end))
                    multiplier = len(start)
                    rng = [start]
                    while start != end:
                        i = (startIndex + 1) % len(case)
                        if i < startIndex:
                            multiplier += 1
                        startIndex = i
                        start = case[startIndex] * multiplier
                        rng.append(start)
                    res.extend(rng)
                else:
                    res.append(c)

        formatDict = {'label': label, 'element': element, 'joinType': joinType}

        condString = joinType.join(["%(label)s.%(element)s" % formatDict + c for c in res])

        cond_rgx = re.compile('cond=".*?"')
        rowCond_rgx = re.compile('rowCond=".*?"')
        colCond_rgx = re.compile('colCond=".*?"')

        if rowCond_rgx.search(line) and re.search(r'\[row\]', condString):
            return rowCond_rgx.sub('rowCond="{0}"'.format(condString), line)
        elif colCond_rgx.search(line) and re.search(r'\[col\]', condString):
            return colCond_rgx.sub('colCond="{0}"'.format(condString), line)
        elif cond_rgx.search(line):
            return cond_rgx.sub('cond="{0}"'.format(condString), line)

        return condString


    def python_input(message):
        vim.command('call inputsave()')
        vim.command("let user_input = input('" + message + ": ')")
        vim.command('call inputrestore()')
        return vim.eval('user_input')

    try:
        label     = python_input("Question Label")
        indices   = python_input("Label Numbers: e.g. (1-4,5|A-D,E)")
        element   = python_input("Cell Type: e.g. (r|c|ch)")
        joinType  = python_input("Join type: e.g. (or|and|,) [or]") or 'or'
    except KeyboardInterrupt:
        pass
    else:
        args = (arg.strip() for arg in (label, indices, element, joinType))
        vim.current.line = MakeOrs(vim.current.line, *args)


def AddValuesLow():
    """
    Adds value attributes to cells from low to high

    .. code-block::xml

        <col label="c1">Very Spammy<br/>1</col>
        <col label="c2">2</col>
        <col label="c3">Not at all Spammy<br/>3</col>

        <col label="c1" value="1">Very Spammy<br/>1</col>
        <col label="c2" value="2">2</col>
        <col label="c3" value="3">Not at all Spammy<br/>3</col>
    """
    i = 1
    output = []
    for line in get_current_range():
        if '>' in line:
            output.append(line.replace('>', ' value="%d">' % i, 1))
            i += 1
        else:
            output.append(line)

    set_current_range( output )


def AddValuesHigh():
    """
    Adds value attributes to cells from high to low

    .. code-block::xml

        <col label="c3">Not at all Spammy<br/>3</col>
        <col label="c2">2</col>
        <col label="c1">Very Spammy<br/>1</col>

        <col label="c3" value="3">Not at all Spammy<br/>3</col>
        <col label="c2" value="2">2</col>
        <col label="c1" value="1">Very Spammy<br/>1</col>
    """
    i = len([line for line in get_current_range() if '>' in line])
    output = []
    for line in get_current_range():
        if '>' in line:
            output.append(line.replace('>', ' value="%d">' % i, 1))
            i -= 1
        else:
            output.append(line)

    set_current_range( output )


def Switcher():
    """
    """
    vrange = get_current_range()
    for i in range(len(vrange)):
        if "<row" in vrange[i]:
            this1 = "row"
            that1 = "col"
            this2 = "r"
            that2 = "c"
        elif "<col" in vrange[i]:
            this1 = "col"
            that1 = "row"
            this2 = "c"
            that2 = "r"
        vrange[i] = re.sub("(<|\/)" + this1, r'\1' + that1, vrange[i])
        vrange[i] = re.sub('label="%s' % this2, 'label="%s' % that2, vrange[i])
    set_current_range( vrange )


def SwitchRating():
    """
    """
    vline = vim.current.line
    namesToSwitch  = ('averages', 'adim')
    valuesToSwitch = ('cols', 'rows')

    combos = []
    for attr in namesToSwitch:
        pair = []
        for val in valuesToSwitch:
            pair.append('{0}="{1}"'.format(attr, val))
        combos.append(pair)

    for combo in combos:
        for i, attr in enumerate(combo):
            if vline.find(attr) != -1:
                vline = vline.replace(attr, combo[i ^ 1])
                break

    set_current_range( vline )


def AddGroups():
    """
    """
    vrange = get_current_range()
    for i, line in enumerate(vrange):
        vrange[i] = line.replace(">", ' groups="g1">', 1)

    set_current_range( vrange )


def CommentQuestion():
    """
    """
    vrange = get_current_range()
    INDENT = 2
    INDENT = ' ' * INDENT

    if len(vrange) == 1:
        template = INDENT + "<comment>%s</comment>"
        selection = '\n'.join([line.strip() for line in vrange if line.strip()])
    else:
        template = INDENT + "<comment>\n%s\n" + INDENT + "</comment>"
        selection = '\n'.join([(INDENT * 2) + line.strip() for line in vrange if line.strip()])

    set_current_range( (template % selection).split('\n') )


def HTMLComment():
    """
    """
    set_current_range( ['<!--'] + get_current_range() + ['-->'] )


def AddAlts():
    """
    Inserts an <alt> for Cells and Element <title>

    .. code-block::xml

        <title>What is your favorite color?</title>
        <row label="r1">Blue</row>
        <row label="r2">Green</row>
        <row label="r3">Red</row>

        <title>What is your favorite color?</title>
        <alt>What is your favorite color?</alt>
        <row label="r1"><alt>Blue</alt>Blue</row>
        <row label="r2"><alt>Green</alt>Green</row>
        <row label="r3"><alt>Red</alt>Red</row>
    """
    ELEMENTS = ('row', 'col', 'choice', 'group')

    selection = '\n'.join(get_current_range())

    rgxTemplate = "(?P<open><({elements}).*?>)(?P<text>.*?)(?P<close></({elements})\s*?>)"
    cell_rgx  = re.compile(rgxTemplate.format(elements='|'.join(ELEMENTS)), re.DOTALL)
    title_rgx = re.compile(rgxTemplate.format(elements='title'), re.DOTALL)

    cellSub  = "\g<open><alt>\g<text></alt>\g<text>\g<close>"
    titleSub = "\g<open>\g<text>\g<close>\n  <alt>\g<text></alt>"

    selection = cell_rgx.sub(cellSub, selection)
    selection = title_rgx.sub(titleSub, selection)

    set_current_range( selection.split('\n') )


def URLQuote():
    set_current_range( [quote(line) for line in get_current_range()] )


def Strip():
    """
    Strip the text-node out of it's Cell

    .. code-block::xml

        <row label="r1">Want to be free</row>

        Want to be free
    """

    ELEMENTS = ('row', 'col', 'choice', 'group')

    text_rgx = re.compile('\s*<({elements}).*?>(?P<text>.*?)</({elements}).*'.format(elements='|'.join(ELEMENTS)))

    output = []

    for line in get_current_range():
        match = text_rgx.match(line)
        if match:
            output.append(match.groupdict()['text'])
        else:
            output.append(line.strip())

    set_current_range( output )


def Justify():
    """
    Justify a long string of words
    to MAX_LINE_LENGTH. Preserves indentation
    """
    selection = ''.join(get_current_range())

    MAX_LINE_LENGTH = 79

    indent = len(selection) - len(selection.lstrip())
    words  = [word for word in selection.split(' ') if word]

    lines = []

    lineLength = 0
    curLine = []
    wordCount = len(words)
    for i, word in enumerate(words):
        curLine.append(word)
        lineLength += len(word)
        if lineLength > MAX_LINE_LENGTH or (i == wordCount - 1):
            lines.append(' ' * indent + ' '.join(curLine))
            curLine, lineLength = [], 0

    set_current_range( lines )


def CleanNotes():
    """
    Clean up TaskList notes for email

    .. code-block::xml

        <!-- XXX [Q1]: The parrot is dead! -->

        [Q1]: The parrot is dead! 
    """
    vbuffer = vim.current.buffer[:]
    comment_rgx = re.compile(r'.*XXX \[(?P<label>[^\]]+)\]: (?P<note>.*) -->')

    template = '[{label}]: {note}'

    output = []
    for line in vbuffer:
        match = comment_rgx.match(line)
        if match:
            output.append(template.format(**match.groupdict()))
        else:
            output.append(line)

    vim.current.buffer[:] = output
