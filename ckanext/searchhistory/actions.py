import datetime
import json
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
import ckan.new_authz as new_authz

import db


def _convert_to_json(key, data, errors, context):
    params_dict = data.get(key, [])
    data[key] = json.dumps(params_dict)


schema_add = {
    'id': [tk.get_validator('ignore_empty'), unicode],
    'params': [tk.get_validator('ignore_missing'), _convert_to_json],
    'user_id': [tk.get_validator('ignore_missing'), unicode],
    'created': [tk.get_validator('ignore')],
}

def search_add(context, data_dict):
    '''
    Add an item to the search_history for the current user.

    :param params: Search query to add to history
    :type params: string
    '''
    tk.check_access('search_history_add', context, data_dict)
    if db.search_history_table is None:
        db.init_db(context['model'])

    data, errors = df.validate(data_dict, schema_add, context)

    username = context.get('user')
    user_id = new_authz.get_user_id_for_username(username, allow_none=False)

    search_history = db.SearchHistory()
    search_history.content = data.get('params')
    search_history.user_id = user_id
    session = context['session']
    session.add(search_history)
    session.commit()
    return db.table_dictize(search_history, context)


@tk.side_effect_free
def search_list(context, data_dict):
    '''
    List the search history

    :param limit: The number of items to show (optional, default: 10)
    :type limit: int
    '''
    if db.search_history_table is None:
        db.init_db(context['model'])

    tk.check_access('search_history_list', context, data_dict)

    username = context.get('user')
    user = new_authz.get_user_id_for_username(username, allow_none=False)
    # Get the limit and put a hard upper limit on it
    limit = data_dict.get('limt', 10)
    if limit > 25:
        limit = 25

    history = db.SearchHistory.search_history(user_id=user, limit=limit)
    result = []
    if history:
        for item in history:
            data_dict = db.table_dictize(item, context)
            params = data_dict.pop('content')
            data_dict['params'] = json.loads(params)
            result.append(data_dict)
    return result
