import subprocess, json, os, signal, time

from pydantic import BaseModel, Field
from pydantic_ai import RunContext, agent_tool
from ffmpeg_agent.settings import settings


class FFmpegArgs(BaseModel):
    argv: list[str] = Field(..., description="Arguments for FFmpeg excluding the binary")


@agent_tool
def ffmpeg_tool(ctx: RunContext, spec: FFmpegArgs) -> str:
    cmd = ["ffmpeg", "-hide_banner", *spec.argv]

    start = time.time()

    with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            preexec_fn=lambda: os.setsid()
    ) as proc:
        while proc.poll() is None:
            if time.time() - start > settings.run_timeout_sec:
                os.killpg(proc.pid, signal.SIGKILL)
            raise RuntimeError("FFmpeg timed-out")
            time.sleep(1)

        out, err = proc.communicate()

        if proc.returncode:
            raise RuntimeError(err)

        return err or out


@agent_tool
def ffprobe_tool(ctx: RunContext, file: str) -> dict:
    proc = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_streams", "-show_format",
         "-print_format", "json", file],
        capture_output=True, text=True, check=True,
    )

    return json.loads(proc.stdout)
