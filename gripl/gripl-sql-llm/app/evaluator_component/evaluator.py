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
        print("in evaluator methode")