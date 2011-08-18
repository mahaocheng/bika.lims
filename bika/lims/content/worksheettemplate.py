from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_inner
from Products.ATExtensions.field.records import RecordsField
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.widgets import ServicesWidget
from bika.lims.browser.widgets import WorksheetTemplateLayoutWidget
from bika.lims.config import ANALYSIS_TYPES, I18N_DOMAIN, PROJECTNAME
from bika.lims.content.bikaschema import BikaSchema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bika')

schema = BikaSchema.copy() + Schema((
    RecordsField('Row',
        required = 1,
        type = 'templateposition',
        subfields = ('pos', 'type', 'sub', 'dup'),
        required_subfields = ('pos', 'type'),
        subfield_labels = {'pos': 'Position',
                           'type': 'Type',
                           'sub': 'Subtype',
                           'dup': 'Duplicate Of'},
        widget = WorksheetTemplateLayoutWidget(
            label = 'Worksheet Layout',
            label_msgid = 'label_positions',
            i18n_domain = I18N_DOMAIN,
        )
    ),
    ReferenceField('Service',
        required = 1,
        multiValued = 1,
        allowed_types = ('AnalysisService',),
        relationship = 'WorksheetTemplateAnalysisService',
        referenceClass = HoldingReference,
        widget = ServicesWidget(
            label = 'Analysis service',
            label_msgid = 'label_analysis',
            i18n_domain = I18N_DOMAIN,
        )
    ),
))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True

class WorksheetTemplate(BaseContent, HistoryAwareMixin):
    security = ClassSecurityInfo()
    schema = schema

    security.declarePublic('getAnalysisTypes')
    def getAnalysisTypes(self):
        """ return Analysis type displaylist """
        return ANALYSIS_TYPES

registerType(WorksheetTemplate, PROJECTNAME)
