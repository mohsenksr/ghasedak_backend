from decouple import config

SECRET_API_KEY_TOKEN = config('SECRET_API_KEY_TOKEN', '')
CLIENT_URL = config('CLIENT_URL', default='')
IN_APP_LOG_LEVEL = int(config('LOG_LEVEL', default=3))
PROJECT_NAME = config('APP_BASE_NAME', 'ghasedak')
SIGN_UP_TOKEN_EXPIRE_TIME = config('SIGN_UP_TOKEN_EXPIRE_TIME', default=60 * 60 * 2, cast=int)
SIGN_UP_TOKEN_PREFIX = 'signup_token_'
FORGET_PASSWORD_TOKEN_PREFIX = 'forget_token_'
PHONE_REGEX_PATTERN = '^(09)[0-9]{9}$'
HOME_PHONE_REGEX_PATTERN = '^(0)[0-9]{10}$'
HEX_COLOR_REGEX_PATTERN = '^#[0-9a-fA-F]{6}$'
