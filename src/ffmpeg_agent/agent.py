import uuid, logging, asyncio
from pydantic_ai import Agent
from pydantic_ai.messages import
from ffmpeg_agent.settings import settings
from ffmpeg_agent.tools import ffprobe_tool, ffmpeg_tool
from ffmpeg_agent.middleware import RetryMiddleware
from ffmpeg_agent.memory_strategies import memory_factory
from ffmpeg_agent.history import SqliteHistory
from ffmpeg_agent.providers_sync import OpenAIClient

logger = logging.getLogger("ffmpeg_agent")
history = SqliteHistory()

SYSTEM_PROMPT = """
You are an FFmpeg expert agent.
Plan steps, call tools, verify outputs, summarise.
Never exceed {max_calls} tool calls.
""".format(max_calls=settings.max_tool_calls)


def build_agent(model_client=None):
    if model_client is None:
        model_client = OpenAIClient()
        agent = Agent(
            model=model_client,
            system_prompt=SYSTEM_PROMPT,
            tools=[ffprobe_tool, ffmpeg_tool],
            # max_turns=settings.max_tool_calls,
            # middleware=[RetryMiddleware()],
            # memory=memory_factory(),
        )
    else:
        agent = Agent(
            model=model_client,
            system_prompt=SYSTEM_PROMPT,
            tools=[ffprobe_tool, ffmpeg_tool],
        )

    async def run_async(ctx, prompt):
        session = ctx.get("session") or str(uuid.uuid4())
        res = await agent.run_async({"session": session}, prompt)
        history.save(session, res.all_messages())
        return res

    def run(ctx, prompt):

        session = ctx.get("session") or str(uuid.uuid4())
        res = agent.run_sync({"session": session}, prompt)
        history.save(session, res.all_messages())
        return res

    agent.run_async = run_async



    return agent
