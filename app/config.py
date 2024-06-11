from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    genapi_key: str
    firebase_type: str
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    firebase_auth_uri: str
    firebase_token_uri: str
    firebase_auth_provider_x509_cert_url: str
    firebase_client_x509_cert_url: str
    firebase_universe_domain: str
    firebase_storage_bucket: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
