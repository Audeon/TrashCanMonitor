from pydantic import Field, BaseModel, Extra, validator
from pydantic.typing import Optional
from enum import Enum


__all__ = ['ConfigForbidExtra', 'ConfigIgnoreExtra', 'ConfigAllowExtra']

class TransportEnum(Enum):
    api = "api"
    mongodb = "mongodb"
    csv = "csv"
    sql = "sql"

class ConfigFields:
    container_id = Field(description="")

    # Loging related fields.
    log_level = Field(default=10, description="The log level, using python standard log levels.")
    log_path = Field(default="./logs/", description="The storage location for this applications logs.")
    log_format = Field(default="%(asctime)s %(name)s %(levelname)s %(message)s",
                            description="Python standard logging string.")
    log_encoding = Field(default="utf-8", description="Encoding the logs will use.")
    log2console = Field(default=True, description="If the application should also send output to the stdout.")
    sleep_time = Field(default=60,
                       description="This is the time the application will pause between running test executions.")

    target_gateway_url = Field(default="http://192.168.12.1", description="This is the admin url for the modem.")
    transport = Field(description="This will change which the data will use.")

    # Mongo transport defaults.
    mongo_user = Field(description="The username you would use to authenticate with mongodb.")
    mongo_pw = Field(description="The password you would use to authenticate with mongodb.")
    mongo_host = Field(description="The host address of the mongodb.")
    mongo_port = Field(default=27017, description="The port mongodb will be assigned on the host.")
    mongo_auth = Field(description="The database the user is going to authenticate to.")
    mongo_db = Field(description="The database that should be used for storing data.")


class ConfigForbidExtra(BaseModel):
    """
        This model will handel validation of config input. Will raise validation error on extra fields in the
        configuration file.
    """
    transport: TransportEnum = ConfigFields.transport
    sleep_time: int = ConfigFields.sleep_time
    target_gateway_url: str = ConfigFields.target_gateway_url

    log_level: int = ConfigFields.log_level
    log_path: Optional[str] = ConfigFields.log_path
    log2console: Optional[bool] = ConfigFields.log2console
    log_format: Optional[str] = ConfigFields.log_format
    log_encoding: Optional[str] = ConfigFields.log_encoding

    mongo_user: Optional[str] = ConfigFields.mongo_user
    mongo_pw: Optional[str] = ConfigFields.mongo_pw
    mongo_host: Optional[str] = ConfigFields.mongo_host
    mongo_port: Optional[int] = ConfigFields.mongo_port
    mongo_auth: Optional[str] = ConfigFields.mongo_auth
    mongo_db: Optional[str] = ConfigFields.mongo_db

    class Config:
        extra=Extra.forbid



class ConfigIgnoreExtra(ConfigForbidExtra):
    """
    This class will ignore any extra fields in the config input.
    """
    class Config:
        extra=Extra.ignore


class ConfigAllowExtra(ConfigForbidExtra):
    """
    This class will allow any extra fields in the config input.
    """
    class Config:
        extra=Extra.allow
