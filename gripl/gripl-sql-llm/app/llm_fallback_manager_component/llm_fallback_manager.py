import traceback

class LLMFallBackManager:

    def __init__(self,
                 llm_names: list[str],
                 llm_api_key_name_in_env = list[str]
                 ):
        self.llm_list = llm_names
        self.llm_api_key_name_in_env = llm_api_key_name_in_env
        self.current_llm_index = 0


    def get_answer_with_fallback(self,
                                 messages: list,
                                 tools: list | None = None,
                                 ):

        try:

            pass

        except Exception as e:
            print(traceback.format_exc())

    def get_next_llm(self,

                               messages: list,
                               tools: list | None = None,
                               ):

        try:
            pass
        except Exception as e:
            print(traceback.format_exc())


