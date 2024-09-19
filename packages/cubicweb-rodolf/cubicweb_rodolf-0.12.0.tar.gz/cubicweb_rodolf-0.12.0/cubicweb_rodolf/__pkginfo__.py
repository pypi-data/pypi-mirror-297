"""cubicweb-rodolf application packaging information"""

modname = "cubicweb_rodolf"
distname = "cubicweb-rodolf"

numversion = (0, 12, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "RDF data production monitoring (RODOLF)"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/rodolf"

__depends__ = {
    "cubicweb[postgresql,s3]": ">= 4.6.3,< 5.0.0",
    "cubicweb-api": ">= 0.15.0,< 0.16.0",
    "cubicweb-file": ">= 4.1.0, < 5.0.0",
    "cubicweb-oauth2": None,
    "rql": ">= 0.43.2, < 1.0.0",
    "cubicweb-rq": None,
    "cubicweb-s3storage": None,
    "requests": None,
    "pyshacl": None,
    "Jinja2": None,
    "rdf-data-manager": None,
    "tqdm": None,
    "pyyaml": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
