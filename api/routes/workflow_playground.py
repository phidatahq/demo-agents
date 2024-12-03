from os import getenv
from phi.playground import Playground

from workflows.blog_post import BlogPostGenerator
from workflows.hackernews import HackerNewsReporter
from workflows.investment import InvestmentAnalyst

######################################################
## Router for the workflow playground
######################################################

# Create a playground instance
playground = Playground(workflows=[BlogPostGenerator, HackerNewsReporter, InvestmentAnalyst])
# Log the playground endpoint with phidata.app
if getenv("RUNTIME_ENV") == "dev":
    playground.create_endpoint("http://localhost:8008")

playground_router = playground.get_router()
