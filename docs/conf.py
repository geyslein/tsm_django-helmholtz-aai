# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import inspect

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
from typing import Optional

import django
from sphinx.ext import apidoc

import django_helmholtz_aai

sys.path.insert(0, os.path.abspath(".."))
if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "testproject.settings"
django.setup()


def generate_apidoc(app):
    appdir = Path(app.__file__).parent
    apidoc.main(
        ["-fMEeTo", str(api), str(appdir), str(appdir / "migrations" / "*")]
    )


api = Path("api")

if not api.exists():
    generate_apidoc(django_helmholtz_aai)

# -- Project information -----------------------------------------------------

project = "django-helmholtz-aai"
copyright = "2022, Helmholtz-Zentrum Hereon"
author = "Philipp S. Sommer, Housam Dibeh, Hatef Takyar"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "autodocsumm",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "autodocsumm",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinxcontrib_django",
    "sphinxarg.ext",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


autodoc_default_options = {
    "show_inheritance": True,
    "members": True,
    "autosummary": True,
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "collapse_navigation": False,
    "includehidden": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "django": ("https://django.readthedocs.io/en/stable/", None),
}


def group_models(app, what, name, obj, section, parent) -> Optional[str]:
    """Group django models."""
    if inspect.isclass(obj) and issubclass(obj, django.db.models.Model):
        return "Models"
    if (
        inspect.isclass(parent)
        and issubclass(parent, django.db.models.Model)
        and any(field.name == name for field in parent._meta.fields)
    ):
        return "Model Fields"


def setup(app):
    app.connect("autodocsumm-grouper", group_models)
    app.add_crossref_type(
        directivename="signal",
        rolename="signal",
        indextemplate="pair: %s; signal",
    )
