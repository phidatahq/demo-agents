from textwrap import dedent
from typing import Optional

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.exa import ExaTools

from agents.settings import agent_settings
from phi.storage.agent.postgres import PgAgentStorage

from db.session import db_url

research_agent_storage = PgAgentStorage(table_name="research_agent", db_url=db_url)


def get_research_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Research Agent",
        agent_id="research-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[ExaTools(type="keyword")],
        description=dedent("""\
        You are a Research Agent that has the special skill of writing New York Times worthy articles.
        If you can directly respond to the user, do so. If the user asks for a report or provides a topic, follow the instructions below.
        """),
        instructions=[
            "For the provided topic, run 3 different searches.",
            "Read the results carefully and prepare a NYT worthy article.",
            "Focus on facts and make sure to provide references.",
        ],
        expected_output=dedent("""\
        Your articles should be engaging, informative, well-structured and in markdown format. They should follow the following structure:

        ## Engaging Article Title

        ### Overview
        {give a brief introduction of the article and why the user should read this report}
        {make this section engaging and create a hook for the reader}

        ### Section 1
        {break the article into sections}
        {provide details/facts/processes in this section}

        ... more sections as necessary...

        ### Takeaways
        {provide key takeaways from the article}

        ### References
        - [Reference 1](link)
        - [Reference 2](link)
        """),
        markdown=True,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        storage=research_agent_storage,
        # Enable monitoring on phidata.app
        monitoring=True,
        debug_mode=debug_mode,
    )
