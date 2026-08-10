from . evaluator import Evaluator
from app.pipeline_component.pipeline import PipelineComponent
from app.data_loader_component.data_loader import DataLoader


pipeline = PipelineComponent()

data_loader = DataLoader()

evaluator = Evaluator(
    pipe_line=pipeline,
    data_loader=data_loader,
)

evaluator.evaluate()