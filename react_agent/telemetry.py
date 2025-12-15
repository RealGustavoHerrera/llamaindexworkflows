from dotenv import load_dotenv
import os
from arize.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

load_dotenv()

async def setup_telemetry():
    # Ensure your API keys are set as environment variables
    # Setup OTel via Arize AX's convenience function
    tracer_provider = register(
        space_id=os.getenv("ARIZE_SPACE_ID"),
        api_key=os.getenv("ARIZE_API_KEY"),
        project_name="my-llamaindex-workflows-react-agent"
    )

    # Instrument LlamaIndex (this covers Workflows as well)
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

    print("LlamaIndex (including Workflows) instrumented for Arize AX.")