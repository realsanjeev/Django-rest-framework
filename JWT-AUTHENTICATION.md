## JWT
JSON Web Token is a fairly new standard which can be used for token-based authentication. Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. 

#### Add in list of authentication classes in `settings.py`
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
```

**Customizing Authentication Header Type:**

To modify the header type, navigate to the `SIMPLE_JWT` section in your `settings.py` file. Adjust the `AUTH_HEADER_TYPES` parameter as needed.

**Note:**
Ensure that the header type is correctly specified in the `authenticated` section of your code. Also watch the `DEFAULT_PERMISSION_CLASSES` in `settings.py` for which permission is given.

```python
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(seconds=30),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1)
}
```
- `AUTH_HEADER_TYPES`: This defines the authentication header type expected by the JWT library, and it's set to use "Bearer" tokens. In JWT-based authentication, the "Bearer" keyword is typically used in the Authorization header to specify the type of token being presented.

- `ACCESS_TOKEN_LIFETIME`: This sets the lifetime or expiration time for access tokens to 30 seconds. Access tokens are short-lived tokens used for authentication and authorization purposes.

- `REFRESH_TOKEN_LIFETIME`: This sets the lifetime or expiration time for refresh tokens to 1 day. Refresh tokens are typically longer-lived tokens that are used to obtain new access tokens when they expire without requiring the user to log in again.

To decode jwt: `https://jwt.io/`

## JS Client
To run html in specific port 
```bash
python -m http.server 3000
```

## CORSHEADERS in Django project
```python
# example.com/api/<replative path>
CORS_URLS_REGEX = r"^/api/.*"
CORS_ALLOWED_ORIGINS = []
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "https://localhost:3000",
    ]
```

In middleware add:
```python
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    ...]
```