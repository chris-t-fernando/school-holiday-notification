from .iparameter_store import IParameterStore

import boto3
from botocore.exceptions import ClientError


class Ssm(IParameterStore):
    def __init__(self):
        self.store = boto3.client("ssm")

    def put(
        self, path: str, value: str, field_type: str = "String", overwrite: bool = True
    ) -> dict:
        try:
            return self.store.put_parameter(
                Name=path, Value=value, Type=field_type, Overwrite=overwrite
            )
        except ClientError as e:
            raise

    def get(self, path: str, with_decryption: bool = True) -> dict:
        try:
            return self.store.get_parameter(Name=path, WithDecryption=with_decryption)["Parameter"][
                "Value"
            ]
        except ClientError as e:
            if e.response["Error"]["Code"] == "ParameterNotFound":
                return "[]"
            raise