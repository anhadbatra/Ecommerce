from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'  # Ensures all uploads go inside media/ folder
    default_acl = 'public-read'  # Makes uploaded files public
    file_overwrite = False  # Prevents overwriting files with the same name
