from typing import Optional

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.youtube_tools import YouTubeTools

from agents.settings import agent_settings
from phi.storage.agent.postgres import PgAgentStorage

from db.session import db_url

youtube_agent_storage = PgAgentStorage(table_name="finance_agent", db_url=db_url)


def get_youtube_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="YouTube Agent",
        role="Answer questions about YouTube videos",
        agent_id="youtube-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            model=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[YouTubeTools()],
        description="You are a YouTube agent that has the special skill of understanding YouTube videos and answering questions about them.",
        instructions=[
            "When the user asks about a video, confirm that they have provided a valid YouTube URL. If not, ask them for it.",
            "Using a video URL, get the video data using the `get_youtube_video_data` tool and captions using the `get_youtube_video_data` tool.",
            "Using the data and captions, answer the user's question.",
            "If you cannot find the answer in the video, say so and ask the user to provide more details.",
            "Aim to wow the user with your knowledge and expertise.",
        ],
        markdown=True,
        add_history_to_messages=True,
        num_history_responses=5,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        storage=youtube_agent_storage,
        # Enable monitoring on phidata.app
        monitoring=True,
        debug_mode=debug_mode,
    )
