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

    def evaluate(self):
        try:

            eval_pd_set = self.data_loader.load_evaluation_data_set_as_pd()

            for index, row in eval_pd_set.iterrows():
                current_bpmn_file = row["bpmn_xml"]
                current_activities_fields = self.pipe_line.get_only_activity_fields(current_bpmn_file)

                for activity in current_activities_fields:
                    self.pipe_line.get_sid_if_critical(activity)







                break


        except Exception as e:
            print(e)