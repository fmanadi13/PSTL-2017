# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with creating headers and footers.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from pylatex.base_classes import Environment, ContainerCommand, Command
from pylatex.package import Package
from pylatex.utils import NoEscape


class Questions(Environment):
    r"""Allows the creation of new page styles."""

    _latex_name = "questions"

    packages = []

    def __init__(self, data=None, pos=None, **kwargs):

        super(Questions, self).__init__(data=data, options=pos,**kwargs)