import datetime

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
import ckan.new_authz as new_authz

import db


schema = {
    'id': [tk.get_validator('ignore_empty'), unicode],
    'content': [tk.get_validator('ignore_missing'), unicode],
    'user_id': [tk.get_validator('ignore_missing'), unicode],
    'created': [tk.get_validator('ignore_missing'),
                tk.get_validator('isodate')],
}


def _search_add(context, data_dict):
    pass


def _search_list(context, data_dict):
    if db.search_history_table is None:
        db.init_db(context['model'])
    user_dict = context['user']
    user = new_authz.get_user_id_for_username(user, allow_none=False)
    limit = data_dict.get('limt')
    out = db.SearchHistory.search_history(user=user, limit=limit)
    if out:
        out = db.table_dictize(out, context)
    return out


def search_add(context, data_dict):
    '''
    Add an item to the search_history for the current user.

    :param content: Search query to add to history
    :type content: string
    '''
    try:
        tk.check_access('ckanext_search_history_add', context, data_dict)
    except tk.NotAuthorized:
        tk.abort(401, tk._('Not authorized to add history item'))
    return _search_add(context, data_dict)


def search_list(context, data_dict):
    '''
    List the search history

    :param limit: The number of items to show (optional, default: 10)
    :type limit: int
    '''
    try:
        tk.check_access('ckanext_search_history_list', context, data_dict)
    except tk.NotAuthorized:
        tk.abort(401, tk._('Not authorized to view history item'))
    return _search_list(context, data_dict)
