from dataclasses import dataclass, InitVar, field
from io import BytesIO
from typing import Any

from minio import Minio


@dataclass
class MinioManager:
    minio_endpoint: InitVar[str]
    dict_settings: InitVar[dict[str, Any]]
    _client: Minio = field(init=False)
    _bucket_name: str = field(init=False)

    def __post_init__(self, minio_endpoint: str, dict_settings: dict[str, Any]) -> None:
        self._client = Minio(minio_endpoint,
                             access_key=dict_settings['access_key'],
                             secret_key=dict_settings['secret_key'],
                             secure=False
                             )
        self._bucket_name = dict_settings['bucket_name']
        self._generate_bucket()

    def _generate_bucket(self) -> None:
        found = self._client.bucket_exists(self._bucket_name)
        if not found:
            self._client.make_bucket(self._bucket_name)
            print(f'Created bucket `{self._bucket_name}`')
        else:
            print(f'Bucket `{self._bucket_name}`, already exists')

    def upload_file(self, local_file_path: str, distant_file_path: str) -> None:
        self._client.fput_object(
            self._bucket_name, distant_file_path, local_file_path,
        )
        print(f'Uploaded file `{local_file_path}` as object `{distant_file_path}` to bucket `{self._bucket_name}`')

    def upload_file_from_memory(self, file_name: str, image_size: int, image_data: BytesIO) -> None:
        v = self._client.put_object(
            self._bucket_name,
            file_name,
            image_data,
            image_size,
            content_type="image/jpeg"
        )
        print(v)
