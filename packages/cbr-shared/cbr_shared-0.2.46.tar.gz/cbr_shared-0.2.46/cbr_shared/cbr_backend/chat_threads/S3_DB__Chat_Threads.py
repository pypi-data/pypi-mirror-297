from cbr_shared.aws.s3.S3_DB__CBR                                   import S3_DB__CBR
from cbr_shared.cbr_backend.chat_threads.S3__Key__Chat_Thread import S3__Key__Chat_Thread
from cbr_shared.cbr_backend.server_requests.S3__Key__Server_Request import S3__Key__Server_Request
from cbr_shared.schemas.base_models.chat_threads.LLMs__Chat_Completion import LLMs__Chat_Completion
from osbot_utils.helpers.Random_Guid import Random_Guid
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import gz_to_json, json_parse
from osbot_utils.utils.Misc import timestamp_utc_now
from osbot_utils.utils.Status import status_ok, status_error

S3_BUCKET_SUFFIX__CHAT_THREADS    = 'chat-threads'
CHAT__REQUEST_TYPE__USER_REQUEST  = 'user-request'
CHAT__REQUEST_TYPE__USER_RESPONSE = 'user-response'
CHAT__REQUEST_TYPE__LLM_REQUEST   = 'llm-request'
CHAT__REQUEST_TYPE__LLM_RESPONSE  = 'llm-response'

class S3_DB__Chat_Threads(S3_DB__CBR):
    bucket_name__suffix   : str = S3_BUCKET_SUFFIX__CHAT_THREADS
    save_as_gz            : bool = True
    s3_key_generator      : S3__Key__Chat_Thread         # todo: change to a __Chat_Threads specific key model


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.s3_key_generator as _:
            _.root_folder      = S3_BUCKET_SUFFIX__CHAT_THREADS
            _.save_as_gz       = self.save_as_gz
            _.server_name      = self.server_name
            _.use_hours        = True
            _.use_minutes      = False
            _.use_request_path = False

    def s3_key(self, **kwargs):
        s3_key = self.s3_key_generator.create__for__llm_request(**kwargs)
        return s3_key

    def save_chat_completion__user_response(self, llm_chat_completion: LLMs__Chat_Completion, request_id: str):
        request_type   = CHAT__REQUEST_TYPE__USER_RESPONSE
        chat_thread_id = llm_chat_completion.chat_thread_id
        llm_request_id = request_id
        s3_key         = self.s3_key(chat_thread_id=chat_thread_id, llm_request_id=llm_request_id, request_type=request_type)
        data           = llm_chat_completion.model_dump()
        metadata       = { 'will': 'go here'}
        if self.s3_save_data(data=data, s3_key=s3_key, metadata=metadata):
            return status_ok(data={'llm_request_id': llm_request_id, 's3_key':s3_key})
        return status_error(message="s3 save data failed")

    def save_chat_completion__user_request(self, llm_chat_completion: LLMs__Chat_Completion, request_id: str):
        request_type   = CHAT__REQUEST_TYPE__USER_REQUEST
        llm_request_id = request_id
        chat_thread_id = llm_chat_completion.chat_thread_id
        chat_data      = dict(request_id          = request_id                       ,
                              chat_thread_id      = chat_thread_id                   ,
                              llm_request_id      = llm_request_id                   ,
                              timestamp           =  timestamp_utc_now()             ,
                              llm_chat_completion =  llm_chat_completion.model_dump())
        s3_key         = self.s3_key(chat_thread_id=chat_thread_id, llm_request_id=llm_request_id, request_type=request_type)
        metadata       = { 'request_id': request_id }
        if self.s3_save_data(data=chat_data, s3_key=s3_key, metadata=metadata):
            return status_ok(data={'llm_request_id': llm_request_id, 's3_key':s3_key})
        return status_error(message="s3 save data failed")
