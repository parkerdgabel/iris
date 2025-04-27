import pytest
from unittest.mock import patch, MagicMock
from ffmpeg_agent.tools import ffmpeg_tool, ffprobe_tool, FFmpegArgs

# Mock objects for subprocess.CompletedProcess and subprocess.Popen
MockCompletedProcess = MagicMock()
MockCompletedProcess.stdout = ""
MockCompletedProcess.stderr = ""
MockCompletedProcess.returncode = 0

MockPopen = MagicMock()
MockPopen.stdout.read.return_value = ""
MockPopen.stderr.read.return_value = ""
MockPopen.communicate.return_value = ("", "")
MockPopen.returncode = 0
MockPopen.pid = 12345
MockPopen.poll.return_value = 0 # Indicate process finished immediately

@patch("subprocess.run", return_value=MockCompletedProcess)
def test_ffprobe_tool(mock_run):
    # Configure mock_run to return a specific JSON output
    mock_run.return_value.stdout = '{"streams": [], "format": {}}'
    result = ffprobe_tool(None, "dummy_file.mp4") # ctx is None for now
    assert result == {"streams": [], "format": {}}
    mock_run.assert_called_once_with(
        ["ffprobe", "-v", "quiet", "-show_streams", "-show_format",
         "-print_format", "json", "dummy_file.mp4"],
        capture_output=True, text=True, check=True,
    )

# Patch subprocess.Popen and time.time for ffmpeg_tool testing
@patch("subprocess.Popen", return_value=MockPopen)
@patch("time.time", side_effect=[0, 1, 2]) # Simulate time passing for timeout
def test_ffmpeg_tool(mock_time, mock_popen):
    spec = FFmpegArgs(argv=["-i", "input.mp4", "output.mp4"])
    result = ffmpeg_tool(None, spec) # ctx is None for now
    assert result == ""
    mock_popen.assert_called_once_with(
        ["ffmpeg", "-hide_banner", "-i", "input.mp4", "output.mp4"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        preexec_fn=hasattr(os, 'setsid') and os.setsid or None # Handle setsid on different OS
    )
