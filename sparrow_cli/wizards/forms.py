from typing import (Any, Optional, Union, List, Dict)
from sparrow_cli.wizards.questions import Question


class Form:
    def __init__(self, questions: List[Question]):
        self.questions = questions

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> "Form":
        """
        Build a new instance from raw.
        :param raw: A dictionary containing the form attributes
        :return: A new ``Form`` instance
        """
        questions = [Question.from_raw(v) for v in raw["questions"]]
        return cls(questions)

    def ask(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform the asking process.

        :param context: A mapping containing already answered questions and environment variables for rendering.
        :param kwargs: Additional named arguments to be passed to each question.
        :return: A mapping from the question names to the obtained answers.
        """
        answers = dict() if context is None else context.copy()

        for question in self.questions:
            if question.name not in answers:
                answers[question.name] = question.ask(context=answers, **kwargs)
        return answers

    def get_template_uris(
            self, answers: Dict[str, Any], context: Optional[Dict[str, Any]] = None, *args, **kwargs
    ) -> List[str]:
        """Get template uris.

        :param answers: A mapping from question name to answer value.
        :param context: Additional context variables.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A list of strings representing template uris.
        """
        if context is None:
            context = dict()

        uris = (
            question.get_template_uri(answers[question.name], context=context.update(answers), *args, **kwargs)
            for question in self.questions
            if question.name in answers
        )
        uris = filter(lambda uri: uri is not None, uris)
        return list(uris)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.questions == other.questions
