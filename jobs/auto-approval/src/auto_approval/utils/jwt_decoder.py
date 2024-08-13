import json
import os
from urllib.request import urlopen

from jose import jwt


def get_jwks():
    """Fetch JWKS from the well-known configuration URL."""
    well_known_config_url = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    jsonurl = urlopen(well_known_config_url)
    well_known_config = json.loads(jsonurl.read().decode("utf-8"))
    jwks_uri = well_known_config["jwks_uri"]
    jsonurl = urlopen(jwks_uri)
    jwks = json.loads(jsonurl.read().decode("utf-8"))
    return jwks


def get_rsa_key(jwks, kid):
    """Return the matching RSA key for kid, from the jwks array."""
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    return None


def decode_token(token):
    """Decode the JWT token and return the payload."""
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError as e:
        raise Exception("Invalid header. Use an RS256 signed JWT Access Token") from e

    if unverified_header["alg"] == "HS256":
        raise Exception("Invalid header. Use an RS256 signed JWT Access Token")

    if "kid" not in unverified_header:
        raise Exception("Invalid header. No KID in token header")

    jwks = get_jwks()
    rsa_key = get_rsa_key(jwks, unverified_header["kid"])

    if not rsa_key:
        raise Exception("Unable to find jwks key referenced in token")

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[os.getenv("JWT_OIDC_ALGORITHMS")],
            audience=os.getenv("JWT_OIDC_AUDIENCE"),
            issuer=os.getenv("JWT_OIDC_ISSUER"),
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise Exception("Token has expired") from e
    except jwt.JWTClaimsError as e:
        raise Exception("Incorrect claims, please check the audience and issuer") from e
    except Exception as e:
        raise Exception("Unable to parse authentication token.") from e
