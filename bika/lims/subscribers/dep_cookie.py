# -*- coding: utf-8 -*-
#
# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

from plone import api
from bika.lims import logger


def SetDepartmentCookies(event):
    """Login event handler.
    When user logs in for the first time, we are setting department filtering cookie values.
    """

    # Fix for https://jira.bikalabs.com/browse/LIMS-2597
    if not is_bika_installed():
        logger.warn("Package 'bika.lims' is not installed, skipping event handler for IUserLoggedInEvent.")
        return

    # get the bika_setup object
    portal = api.portal.get()
    bika_setup = portal.get("bika_setup")

    # just to be sure...
    # This should go into the api.py module once it is in place
    if bika_setup is None:
        raise RuntimeError("bika_setup not found in this Bika LIMS installation")

    # Getting request, response and username
    request = api.env.getRequest()
    response = request.RESPONSE

    user = api.user.get_current()
    username = user and user.getUserName() or None
    portal_catalog = api.portal.get_tool("portal_catalog")

    if bika_setup.getAllowDepartmentFiltering():
        dep_for_cookie = ''

        if username == 'admin':
            departments = portal_catalog(portal_type='Department',
                                         sort_on='sortable_title',
                                         sort_order='ascending',
                                         inactive_state='active')

            for department in departments:
                dep_for_cookie += department.UID + ','

            response.setCookie('dep_filter_disabled', 'true', path='/', max_age=24 * 3600)
        else:
            labcontact = portal_catalog(portal_type='LabContact', getUsername=username)
            if labcontact:
                departments = labcontact[0].getObject().getSortedDepartments()
                dep_for_cookie = departments[0].UID() if len(departments) > 0 else ''

        response.setCookie('filter_by_department_info', dep_for_cookie, path='/', max_age=24 * 3600)
    else:
        response.setCookie('filter_by_department_info', None, path='/', max_age=0)
        response.setCookie('dep_filter_disabled', None, path='/', max_age=0)


def ClearDepartmentCookies(event):
    """Logout event handler.
    When user explicitly logs out from the Logout menu, clean department filtering related cookies.
    """

    if not is_bika_installed():
        logger.warn("Package 'bika.lims' is not installed, skipping event handler for IUserLoggedOutEvent.")
        return

    request = api.env.getRequest()
    response = request.RESPONSE

    # Voiding our special cookie on logout
    response.setCookie('filter_by_department_info', None, path='/', max_age=0)
    response.setCookie('dep_filter_disabled', None, path='/', max_age=0)


def is_bika_installed():
    """Check if Bika LIMS is installed in the Portal
    """
    qi = api.portal.get_tool("portal_quickinstaller")
    return qi.isProductInstalled("bika.lims")
