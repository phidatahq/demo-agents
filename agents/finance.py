from typing import Optional

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools

from agents.settings import agent_settings
from phi.storage.agent.postgres import PgAgentStorage

from db.session import db_url

finance_agent_storage = PgAgentStorage(table_name="finance_agent", db_url=db_url)


def get_finance_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Finance Agent",
        role="Analyze financial data",
        agent_id="finance-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[YFinanceTools(enable_all=True)],
        description="You are a financial agent with the special skill of analyzing complex financial information.",
        instructions=[
            "Always use tables to display data",
            "Aim to wow the user with your knowledge and expertise.",
        ],
        storage=finance_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
