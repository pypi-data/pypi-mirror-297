from cbr_shared.aws.s3.S3__Key_Generator import S3__Key_Generator
from osbot_utils.utils.Misc             import random_guid


class S3__Key__Chat_Thread(S3__Key_Generator):
    use_request_path  : bool = False

    def create__for__llm_request(self, chat_thread_id=None, llm_request_id=None):
        path_elements = self.create_path_elements__from_when()

        if not chat_thread_id:
            chat_thread_id = random_guid()
        if not llm_request_id:
            llm_request_id = random_guid()

        path_elements.append(chat_thread_id)

        s3_key = self.create_s3_key(path_elements=path_elements, file_id=llm_request_id)
        return s3_key

