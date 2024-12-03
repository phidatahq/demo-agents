import json
import httpx
from typing import Iterator

from phi.agent import Agent, RunResponse
from phi.workflow import Workflow
from phi.tools.newspaper4k import Newspaper4k
from phi.utils.log import logger


class HackerNewsReporter(Workflow):
    description: str = "Get the top stories from Hacker News and write a report on them."

    hn_agent: Agent = Agent(
        description="Get the top stories from hackernews. "
        "Share all possible information, including url, score, title and summary if available.",
        show_tool_calls=True,
    )

    writer: Agent = Agent(
        tools=[Newspaper4k()],
        description="Write an engaging report on the top stories from hackernews.",
        instructions=[
            "You will be provided with top stories and their links.",
            "Carefully read each article and think about the contents",
            "Then generate a final New York Times worthy article",
            "Break the article into sections and provide key takeaways at the end.",
            "Make sure the title is catchy and engaging.",
            "Share score, title, url and summary of every article.",
            "Give the section relevant titles and provide details/facts/processes in each section."
            "Ignore articles that you cannot read or understand.",
            "REMEMBER: you are writing for the New York Times, so the quality of the article is important.",
        ],
    )

    def get_top_hackernews_stories(self, num_stories: int = 10) -> str:
        """Use this function to get top stories from Hacker News.

        Args:
            num_stories (int): Number of stories to return. Defaults to 10.

        Returns:
            str: JSON string of top stories.
        """

        # Fetch top story IDs
        response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        story_ids = response.json()

        # Fetch story details
        stories = []
        for story_id in story_ids[:num_stories]:
            story_response = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            story = story_response.json()
            story["username"] = story["by"]
            stories.append(story)
        return json.dumps(stories)

    def run(self, num_stories: int = 5) -> Iterator[RunResponse]:
        # Set the tools for hn_agent here to avoid circular reference
        self.hn_agent.tools = [self.get_top_hackernews_stories]

        logger.info(f"Getting top {num_stories} stories from HackerNews.")
        top_stories: RunResponse = self.hn_agent.run(num_stories=num_stories)
        if top_stories is None or not top_stories.content:
            yield RunResponse(run_id=self.run_id, content="Sorry, could not get the top stories.")
            return

        logger.info("Reading each story and writing a report.")
        yield from self.writer.run(top_stories.content, stream=True)
