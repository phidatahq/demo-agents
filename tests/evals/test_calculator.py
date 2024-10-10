from typing import Optional

from phi.eval import Eval, EvalResult

from agents.calculator import get_calculator_agent


def test_9_11_bigger_or_9_9():
    evaluation = Eval(
        agent=get_calculator_agent(),
        question="Is 9.11 bigger or 9.9?",
        ideal_answer="9.11 is smaller than 9.9",
    )
    result: Optional[EvalResult] = evaluation.print_result()

    assert result is not None and result.accuracy_score >= 8


test_9_11_bigger_or_9_9()
