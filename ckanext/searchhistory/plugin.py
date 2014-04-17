import ckan.plugins as p
import ckan.plugins.toolkit as tk

import actions
import auth

class SearchHistoryPlugin(p.SingletonPlugin):
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    # Override package_search with for_view and if logged in user

    def get_actions(self):
        return {
            'ckanext_search_history_list': actions.search_list,
            'ckanext_search_history_add': actions.search_add,
        }

    def get_auth_functions(self):
        return {
            'ckanext_search_history_list': auth.search_list,
            'ckanext_search_history_add': auth.search_add,
        }
