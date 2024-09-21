from cbr_shared.cbr_backend.chat_threads.S3_DB__Chat_Threads import S3_DB__Chat_Threads
from cbr_shared.schemas.base_models.chat_threads.LLMs__Chat_Completion import LLMs__Chat_Completion
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid


class S3__Chat_Thread(Type_Safe):
    chat_thread_id : Random_Guid
    s3_db          : S3_DB__Chat_Threads

    def save_chat_completion(self, llm_chat_completion: LLMs__Chat_Completion):
        s3_key = self.s3_db.s3_key()
        data     = llm_chat_completion.model_dump()
        metadata = { 'will': 'go here'}
        if self.s3_db.s3_save_data(data=data, s3_key=s3_key, metadata=metadata):
            return s3_key

