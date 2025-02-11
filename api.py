import base64
import hashlib
import hmac
import logging
import os
import re
import time
import urllib.parse
import uuid
from dotenv import load_dotenv
import requests

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DEVICE_IDENTIFIER = os.getenv("DEVICE_IDENTIFIER")
DEVICE_ID = os.getenv("DEVICE_ID")

COUNTRY = "es"
API_BASE = "https://app.idealista.com/api"
API_KEY = "5b85c03c16bbb85d96e232b112ee85dc"
CONSUMER_SECRET = "idea;andr01d"


def generate_signature(data: str, secret_key: str) -> str:
    # Convertir los datos a bytes
    data_bytes = data.encode('utf-8')
    secret_bytes = secret_key.encode('utf-8')

    # Crear una firma HMAC usando SHA256
    signature = hmac.new(secret_bytes, data_bytes, hashlib.sha256).hexdigest()
    return signature


def encode_params(params: dict) -> str:
    return urllib.parse.urlencode(sorted(params.items()))


def get_basic_auth(consumer_key, consumer_secret):
    url_encoded_consumer_key = urllib.parse.quote(consumer_key)
    url_encoded_consumer_secret = urllib.parse.quote(consumer_secret)

    combined = f"{url_encoded_consumer_key}:{url_encoded_consumer_secret}".encode()
    return base64.b64encode(combined).decode()


def get_timestamp_millis():
    return int(time.time() * 1000)


def md5_hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


class IdealistaClient:
    def __init__(self):
        self.authorization = ""
        self.expiration_date = 0
        self.token = ""

    def start(self):
        try:
            oauth = self._oauth()

            # Ensure the request was successful
            if oauth.status_code != 200:
                logging.error(f"OAuth request failed with status {oauth.status_code}: {oauth.text}")
                raise requests.HTTPError(f"OAuth request failed: {oauth.status_code}")

            # Attempt to parse JSON
            try:
                oauth_json = oauth.json()
            except ValueError as e:
                logging.error("Failed to parse OAuth response as JSON.")
                raise ValueError("Invalid JSON response from OAuth server.") from e

            # Validate required fields
            if not all(k in oauth_json for k in ["token_type", "access_token", "expires_in"]):
                logging.error(f"Missing expected keys in OAuth response: {oauth_json}")
                raise KeyError("OAuth response is missing required fields.")

            # Set token and expiration
            self.authorization = oauth_json["token_type"].capitalize() + " " + oauth_json["access_token"]
            expires_in = oauth_json["expires_in"]

            if not isinstance(expires_in, (int, float)) or expires_in <= 0:
                logging.error(f"Invalid expires_in value: {expires_in}")
                raise ValueError("Invalid expiration time received from OAuth.")

            self.expiration_date = time.time() + expires_in

        except requests.RequestException as e:
            logging.error("Network error during OAuth request.", exc_info=True)
            raise RuntimeError("Failed to complete OAuth request due to a network error.") from e

        except (KeyError, ValueError) as e:
            logging.error("Error processing OAuth response.", exc_info=True)
            raise RuntimeError("Failed to process OAuth response.") from e

        return oauth

    def sign_request(self, request: requests.Request) -> requests.Request:
        # if the url contains the country and does not match /api/([A-z]+)/login
        request.params['t'] = DEVICE_IDENTIFIER
        request.params['k'] = API_KEY
        if self.token and COUNTRY in request.url and not re.match(r"/api/([A-z]+)/login", request.url):
            timestamp = get_timestamp_millis()

            request.params['user'] = USER
            request.params['token'] = md5_hash(f"{self.token}{timestamp}")
            request.params['timestamp'] = timestamp

        # Obtener el tipo de método (GET o POST)
        is_get = request.method == 'GET'
        content_type = request.headers.get('Content-Type', '') or request.headers.get('content-type', '')
        # Determinar el tipo de cuerpo
        if is_get:
            body_type = 'QUERY_STRING'
        elif 'multipart' in content_type:
            body_type = 'BODY_PARAMS_B'
        elif 'json' in content_type:
            body_type = 'RAW'
        else:
            body_type = 'BODY_PARAMS_A'

        query_string = encode_params(request.params)
        body_string = encode_params(request.data) if not is_get and body_type not in ['BODY_PARAMS_B', 'RAW'] else ''

        # Generar un valor 'seed' aleatorio
        seed = str(uuid.uuid4())

        # Concatenar todos los componentes para generar la firma
        secret_key = base64.b64encode("mpTQnS88JtXD6d2E".encode('utf-8')).decode('utf-8')
        signature = generate_signature(f"{seed}{request.method}{query_string}{body_string}", secret_key)

        # Crear una nueva solicitud con las cabeceras 'Signature' y 'seed'
        request.headers['Signature'] = signature
        request.headers['seed'] = seed

        return request

    def _oauth(self):
        url = f"{API_BASE}/oauth/token"

        payload = {
            "grant_type": "client_credentials",
            "scope": "write"
        }
        headers = {
            "authorization": f"Basic {get_basic_auth(API_KEY, CONSUMER_SECRET)}",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; M2101K6G Build/TQ2A.230305.008.C1)",
            "app_version": "12.15.1",
            "device_identifier": DEVICE_IDENTIFIER,
            "content-type": "application/x-www-form-urlencoded",
        }

        return requests.post(url, data=payload, headers=headers)

    def exists(self, email: str):
        url = f"{API_BASE}/3/{COUNTRY}/user/exists"

        querystring = {
            "email": email,
        }

        headers = {
            "app_version": "12.15.1",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; M2101K6G Build/TQ2A.230305.008.C1)",
            "device_identifier": DEVICE_IDENTIFIER,
            "authorization": self.authorization,
            "host": "app.idealista.com",
            "connection": "Keep-Alive",
            "accept-encoding": "gzip"
        }

        request = requests.Request("GET", url, headers=headers, params=querystring)
        signed = self.sign_request(request)
        return requests.Session().send(signed.prepare())

    def _login(self, user, password):
        url = f"{API_BASE}/{COUNTRY}/login"

        payload = {
            "user": user,
            "pwd": password,
            "authenticationCode": "",
            "securityToken": "",
            "deviceId": DEVICE_ID
        }
        headers = {
            "app_version": "12.15.1",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; M2101K6G Build/TQ2A.230305.008.C1)",
            "device_identifier": DEVICE_IDENTIFIER,
            "authorization": self.authorization,
            "content-type": "application/x-www-form-urlencoded",
        }

        request = requests.Request("POST", url, headers=headers, data=payload)
        signed = self.sign_request(request)
        return requests.Session().send(signed.prepare())

    def login(self, user, password):
        r = self._login(user, password)
        self.token = r.json()["token"]
        return r

