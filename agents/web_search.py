from textwrap import dedent
from typing import Optional

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.serpapi_tools import SerpApiTools

from agents.settings import agent_settings
from phi.storage.agent.postgres import PgAgentStorage

from db.session import db_url

web_search_agent_storage = PgAgentStorage(table_name="web_search_agent", db_url=db_url)


def get_web_search_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Web Search Agent",
        agent_id="web-search-agent",
        role="Search the web for information",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[SerpApiTools()],
        description="You are a Web Search Agent that has the special skill of searching the web for information.",
        instructions=[
            "If you can directly answer the user's question, do so.",
            "Otherwise, search the web for information.",
            "Important: \n"
            " - Focus on legitimate sources",
            " - Always provide sources and the links to the information you used to answer the question",
            " - If you cannot find the answer, say so and ask the user to provide more details.",
        ],
        expected_output=dedent("""\
        Your answer should be in the following format:

        ## Answer
        {provide a detailed answer to the user's question}

        ## Sources
        {provide the sources and links to the information you used to answer the question}
        """),
        markdown=True,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        storage=web_search_agent_storage,
        # Enable monitoring on phidata.app
        monitoring=True,
        debug_mode=debug_mode,
    )
