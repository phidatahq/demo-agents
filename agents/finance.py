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
        agent_id="finance-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[YFinanceTools(enable_all=True)],
        description="You are a finance agent",
        instructions=["Use tables where possible"],
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        storage=finance_agent_storage,
        # Enable monitoring on phidata.app
        monitoring=True,
        debug_mode=debug_mode,
    )
