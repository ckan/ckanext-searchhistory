import ckan.plugins as p
import ckan.plugins.toolkit as tk

class SearchHistoryPlugin(p.SingletonPlugin):
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    # Override package_search with for_view and if logged in user

    def get_actions(self):
        return {
            'ckanext_searchhistory_list': actions.search_list,
            'ckanext_searchhistory_add': actions.search_add,
        }

    def get_auth_functions(self):
        return {
            'ckanext_searchhistory_list': auth.search_list,
            'ckanext_searchhistory_add': auth.search_add,
        }
