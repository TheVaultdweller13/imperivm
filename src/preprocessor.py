import re
from abc import ABC, abstractmethod
from typing import override, List


class Preprocessor(ABC):
    @abstractmethod
    def process(self, program: str) -> str:
        pass


class CommentsPreprocessor(Preprocessor):
    @override
    def process(self, program: str):
        cleaned_program = map(lambda line: re.sub(r"#.*$", "", line), program.splitlines())
        return "\n".join(cleaned_program)


class PipelinePreprocessor(Preprocessor):
    def __init__(self, preprocessor_actions: List[Preprocessor]):
        self.preprocessor_actions = preprocessor_actions

    @override
    def process(self, program: str):
        for action in self.preprocessor_actions:
            program = action.process(program)
        return program