#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from string import uppercase, lowercase
from urllib import quote
sys.path.append('../decipher')
import decipher


pyFlakes = (os, uppercase, lowercase, quote, decipher)


class ClipParserException(Exception):
    pass


class ClipFunctionParser(object):
    """Parses out functions from a .vim plugin placing all
    parsed functions in global namespace"""
    FUNC_RGX = re.compile(r'\s*def ([A-Z].*?)\(.*')  # testable funcs are capitalized FUPEP8

    def __init__(self, clipPath):
        try:
            self.document = open(clipPath).readlines()
        except IOError:
            msg = "Could not open plugin: {path}"
            raise ClipParserException(msg.format(path=clipPath))

    def get_indent(self, string):
        return len(string) - len(string.lstrip())

    def parse(self):
        parsing = False
        capture = []
        indent = 0

        for line in self.document:
            if parsing:
                if line.strip() and self.get_indent(line) <= indent:
                    self._exec(''.join(capture))
                    capture = []
                    parsing = False
                    indent = 0
                else:
                    capture.append(line[indent:])
            elif self.FUNC_RGX.match(line):
                parsing = True
                indent = self.get_indent(line)
                capture.append(line.lstrip())

    def _exec(self, code):
        exec(code, globals(), globals())


ClipFunctionParser('../decipher_clips.vim').parse()
