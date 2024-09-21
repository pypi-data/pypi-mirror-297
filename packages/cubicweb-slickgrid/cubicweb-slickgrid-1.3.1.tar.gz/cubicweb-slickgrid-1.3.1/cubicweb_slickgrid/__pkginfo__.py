# pylint: disable=W0622
#
# copyright 2003-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
#
# Developped by Logilab S.A. (Paris, FRANCE) https://www.logilab.fr
#
"""cubicweb-slickgrid application packaging information"""

from os.path import dirname, join


modname = "slickgrid"
distname = f"cubicweb-{modname}"

# Version lives in a dedicated file to ease automation.
with open(join(dirname(__file__), "VERSION")) as f:
    version = f.readline().strip()
numversion = tuple(int(num) for num in version.split(".")[:3])

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Table view rendered using the SlickGrid_ JavaScript library."
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 3.38.16, < 5.0.0",
    "cubicweb-web": ">= 0.1.3, < 2.0.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]
