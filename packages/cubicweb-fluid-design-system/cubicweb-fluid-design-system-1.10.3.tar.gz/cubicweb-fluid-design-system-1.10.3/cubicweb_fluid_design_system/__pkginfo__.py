# pylint: disable=W0622
"""cubicweb-fluid-design-system application packaging information"""

modname = "fluid_design_system"
distname = "cubicweb-fluid-design-system"

numversion = (1, 10, 3)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "CubicWeb's cube used to manage the ENGIE's Fluid Design System"
web = "https://github.tools.digital.engie.com/GBSEngieDigitalNemoOpti/cubicweb-fds"

__depends__ = {
    "cubicweb": ">= 3.38.16, < 5.0.0",
    "cubicweb-web": ">= 0.1.3, < 2.0",
    "webtest": "",
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
