decipher-clips plugin for vim
=============================

.. image:: https://travis-ci.org/rwscarb/decipher-clips.png?branch=master
        :target: https://travis-ci.org/rwscarb/decipher-clips


Installation
~~~~~~~~~~~~

You might want to use `pathogen <https://github.com/tpope/vim-pathogen>`_ to
install decipher-clips in vim. Also you need a vim version that was compiled with
``+python``, which is typical for most distributions on Linux.


Cheat Sheet
~~~~~~~~~~~

Normal Mode
-----------

These commands are to be executed in vim's Normal mode

**NewSurvey**

Clean up unicode, newlines, tabs and place the current buffer in a new-survey template. This is typically
the first thing done when working with a *new* survey.

.. code-block:: xml+cheetah

    <leader>ss

**MakeOrs**

Create boolean logic you can trust. Conditions will be put inside a ``cond=""`` (if present)
on the line where invoked. Supports alpha ranges as well as numeric. Will place (if found) ``[row]``
into a ``rowCond=""`` and ``[col]`` into a ``colCond=""`` similar to the third example below.

.. code-block:: xml+cheetah

    <leader>mo

    Question Label?: Q1
    Label Numbers: e.g. (1-4,5|A-D,E): 1-3,5,8  // supports mixture of ranges and individual indices
    Cell Type: e.g. (r|c|ch): r
    Join type: e.g. (or|and|,) [or]: and        // default is to use `or`

...will become...

.. code-block:: xml+cheetah

    Q1.r1 and Q1.r2 and Q1.r3 and Q1.r5 and Q1.r8

.. code-block:: xml+cheetah

    <leader>mo

    Question Label?: Q2
    Label Numbers: e.g. (1-4,5|A-D,E): A-C,E,H  // support alpha ranges as well
    Cell Type: e.g. (r|c|ch):
    Join type: e.g. (or|and|,) [or]:

...will become...

.. code-block:: xml+cheetah

    Q2.A or Q2.B or Q2.C or Q2.E or Q2.H

.. code-block:: xml+cheetah

    <leader>mo

    Question Label?: Q3[row]                   // useful in row and col conds
    Label Numbers: e.g. (1-4,5|A-D,E): 1-5
    Cell Type: e.g. (r|c|ch): c
    Join type: e.g. (or|and|,) [or]:

...will become...

.. code-block:: xml+cheetah

    Q3[row].c1 or Q3[row].c2 or Q3[row].c3 or Q3[row].c4 or Q3[row].c5

**Justify**

Justify the current line with hard breaks, removing extra spaces in the process. Indentation will
be preserved and words will not be broken.

.. code-block:: xml+cheetah

    <leader>ju

    Well, there's egg and bacon; egg sausage and bacon; egg and spam; egg bacon and spam; egg bacon sausage and spam; spam bacon sausage and spam; spam egg spam spam bacon and spam; spam sausage spam spam bacon spam tomato and spam

...will become...

.. code-block:: xml+cheetah

    Well, there's egg and bacon; egg sausage and bacon; egg and spam; egg bacon and spam; egg bacon sausage
    and spam; spam bacon sausage and spam; spam egg spam spam bacon and spam; spam sausage spam spam bacon
    spam tomato and spam

**SwitchRating**

Switch adim and averages between cols and rows

.. code-block:: xml+cheetah

    <leader>sr

    averages="cols" adim="rows"

...will become...

.. code-block:: xml+cheetah

    averages="rows" adim="cols"

**Vimdiff**

Open the current buffer into parts **delimited by blank lines** in gvimdiff. This is very handy when trying
to discover differences between repeating items in a questionnaire.

.. code-block:: xml+cheetah

    <leader>dif

**CommentBlocks**

Add ``<!-- EO block -->`` style comments to the end of blocks for easier navigation of nested block trees

.. code-block:: xml+cheetah

    <leader>cb

    <block label="spam_block" randomizeChildren="0" cond="1">
    <radio label="Q1">
        <title>
        What would you like to eat?
        </title>
        <comment>Please select one</comment>
        <row label="r1">Ham</row>
        <row label="foo">Spam</row>
        <row label="r3">bar Eggs</row>
        <row label="r42">Bacon</row>
    </radio>
    <suspend/>
    </block>

...will become...

.. code-block:: xml+cheetah

    <block label="spam_block" randomizeChildren="0" cond="1">
    <radio label="Q1">
        <title>
        What would you like to eat?
        </title>
        <comment>Please select one</comment>
        <row label="r1">Ham</row>
        <row label="foo">Spam</row>
        <row label="r3">bar Eggs</row>
        <row label="r42">Bacon</row>
    </radio>
    <suspend/>
    </block>
    <!-- EO spam_block -->

**AttrSpacing**

Justifies the spacing of attributes accross multiple xml elements

.. code-block:: xml+cheetah

    <row label="ham" cs:extra="HAM"  >HAM</row>
    <row label="spam" cs:extra="SPAM" >SPAM</row>
    <row label="r3" cs:extra="BACON" exclusive="1" randomize="0">BACON</row>

...will become...

.. code-block:: xml+cheetah

    <row label="ham"  cs:extra="HAM"  >HAM</row>
    <row label="spam" cs:extra="SPAM" >SPAM</row>
    <row label="r3"   cs:extra="BACON" exclusive="1" randomize="0">BACON</row>

**CleanNotes**

To clean aggregated tasks in the form of ``<!-- XXX [foo]: bar -->``

.. code-block:: xml+cheetah

    <leader>no

    <!-- XXX [Q1]: Not enough Spam -->
    <!-- XXX [Q2]: Bacon doesn't have Spam on it -->
    <!-- XXX [Q3]: Spam, then Eggs, then Spam -->

...will become...

.. code-block:: xml+cheetah

    [Q1]: Not enough Spam
    [Q2]: Bacon doesn't have Spam on it
    [Q3]: Spam, then Eggs, then Spam

**Insertions**

Executing these commands will insert their accompanied text at the cursor's position

.. code-block:: xml+cheetah

    <leader>ee

    exclusive="1" randomize="0"

.. code-block:: xml+cheetah

    <leader>rr

    randomize="0"

.. code-block:: xml+cheetah

    <leader>oe

    open="1" openSize="25" randomize="0"

.. code-block:: xml+cheetah

    <leader>aa

    aggregate="0" percentages="0"

.. code-block:: xml+cheetah

    <leader>oo

    optional="1"

.. code-block:: xml+cheetah

    <leader>dev

    where="execute"

.. code-block:: xml+cheetah

    <leader>sh

    shuffle="rows"

.. code-block:: xml+cheetah

    <leader>su

    <suspend/>  // this is inserted below the current line

.. code-block:: xml+cheetah

    <leader>br

    <br/><br/>

.. code-block:: xml+cheetah

    <leader>mb

    <br><br>


Visual Mode
-----------

These commands are to be executed in vim's Visual mode.
Note the use of the period as a delimiter of a cell's label.

**Rows**

Make row cells

.. code-block:: xml+cheetah

    <leader>ro

    Ham
    foo. Spam
    bar Eggs
    42. Bacon

...will become...

.. code-block:: xml+cheetah

      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

**Cols**

Make col cells

.. code-block:: xml+cheetah

    <leader>co

    Ham
    foo. Spam
    bar Eggs
    42. Bacon

...will become...

.. code-block:: xml+cheetah

      <col label="c1">Ham</col>
      <col label="foo">Spam</col>
      <col label="c3">bar Eggs</col>
      <col label="c42">Bacon</col>

**Choice**

Make choice cells

.. code-block:: xml+cheetah

    <leader>ch

    Ham
    foo. Spam
    bar Eggs
    42. Bacon

...will become...

.. code-block:: xml+cheetah

      <choice label="ch1">Ham</choice>
      <choice label="foo">Spam</choice>
      <choice label="ch3">bar Eggs</choice>
      <choice label="ch42">Bacon</choice>

**Rates**

Make rating-style col cells with ``<br/>`` tags before poles. Note: periods delimiting labels and text
are optional as the digits are assumed to be the rating numbers.

.. code-block:: xml+cheetah

    <leader>ra

    1 Spammy
    2
    3
    4
    5 Very Spammy

...will become...

.. code-block:: xml+cheetah

    <col label="c1">Spammy<br/>1</col>
    <col label="c2">2</col>
    <col label="c3">3</col>
    <col label="c4">4</col>
    <col label="c5">Very Spammy<br/>5</col>

**MakeRadio**

Make radio element

.. code-block:: xml+cheetah

    <leader>mr

    Q1 Which is your favorite?
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

...will become...

.. code-block:: xml+cheetah

    <radio label="Q1">
      <title>
        Which is your favorite?
      </title>
      <comment>Please select one</comment>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>
    </radio>
    <suspend/>

**MakeRating**

Make radio-rating element

.. code-block:: xml+cheetah

    <leader>mv

    Q1 Please rate each item by it's spam factor
      <col label="c1">Spammy<br/>1</col>
      <col label="c2">2</col>
      <col label="c3">3</col>
      <col label="c4">4</col>
      <col label="c5">Very Spammy<br/>5</col>
      <row label="r1">Spam</row>
      <row label="r2">Spam Spam</row>
      <row label="r3">Spam Spam Spam</row>

...will become...

.. code-block:: xml+cheetah

    <radio label="Q1" averages="cols" values="order" adim="rows" type="rating">
      <title>
        Please rate each item by it's spam factor
      </title>
      <comment>Please select one for each row</comment>
      <col label="c1">Spammy<br/>1</col>
      <col label="c2">2</col>
      <col label="c3">3</col>
      <col label="c4">4</col>
      <col label="c5">Very Spammy<br/>5</col>
      <row label="r1">Spam</row>
      <row label="r2">Spam Spam</row>
      <row label="r3">Spam Spam Spam</row>
    </radio>
    <suspend/>

**MakeCheckbox**

Make checkbox element

.. code-block:: xml+cheetah

    <leader>mc

    Q1 What would you like?
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

...will become...

.. code-block:: xml+cheetah

    <checkbox label="Q1" atleast="1">
      <title>
        What would you like?
      </title>
      <comment>Please select all that apply</comment>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>
    </checkbox>
    <suspend/>

**MakeSelect**

Make select element

.. code-block:: xml+cheetah

    <leader>ms

    Q1 Select your quantity of each...
      <choice label="ch1">0</choice>
      <choice label="ch2">1</choice>
      <choice label="ch3">2</choice>
      <choice label="ch4">3</choice>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

...will become...

.. code-block:: xml+cheetah
    
    <select label="Q1" optional="0">
      <title>
        Select your quantity of each...
      </title>
      <comment>Please select one for each selection</comment>
      <choice label="ch1">0</choice>
      <choice label="ch2">1</choice>
      <choice label="ch3">2</choice>
      <choice label="ch4">3</choice>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>
    </select>
    <suspend/>

**MakeNumber**

Make number element

.. code-block:: xml+cheetah

    <leader>mn

    Q1 Enter desired quantity for each item...
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

...will become...

.. code-block:: xml+cheetah

    <number label="Q1" optional="0" size="3">
      <title>
        Enter desired quantity for each item...
      </title>
      <comment>Please enter a whole number</comment>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>
    </number>
    <suspend/>

**MakeFloat**

Make float element

.. code-block:: xml+cheetah

    <leader>mf

    Q1 What... is the air-speed velocity of an unladen swallow?

...will become...

.. code-block:: xml+cheetah

    <float label="Q1" optional="0" size="3">
      <title>
        What... is the air-speed velocity of an unladen swallow?
      </title>
      <comment>Please enter a number</comment>
    </float>
    <suspend/>

**MakeText**

Make text element

.. code-block:: xml+cheetah

    <leader>mt

    Q1 Please explain your love for the following...
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>

...will become...

.. code-block:: xml+cheetah

    <text label="Q1" optional="0">
      <title>
        Please explain your love for the following...
      </title>
      <comment>Please be as specific as possible</comment>
      <row label="r1">Ham</row>
      <row label="foo">Spam</row>
      <row label="r3">bar Eggs</row>
      <row label="r42">Bacon</row>
    </text>
    <suspend/>

**MakeTextarea**

Make textarea element

.. code-block:: xml+cheetah

    <leader>ma

    Q42 Briefly describe the ultimate question of life, the universe, and everything

...will become...

.. code-block:: xml+cheetah

    <textarea label="Q42" optional="0">
      <title>
        Briefly describe the ultimate question of life, the universe, and everything
      </title>
      <comment>Please be as specific as possible</comment>
    </textarea>
    <suspend/>

**MakeHTML**

Make html element

.. code-block:: xml+cheetah

    <leader>mh

    That's it. That's all there is.

...will become...

.. code-block:: xml+cheetah

    <html label="" where="survey">
      <p>
        That's it. That's all there is.
      </p>
    </html>

**Resource**

Make res elements

.. code-block:: xml+cheetah

    <leader>re

    spamLot. Ham Spam Eggs Bacon and Spam

...will become...

.. code-block:: xml+cheetah

    <res label="spamLot">Ham Spam Eggs Bacon and Spam</res>

**MakeGroups**

Make group cells

.. code-block:: xml+cheetah

    <leader>mg

    Spam
    Eggs
    Bacon
    Ham

...will become...

.. code-block:: xml+cheetah

      <group label="g1">Spam</group>
      <group label="g2">Eggs</group>
      <group label="g3">Bacon</group>
      <group label="g4">Ham</group>

**MakeNets**

Make net Cells

.. code-block:: xml+cheetah

    <leader>ne

    Spam
    Eggs
    Bacon
    Ham

...will become...

.. code-block:: xml+cheetah

      <net labels="">Spam</net>
      <net labels="">Eggs</net>
      <net labels="">Bacon</net>
      <net labels="">Ham</net>

**NoAnswer**

Make noanswer cells

.. code-block:: xml+cheetah

    <leader>na

    r99. I do not like spam

...will become...

.. code-block:: xml+cheetah

      <noanswer label="r99">I do not like spam</noanswer>

**Case**

Make a pipe consisting of selected lines as cases

.. code-block:: xml+cheetah

    <leader>ca

    Spam
    Eggs
    Bacon
    Ham

...will become...

.. code-block:: xml+cheetah

    <pipe label="" capture="">
      <case label="c1" cond="">Spam</case>
      <case label="c2" cond="">Eggs</case>
      <case label="c3" cond="">Bacon</case>
      <case label="c4" cond="">Ham</case>
      <case label="c99" cond="1">BAD PIPE</case>
    </pipe>

**AddValuesLow**

Add values to cells from low to high

.. code-block:: xml+cheetah

    <leader>avl

      <col label="c1">Spammy<br/>1</col>
      <col label="c2">2</col>
      <col label="c3">3</col>
      <col label="c4">4</col>
      <col label="c5">Very Spammy<br/>5</col>

...will become...

.. code-block:: xml+cheetah

      <col label="c1" value="1">Spammy<br/>1</col>
      <col label="c2" value="2">2</col>
      <col label="c3" value="3">3</col>
      <col label="c4" value="4">4</col>
      <col label="c5" value="5">Very Spammy<br/>5</col>

**AddValuesHigh**

Add values to cells from high to low

.. code-block:: xml+cheetah

    <leader>avh

      <col label="c5">Very Spammy<br/>5</col>
      <col label="c4">4</col>
      <col label="c3">3</col>
      <col label="c2">2</col>
      <col label="c1">Spammy<br/>1</col>

...will become...

.. code-block:: xml+cheetah

      <col label="c5" value="5">Very Spammy<br/>5</col>
      <col label="c4" value="4">4</col>
      <col label="c3" value="3">3</col>
      <col label="c2" value="2">2</col>
      <col label="c1" value="1">Spammy<br/>1</col>

**AddGroups**

Add groups to cells

.. code-block:: xml+cheetah

    <leader>ag

      <row label="a">King Arthur</row>
      <row label="b">Launcelot</row>
      <row label="c">Shrubber</row>

...will become...

.. code-block:: xml+cheetah

      <row label="a" groups="g1">King Arthur</row>
      <row label="b" groups="g1">Launcelot</row>
      <row label="c" groups="g1">Shrubber</row>

**AddAlts**

Add alts to cells and title. Which ever is contained in the visual selection.

.. code-block:: xml+cheetah

    <leader>aa

    <text label="Q1" optional="0">
      <title>
        Please explain your love for the following...
      </title>
      <comment>Please be as specific as possible</comment>
      <row label="r1">${res.spam1}</row>
      <row label="r2">${res.spam2}</row>
      <row label="r3">${res.spam3}</row>
      <row label="r4">${res.spam4}</row>
    </text>
    <suspend/>

...will become...

.. code-block:: xml+cheetah

    <text label="Q1" optional="0">
      <title>
        Please explain your love for the following...
      </title>
      <alt>
        Please explain your love for the following...
      </alt>
      <comment>Please be as specific as possible</comment>
      <row label="r1"><alt>${res.spam1}</alt>${res.spam1}</row>
      <row label="r2"><alt>${res.spam2}</alt>${res.spam2}</row>
      <row label="r3"><alt>${res.spam3}</alt>${res.spam3}</row>
      <row label="r4"><alt>${res.spam4}</alt>${res.spam4}</row>
    </text>
    <suspend/>

**CommentQuestion**

Create a question comment

.. code-block:: xml+cheetah

    <leader>qc

    Please select one spam

...will become...

.. code-block:: xml+cheetah

      <comment>Please select one spam</comment>

**XMLEscape**

Escape ``< and >`` characters into ``&lt; and &gt;``

.. code-block:: xml+cheetah

    <leader>es

    Green eggs and <em>spam</em>

...will become...

.. code-block:: xml+cheetah

    Green eggs and &lt;em&gt;spam&lt;/em&gt;

**XML/HTML Comment**

Comment out some text from the xml

.. code-block:: xml+cheetah

    <leader>hc

    I have to push the pram a lot. 

...will become...

.. code-block:: xml+cheetah

    <!--
    I have to push the pram a lot. 
    -->

**Make Extras**

Pull text node value into a configurable style attribute. This is useful when you want to use row text,
but avoid translation problems.

.. code-block:: xml+cheetah

    <leader>me

      <row label="r1">Spam</row>
      <row label="r2">Ham</row>
      <row label="r3">Bacon</row>

...will become...

.. code-block:: xml+cheetah

      <row label="r1" cs:extra="Spam" >Spam</row>
      <row label="r2" cs:extra="Ham"  >Ham</row>
      <row label="r3" cs:extra="Bacon">Bacon</row>


**Quote Spaces**

HTML escape spaces. This is very useful when dealing with macro arguments which are space delimited 

.. code-block:: xml+cheetah

    <leader>qs

    That parrot is dead

...will become...

.. code-block:: xml+cheetah

    That&#32;parrot&#32;is&#32;dead

**Strip**

Strip text nodes from selected cells

.. code-block:: xml+cheetah

    <leader>st

      <col label="c1">Spammy<br/>1</col>
      <col label="c2">2</col>
      <col label="c3">3</col>
      <col label="c4">4</col>
      <col label="c5">Very Spammy<br/>5</col>
      <row label="r1">Spam</row>
      <row label="r2">Spam Spam</row>
      <row label="r3">Spam Spam Spam</row>

...will become...

.. code-block:: xml+cheetah

    Spammy<br/>1
    2
    3
    4
    Very Spammy<br/>5
    Spam
    Spam Spam
    Spam Spam Spam

**Switcher**

Switch back and forth between cols and rows

.. code-block:: xml+cheetah

    <leader>sw

      <row label="r1">Spam</row>
      <row label="r2">Spam Spam</row>
      <row label="r3">Spam Spam Spam</row>

...will become...

.. code-block:: xml+cheetah

      <col label="c1">Spam</col>
      <col label="c2">Spam Spam</col>
      <col label="c3">Spam Spam Spam</col>

**Quote URL**

URL escape selection. This very handy in passing text to certain swf's that do not do this themselves.

.. code-block:: xml+cheetah

    <leader>qu

    No, now go away or I shall taunt you a second time. 

...will become...

.. code-block:: xml+cheetah

    No%2C%20now%20go%20away%20or%20I%20shall%20taunt%20you%20a%20second%20time.%20

**CleanUp**

Clean out common utf-8 chars and remove excessive tabs and newlines

.. code-block:: xml+cheetah

    <leader>cl

    ‘“HAM”–“SPAM”&“EGGS”’…

...will become...

.. code-block:: xml+cheetah

    '"HAM"-"SPAM"&amp;"EGGS"'...

**HRef**

Turn the selected text into a hyperlink. This is useful in emails where the href and the
text node will have the same value.

.. code-block:: xml+cheetah

    <leader>hr

    http://google.com

...will become...

.. code-block:: xml+cheetah

    <a href="http://google.com">http://google.com</a>

**MailLink**

Turn the selected text into a ``mailto:`` hyperlink

.. code-block:: xml+cheetah

    <leader>ml

    foo@bar.com

...will become...

.. code-block:: xml+cheetah

    <a href="mailto:foo@bar.com">foo@bar.com</a>
