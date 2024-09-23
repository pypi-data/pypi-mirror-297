from flask_cognito_lib_custom.config import Config
from flask_cognito_lib_custom.services.cognito_svc import CognitoService
from flask_cognito_lib_custom.services.token_svc import TokenService


def cognito_service_factory(cfg: Config):
    return CognitoService(cfg=cfg)


def token_service_factory(cfg: Config):
    return TokenService(cfg=cfg)
