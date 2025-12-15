# Our system will have three agents:

## Agents

- A ResearchAgent that will search the web for information on the given topic.
- A WriteAgent that will write the report using the information found by the ResearchAgent.
- A ReviewAgent that will review the report and provide feedback.

## Workflow

We will use the `AgentWorkflow` class to create a multi-agent system that will execute these agents in order.

While there are many ways to implement this system, in this case, we will use a few tools to help with the research and writing processes.

## Tools

- A web_search tool to search the web for information on the given topic.
- A record_notes tool to record notes on the given topic.
- A write_report tool to write the report using the information found by the ResearchAgent.
- A review_report tool to review the report and provide feedback.

Utilizing the `Context` class, we can pass state between agents, and each agent will have access to the current state of the system.