"""Public interfaces"""

from zope.interface import Interface
from zope.schema import Dict


class IMonkeyPatchEvent(Interface):
    """Monkey patch applied event"""

    patch_info = Dict(
        title="Misc information about the patch",
        description="""A mapping about the patch with following keys:
        * 'description': A text that describes the monkey patch
        * 'zcml_info': A text about the ZCML portion that made the patch
        * 'original': Dotted name of the original method/function.
        * 'replacement': Dotted name of the new function
        """,
    )
