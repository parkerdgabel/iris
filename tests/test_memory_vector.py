import pytest
from unittest.mock import patch, MagicMock
from ffmpeg_agent.memory.sqlite_vector import SQLiteVectorMemory
from ffmpeg_agent.settings import settings

# Mock the sqlite3 connect and cursor
@patch("sqlite3.connect")
def test_sqlite_vector_memory_init(mock_connect):
    # Ensure that connect is called with the correct database path
    memory = SQLiteVectorMemory()
    mock_connect.assert_called_once_with(settings.db_path)

    # Ensure that _init_db is called (which is a placeholder for now)
    # In a real test, we would mock cursor and check execute calls for table creation, etc.
    assert hasattr(memory, "conn")
   
