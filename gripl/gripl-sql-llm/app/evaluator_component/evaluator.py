from logging import critical

from app.data_loader_component.data_loader import DataLoader
from app.pipeline_component.pipeline import PipelineComponent
import re

class Evaluator:

    def __init__(self,
                 data_loader: DataLoader,
                 pipe_line: PipelineComponent
                 ):
        self.data_loader = data_loader
        self.pipe_line = pipe_line

    def evaluate(self)->list[dict[str, str]]:
        try:

            eval_pd_set = self.data_loader.load_evaluation_data_set_as_pd()

            critical_elements = []

            for index, row in eval_pd_set.iterrows():
                current_bpmn_file = row["bpmn_xml"]
                current_activities_fields = self.pipe_line.get_only_activity_fields(current_bpmn_file)

                for activity in current_activities_fields:

                    possible_critical_element = self.pipe_line.get_sid_and_reason_if_critical(activity)
                    if possible_critical_element:
                        critical_elements.append(possible_critical_element)
                
            return critical_elements

        except Exception as e:
            print(e)
            return []