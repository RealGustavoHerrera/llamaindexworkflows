from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow
from maw_agents import research_agent, write_agent, review_agent

class MAW_Workflow(AgentWorkflow):
    """Multi-Agent Workflow coordinating research, writing, and review agents."""

    def __init__(self):
        super().__init__(
            agents=[research_agent, write_agent, review_agent],
            initial_agent=research_agent,
        )
    
    def run_agent(self, **kwargs):
        """Run the workflow starting with the initial agent."""
        return self.run(kwargs)
    
    