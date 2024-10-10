from os import getenv
from phi.playground import Playground

from agents.finance import get_finance_agent

######################################################
## Router for the agent playground
######################################################

finance_agent = get_finance_agent(debug_mode=True)

# Create a playground instance
playground = Playground(agents=[finance_agent])
# Log the playground endpoint with phidata.app
if getenv("RUNTIME_ENV") == "dev":
    playground.create_endpoint("http://localhost:8000")

playground_router = playground.get_router()
