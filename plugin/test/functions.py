# -*- coding: utf-8 -*-
import os
import sys
import re
import string
from urllib import quote

sys.path.append('plugin/decipherclips')
import decipherclips


FUNCTION_DEPS = (os, string.uppercase, string.lowercase, quote, decipherclips)


class ClipParserException(Exception):
    pass


class ClipFunctionParser(object):
    """Parses and compiles python functions from the vim plugin placing them in the global namespace"""
    FUNC_RGX = re.compile(r'\s*def ([A-Z].*?)\(.*')  # testable funcs are capitalized

    def __init__(self, clip_path):
        try:
            self.clip_lines = open(clip_path).readlines()
        except IOError:
            raise ClipParserException('Could not read plugin: {path}'.format(path=clip_path))

    def get_indent(self, s):
        """Used to keep track of scope via white space

        :param s:
        :return: :rtype: int
        """
        return len(s) - len(s.lstrip())

    def parse(self):
        parsing = False
        capture = []
        indent = 0

        for line in self.clip_lines:
            if parsing:
                if line.strip() and self.get_indent(line) <= indent:
                    self._exec(''.join(capture))
                    parsing = False
                    capture = []
                    indent = 0
                else:
                    capture.append(line[indent:])
            elif self.FUNC_RGX.match(line):
                parsing = True
                indent = self.get_indent(line)
                capture.append(line.lstrip())

    def _exec(self, code):
        exec(code, globals(), globals())


ClipFunctionParser('plugin/decipher_clips.vim').parse()
