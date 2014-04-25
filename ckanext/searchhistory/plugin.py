import ckan.plugins as p
import ckan.plugins.toolkit as tk

import actions
import auth

class SearchHistoryPlugin(p.SingletonPlugin):
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
    p.implements(p.IPackageController, inherit=True)

    # Override package_search with for_view and if logged in user

    def get_actions(self):
        return {
            'search_history_list': actions.search_list,
            'search_history_add': actions.search_add,
        }

    def get_auth_functions(self):
        return {
            'search_history_list': auth.search_list,
            'search_history_add': auth.search_add,
        }

    def before_search(self, search_params):
        context = {}
        if search_params.get('q') and tk.c.user:
            data_dict = {'content': search_params.get('q')}
            result = tk.get_action('search_history_add')(context, data_dict)
            print result
        return search_params
