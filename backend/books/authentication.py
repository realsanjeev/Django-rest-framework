from rest_framework.authentication import TokenAuthentication as BaseAuth

class TokenAuthentication(BaseAuth):
    # In header change keyword
    # Authentication Bearer `Token`
    keyword = "Bearer"