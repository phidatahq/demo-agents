from typing import Optional

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.calculator import Calculator

from agents.settings import agent_settings


def get_calculator_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Calculator Agent",
        agent_id="calculator-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        instructions=["Use the calculator tool for comparisons."],
        tools=[Calculator(enable_all=True)],
        markdown=True,
        show_tool_calls=True,
        # Enable monitoring on phidata.app
        monitoring=True,
        debug_mode=debug_mode,
    )
