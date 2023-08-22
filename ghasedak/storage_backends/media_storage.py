from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    BASE_LOCATION = "media"
    location = "media"
    file_overwrite = True
