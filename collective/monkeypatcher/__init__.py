# -*- coding: utf-8 -*-
# $Id$
"""collective.monkeypatcher"""

from controlpanel import ControlPanel

def initialize(context):
    """Zope 2 registration"""

    # FIXME: somehow dirty way to get the control panel. Something cleaner available around?
    zope_control_panel = context._ProductContext__app.Control_Panel
    cp_id = ControlPanel.id
    if cp_id not in zope_control_panel.objectIds():
        control_panel = ControlPanel()
        zope_control_panel._setObject(cp_id, control_panel)
    return
