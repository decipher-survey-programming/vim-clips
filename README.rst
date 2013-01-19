#############################
decipher-clips plugin for VIM
#############################


Installation
============

You might want to use `pathogen <https://github.com/tpope/vim-pathogen>`_ to
install decipher-clips in VIM. Also you need a VIM version that was compiled with
``+python``, which is typical for most distributions on Linux.


Cheat Sheet
===========

Normal Mode
    Clean up unicode, newlines, tabs and place the current buffer in a new-survey template

    .. code-block::

        <leader>ss

    **Make Ors**: Create boolean logic you can trust. Conditions will be placed inside cond if present
    on current line. Supports alpha ranges as well as numeric.

    .. code-block::

        <leader>mo

        Label?: Q1
        Indices?: 1-3,5,8
        Cell Type?: r
        Join type? [or]: or

        returns: Q1.r1 or Q1.r2 or Q1.r3 or Q1.r5 or Q1.r8

        <leader>mo

        Label?: Q2
        Indices?: A-C,E,H
        Cell Type?:
        Join type? [or]:

        returns: Q2.A or Q2.B or Q2.C or Q2.E or Q2.H

    Justify the current line to prevent horizontal scrolling

    .. code-block::

        <leader>ju

    **Switch Rating**: Switch adim and averages between cols and rows

    .. code-block::

        <leader>sr

    Open the current buffer into parts *delimited by blank lines* in gvimdiff

    .. code-block::

        <leader>dif

    To clean ``<!-- XXX [foo]: bar -->`` notes made by snipmate for sending to QA

    .. code-block::

        <leader>no

    Turn the current line into a hyperlink

    .. code-block::

        <leader>hr

    Turn the current line into a mailto: hyperlink

    .. code-block::

        <leader>mai

    Insert ``exclusive="1" randomize="0"``

    .. code-block::

        <leader>ee

    Insert ``randomize="0"``

    .. code-block::

        <leader>rr

    Insert ``open="1" openSize="25" randomize="0"``

    .. code-block::

        <leader>oe

    Insert ``aggregate="0" percentages="0"``

    .. code-block::

        <leader>aa

    Insert ``optional="1"``

    .. code-block::

        <leader>oo

    Insert ``where="execute"``

    .. code-block::

        <leader>dev

    Insert ``shuffle="rows"``

    .. code-block::

        <leader>sh

    Insert ``<suspend/>`` below current line

    .. code-block::

        <leader>su

    Insert ``<br/><br/>``

    .. code-block::

        <leader>br

    **Mail Break**: Insert ``<br><br>``

    .. code-block::

        <leader>mb


Visual Mode
    Make row Cells

    .. code-block::

        <leader>ro

    Make col Cells

    .. code-block::

        <leader>co

    Make choice Cells

    .. code-block::

        <leader>ch

    Make rating row cells with poles. e.g. ``Disagree</br>1,2,3,4,Agree<br/>5``

    .. code-block::

        <leader>ra

    Make radio Element

    .. code-block::

        <leader>mr

    Make checkbox Element

    .. code-block::

        <leader>mc

    Make select Element

    .. code-block::

        <leader>ms

    Make number Element

    .. code-block::

        <leader>mn

    Make float Element

    .. code-block::

        <leader>mf

    Make text Element

    .. code-block::

        <leader>mt

    Make textarea Element

    .. code-block::

        <leader>ma

    Make html Element

    .. code-block::

        <leader>mh

    **Make Values**: Make radio-rating Element

    .. code-block::

        <leader>mv

    Make res Elements

    .. code-block::

        <leader>re

    Make group Cells

    .. code-block::

        <leader>mg

    Make net Cells

    .. code-block::

        <leader>ne

    Make noanswer Cells

    .. code-block::

        <leader>na

    Make pipe by creating cases out of selected lines

    .. code-block::

        <leader>ca

    Add values to Cells from low to high

    .. code-block::

        <leader>avl

    Add values to Cells from high to low

    .. code-block::

        <leader>avh

    Add groups to Cells

    .. code-block::

        <leader>ag

    Add alts to Cells and title

    .. code-block::

        <leader>aa

    Create a question comment

    .. code-block::

        <leader>qc

    Escape ``< and >``

    .. code-block::

        <leader>es

    **HTML Comment**: Comment out some text

    .. code-block::

        <leader>hc

    **Make Extras**: Pull text node into configurable style

    .. code-block::

        <leader>me

    **Quote Spaces**: HTML escape spaces

    .. code-block::

        <leader>qs

    Strip text-nodes from selected Cells

    .. code-block::

        <leader>st

    Switch selected Cells between cols and rows

    .. code-block::

        <leader>sw

    **Quote URL**: URL escape selection

    .. code-block::

        <leader>qu

    Clean out common utf-8 chars and remove excessive tabs, newlines, etc

    .. code-block::

        <leader>cl
