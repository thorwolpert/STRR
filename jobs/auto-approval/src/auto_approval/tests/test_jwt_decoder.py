import json
import unittest
from unittest.mock import MagicMock, patch

from jose import jwk, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from auto_approval.utils.jwt_decoder import decode_token, get_jwks, get_rsa_key


class TestJWTFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "kid": "1",
                    "use": "sig",
                    "n": "mock_modulus",
                    "e": "mock_exponent",
                }
            ]
        }
        self.mock_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    @patch("os.getenv")
    @patch("auto_approval.utils.jwt_decoder.urlopen")
    def test_get_jwks(self, mock_urlopen, mock_getenv):
        mock_getenv.return_value = (
            "https://example.com/.well-known/openid-configuration"
        )

        mock_responses = {
            "https://example.com/.well-known/openid-configuration": MagicMock(
                read=lambda: json.dumps(
                    {"jwks_uri": "https://example.com/jwks"}
                ).encode("utf-8")
            ),
            "https://example.com/jwks": MagicMock(
                read=lambda: json.dumps(self.mock_jwks).encode("utf-8")
            ),
        }

        def side_effect(url):
            if url in mock_responses:
                return mock_responses[url]
            raise urllib.error.URLError(f"Mocked URL not found: {url}")

        mock_urlopen.side_effect = side_effect

        jwks = get_jwks()
        self.assertIsInstance(jwks, dict)
        self.assertIn("keys", jwks)
        self.assertEqual(len(jwks["keys"]), 1)

        mock_urlopen.assert_any_call(
            "https://example.com/.well-known/openid-configuration"
        )
        mock_urlopen.assert_any_call("https://example.com/jwks")

    def test_get_rsa_key(self):
        rsa_key = get_rsa_key(self.mock_jwks, "1")
        self.assertIsInstance(rsa_key, dict)
        self.assertEqual(rsa_key["kid"], "1")

        rsa_key = get_rsa_key(self.mock_jwks, "2")
        self.assertIsNone(rsa_key)

    @patch("os.getenv")
    @patch("jose.jwt.decode")
    @patch("auto_approval.utils.jwt_decoder.get_jwks")
    @patch("jose.jwt.get_unverified_header")
    def test_decode_token(
        self, mock_get_unverified_header, mock_get_jwks, mock_jwt_decode, mock_getenv
    ):
        mock_getenv.side_effect = lambda key, default=None: {
            "JWT_OIDC_WELL_KNOWN_CONFIG": "https://example.com/.well-known/openid-configuration",
            "JWT_OIDC_ALGORITHMS": "RS256",
            "JWT_OIDC_AUDIENCE": "account-services",
            "JWT_OIDC_ISSUER": "https://example.com",
        }.get(key, default)

        mock_get_unverified_header.return_value = {"alg": "RS256", "kid": "1"}
        mock_get_jwks.return_value = self.mock_jwks
        mock_payload = {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
        mock_jwt_decode.return_value = mock_payload

        payload = decode_token(self.mock_token)
        self.assertEqual(payload, mock_payload)

    @patch("jose.jwt.get_unverified_header")
    def test_decode_token_invalid_algorithm(self, mock_get_unverified_header):
        mock_get_unverified_header.return_value = {"alg": "HS256", "kid": "1"}

        with self.assertRaises(Exception) as context:
            decode_token(self.mock_token)
        self.assertTrue(
            "Invalid header. Use an RS256 signed JWT Access Token"
            in str(context.exception)
        )

    @patch("jose.jwt.get_unverified_header")
    def test_decode_token_missing_kid(self, mock_get_unverified_header):
        mock_get_unverified_header.return_value = {"alg": "RS256"}

        with self.assertRaises(Exception) as context:
            decode_token(self.mock_token)
        self.assertTrue(
            "Invalid header. No KID in token header" in str(context.exception)
        )

    @patch("os.getenv")
    @patch("jose.jwt.decode")
    @patch("auto_approval.utils.jwt_decoder.get_jwks")
    @patch("jose.jwt.get_unverified_header")
    def test_decode_token_expired(
        self, mock_get_unverified_header, mock_get_jwks, mock_jwt_decode, mock_getenv
    ):
        mock_getenv.side_effect = lambda key, default=None: {
            "JWT_OIDC_WELL_KNOWN_CONFIG": "https://example.com/.well-known/openid-configuration",
            "JWT_OIDC_ALGORITHMS": "RS256",
            "JWT_OIDC_AUDIENCE": "account-services",
            "JWT_OIDC_ISSUER": "https://example.com",
        }.get(key, default)

        mock_get_unverified_header.return_value = {"alg": "RS256", "kid": "1"}
        mock_get_jwks.return_value = self.mock_jwks
        mock_jwt_decode.side_effect = ExpiredSignatureError()

        with self.assertRaises(Exception) as context:
            decode_token(self.mock_token)
        self.assertTrue("Token has expired" in str(context.exception))

    @patch("os.getenv")
    @patch("jose.jwt.decode")
    @patch("auto_approval.utils.jwt_decoder.get_jwks")
    @patch("jose.jwt.get_unverified_header")
    def test_decode_token_invalid_claims(
        self, mock_get_unverified_header, mock_get_jwks, mock_jwt_decode, mock_getenv
    ):
        mock_getenv.side_effect = lambda key, default=None: {
            "JWT_OIDC_WELL_KNOWN_CONFIG": "https://example.com/.well-known/openid-configuration",
            "JWT_OIDC_ALGORITHMS": "RS256",
            "JWT_OIDC_AUDIENCE": "account-services",
            "JWT_OIDC_ISSUER": "https://example.com",
        }.get(key, default)

        mock_get_unverified_header.return_value = {"alg": "RS256", "kid": "1"}
        mock_get_jwks.return_value = self.mock_jwks
        mock_jwt_decode.side_effect = JWTClaimsError()

        with self.assertRaises(Exception) as context:
            decode_token(self.mock_token)
        self.assertTrue(
            "Incorrect claims, please check the audience and issuer"
            in str(context.exception)
        )

    @patch("os.getenv")
    @patch("jose.jwt.decode")
    @patch("auto_approval.utils.jwt_decoder.get_jwks")
    @patch("jose.jwt.get_unverified_header")
    def test_decode_token_unable_to_parse(
        self, mock_get_unverified_header, mock_get_jwks, mock_jwt_decode, mock_getenv
    ):
        mock_getenv.side_effect = lambda key, default=None: {
            "JWT_OIDC_WELL_KNOWN_CONFIG": "https://example.com/.well-known/openid-configuration",
            "JWT_OIDC_ALGORITHMS": "RS256",
            "JWT_OIDC_AUDIENCE": "account-services",
            "JWT_OIDC_ISSUER": "https://example.com",
        }.get(key, default)

        mock_get_unverified_header.return_value = {"alg": "RS256", "kid": "1"}
        mock_get_jwks.return_value = self.mock_jwks
        mock_jwt_decode.side_effect = Exception("Random error")

        with self.assertRaises(Exception) as context:
            decode_token(self.mock_token)
        self.assertTrue(
            "Unable to parse authentication token." in str(context.exception)
        )
