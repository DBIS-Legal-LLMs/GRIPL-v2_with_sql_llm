import time
from app.data_loader_component.data_loader import DataLoader
from app.pipeline_component.pipeline import PipelineComponent
import traceback
import json
import os

class Evaluator:

    def __init__(self,
                 data_loader: DataLoader,
                 pipe_line: PipelineComponent
                 ):
        self.data_loader = data_loader
        self.pipe_line = pipe_line

    async def evaluate(self):
        try:



            eval_pd_set = self.data_loader.load_evaluation_data_set_as_pd()

            idx = 0

            for index, row in eval_pd_set.iterrows():
                current_bpmn_file = row["bpmn_xml"]

                current_activities_fields = self.pipe_line.get_only_activity_fields(current_bpmn_file)

                predicted_critical_elements = []

                gold_critical_elements = row.get("expected_values", [])

                for activity in current_activities_fields:

                    possible_critical_element = await self.pipe_line.get_sid_and_reason_if_critical(activity)
                    if possible_critical_element:
                        predicted_critical_elements.append(possible_critical_element)
                    time.sleep(60)

                eval_res = self.check_equal_and_predicted_equal(
                    predicted_critical_elements,
                    gold_critical_elements,
                )
                print("eval res ")
                print(eval_res)
                print("------------")
                print("gold queries")
                print(gold_critical_elements)
                print("-------------")
                print("predicted queries")
                print(predicted_critical_elements)

                time.sleep(60)

                idx += 1
                if idx  == 5:
                    break

        except Exception as e:
            print("in eval pipeline")
            print(traceback.format_exc())
            print(e)

    def check_equal_and_predicted_equal(self,
                                        predicted_critical_elements,
                                        gold_critical_elements
                                        )-> bool:
        gold_critical_elements = json.loads(gold_critical_elements)
        return set(
            (element["value"], element["reason"])
            for element in predicted_critical_elements
        ) == set(
            (element["value"], element["reason"])
            for element in gold_critical_elements
        )
