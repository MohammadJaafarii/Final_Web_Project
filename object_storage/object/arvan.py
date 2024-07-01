import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

def download_object(object_name,download_path_o='C:\\Users\\ok\\PycharmProjects\\final web\\Final_Web_Project\\download'):
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
            aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            # bucket
            bucket = s3_resource.Bucket('mohammadjafarimohammadmahdiketabchibucket')

            #object_name = 'object_name.txt'
            #download_path = '/the/abs/path/to/file.txt'
            download_path = f'{download_path_o}\\{object_name}'
            bucket.download_file(
                object_name,
                download_path
            )
            return True
        except ClientError as e:
            logging.error(e)
            return False



def deleteobject(object_name):
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
            aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            # bucket
            bucket_name = 'mohammadjafarimohammadmahdiketabchibucket'
            #object_name = 'object_name.txt'

            bucket = s3_resource.Bucket(bucket_name)
            object = bucket.Object(object_name)

            response = object.delete()
            return True
        except ClientError as e:
            logging.error(e)
            return False


def uploadobject(file_path,object_name):
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
            aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
        )
    except Exception as exc:
        logging.error(exc)

    else:
        try:
            bucket = s3_resource.Bucket('mohammadjafarimohammadmahdiketabchibucket')
            #file_path = 'the/abs/path/to/file.txt'
            #object_name = 'file.txt'

            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='public-read',
                    Body=file,
                    Key=object_name
                )
            return True
        except ClientError as e:
            logging.error(e)
            return False

def getallobject():
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
            aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
        )
    except Exception as exc:
        logging.error(exc)

    else:
        try:
            bucket_name = 'mohammadjafarimohammadmahdiketabchibucket'
            bucket = s3_resource.Bucket(bucket_name)

            for obj in bucket.objects.all():
                logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")
            return bucket.objects.all()

        except ClientError as e:
            logging.error(e)
#for check is bucket exist

# try:
#    s3_client = boto3.client(
#        's3',
#        endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
#        aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
#        aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
#    )
# except Exception as exc:
#    logging.error(exc)
#
# else:
#    try:
#        response = s3_client.head_bucket(Bucket="mohammadjafarimohammadmahdiketabchibucket")
#    except ClientError as err:
#        status = err.response["ResponseMetadata"]["HTTPStatusCode"]
#        errcode = err.response["Error"]["Code"]
#
#        if status == 404:
#            logging.warning("Missing object, %s", errcode)
#        elif status == 403:
#            logging.error("Access denied, %s", errcode)
#        else:
#            logging.exception("Error in request, %s", errcode)
#    else:
#        print(response)


#for create bucket
# try:
#    s3_client  = boto3.resource(
#        's3',
#        endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
#        aws_access_key_id='d8cfa58a-7deb-4bfe-952e-3e108920b3d8',
#        aws_secret_access_key='d3c6a0ea3addcbe417eec5edecbfffa5c6a15bf80dabc9374acaa1ef2c628be5'
#    )
# except Exception as exc:
#    logging.info(exc)
# else:
#    try:
#        bucket_name = 'mohammadjafarimohammadmahdiketabchibucket'
#        bucket = s3_resource.Bucket(bucket_name)
#        bucket.create(ACL='public-read') # ACL='private'|'public-read'
#    except ClientError as exc:
#        logging.error(exc)

