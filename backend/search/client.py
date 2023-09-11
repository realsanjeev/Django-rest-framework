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
    '''
    
    Perform Complex search
    perform_search(query=query, tags=tags, public=True)
    '''
    index = get_index()
    params = {}
    tags = ""
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params['tagFilters'] = tags
    index_filters = [f"{k}:{v}" for k, v in kwargs.items()]
    if len(index_filters) != 0:
        params["facetFilters"] = index_filters
    display_in_console(f"{params}")
    results = index.search(query, params)
    print(results["hits"])
    return results
