# -*- coding: utf-8 -*-
# $Id$
"""ZMI control panel"""

import Acquisition
from Globals import InitializeClass
from OFS import SimpleItem
from App.ApplicationManager import Fake, ApplicationManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from meta import all_patches

class ControlPanel(Fake, SimpleItem.Item, Acquisition.Implicit):
    """The Monkey patches control panel"""

    id = 'collective_monkeypatcher'
    name = title = "Monkey Patches"
    meta_type = "Monkey patches control panel"
    icon = 'p_/DebugManager_icon' # FIXME: Use another one ?
    manage_main = PageTemplateFile('zmi/controlpanel.pt', globals())

    manage_options=((
        {'label': 'Monkey patches', 'action': 'manage_main'},
        ))

    def getId(self):
        return self.id

    def allPatches(self):
        return all_patches

InitializeClass(ControlPanel)
