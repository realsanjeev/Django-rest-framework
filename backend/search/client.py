from algoliasearch_django import algolia_engine


def display_in_console(string):
    print("-"*10)
    print(string)
    print("-"*10)

def get_client():
    return algolia_engine.client

def get_index(index_name="server_Book"):
    client = get_client()
    index = client.init_index(index_name)
    # display_in_console(f"client: {client}")
    # search diretly from index `index.search(query='api')`
    return index

def perform_search(query, **kwargs):
    index = get_index()
    params = {}
    tags = ""
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        display_in_console(f"{tags}")
        if len(tags) != 0:
            params['tagFilters'] = tags
    results = index.search(query, params)
    return results