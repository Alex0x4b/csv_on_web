from pathlib import Path

from pkg_resources import resource_filename
PATH_TO_PKG = Path(resource_filename(__name__, "/"))

# module level doc-string
__docformat__ = "restructuredtext"
__doc__ = """
Read CSV from a web browser
===========================
"""
