import ckan.plugins as p
import ckan.plugins.toolkit as tk

class SearchHistoryPlugin(p.SingletonPlugin):
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
