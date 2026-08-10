from app.data_loader_component.data_loader import DataLoader
from app.pipeline_component.pipeline import PipelineComponent


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

            print("pd ")
            print(eval_pd_set)

        except Exception as e:
            print(e)