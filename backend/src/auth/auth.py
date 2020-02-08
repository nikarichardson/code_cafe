import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# pip install python-jose 
# http://localhost:8100/

AUTH0_DOMAIN = 'coffeeshopfnsd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drink'

## AuthError Exception

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError():
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

        abort(status_code)


## Auth Header

'''
Obtains the access token from the authorization header. Tries to get the header 
from the request and returns an error if no header is present. If the header is malformed,
an authorization error is returned. 
'''
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        return AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
        

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        return AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        return AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        return AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

'''
Checks that the required permission is included in the payload. Returns an authorization error if 
permissions are not included or if the desired permission itself is not included in the payload. 
'''
def check_permissions(permission, payload):
    #print("inside permissions")
    #for x in payload['permissions']:
    #    print(x) 
    print('permissions' not in payload)
    if 'permissions' not in payload:
        return AuthError({
            'success': False,
            'code': 'missing_header',
            'description': 'Permissions header is missing.'
        }, 403)
    if permission not in payload['permissions']:
        return AuthError({
            'success': False,
            'code': 'missing_permission',
            'description': 'User does not have this permission.'
        }, 401)
    else:
        return True 

'''
Takes a json web token and verifies that it is an Auth0 token with key id with Autho0, decodes the payload
from the token, validates the claims, and returns the decoded payload.  
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        return AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            return AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            return AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            return AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    return AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

"""
Uses the get_token_auth_header method to get the token. Uses the verify_decode_jwt method to decode the jwt.
Validates claims with the check_permissions method and returns the decorator. 
"""
def requires_auth(permission=''): # default to empty string, will be 
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            print("here")
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator 