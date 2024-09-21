from cbr_shared.aws.s3.S3__Key_Generator import S3__Key_Generator
from osbot_utils.utils.Misc             import random_guid



class S3__Key__Chat_Thread(S3__Key_Generator):
    use_request_path  : bool = False

    def create(self, when=None, request_id=None, request_path=None):
        path_elements = self.create_path_elements__from_when(when=when)

        if not request_id:
            request_id = random_guid()

        if self.use_request_path:
            if request_path:
                if request_path == '/':
                    request_path = '(root)'                                      # todo: see implications of this (since boto3 on AWS handles this ok, but minio doesn't like a / as the path
                else:
                    request_path = request_path[1:]
                if request_path:
                    path_elements.append(request_path)


        s3_key = self.create_s3_key(path_elements=path_elements, file_id=request_id)
        return s3_key

