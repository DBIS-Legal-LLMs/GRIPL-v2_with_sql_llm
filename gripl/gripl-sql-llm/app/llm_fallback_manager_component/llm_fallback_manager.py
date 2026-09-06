from app.llm_component.llm import LLM
import traceback

class LLMFallBackManager:

    def __init__(self,
                 llm_list: list[LLM]
                 ):
        self.llm_list = llm_list


    def get_answer_with_fallback(self,
                                 messages: list,
                                 tools: list | None = None,
                                 ):

        try:

            pass

        except Exception as e:
            print(traceback.format_exc())

    def get_current_llm_answer(self,
                               current_llm: LLM,
                               messages: list,
                               tools: list | None = None,
                               ):

        try:
            return current_llm.get_answer_from_llm(
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            print(traceback.format_exc())


