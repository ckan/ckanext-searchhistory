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

    def after_search(self, search_results, search_params):
        context = {}
        q = search_params.get('q')
        fq = search_params.get('fq')

        try:
            tk.c.user
        except TypeError:
            # Web context not ready, eg paster command
            return search_results

        if (tk.c and tk.c.user and tk.c.controller == 'package'
                and tk.c.action == 'search' and
                ((q is not None and not q in ('', '*:*'))
                or '+dataset_type:dataset' not in fq[0])):
            data_dict = {'params': search_params}
            result = tk.get_action('search_history_add')(context, data_dict)
            print result
        return search_results
