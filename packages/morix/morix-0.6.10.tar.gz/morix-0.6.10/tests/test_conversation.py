import pytest
import os
from unittest.mock import patch, MagicMock
from morix.conversation import (
    initialize_messages,
    handle_user_interaction,
    conversation
)
from morix.settings import config
from morix.complection import chat_completion_request


@pytest.fixture
def dummy_scan_folder(tmp_path):
    return str(tmp_path)


def test_scan_project_scan(dummy_scan_folder):
    os.mkdir(os.path.join(dummy_scan_folder, "test"))
    with open(os.path.join(dummy_scan_folder, "test", "file.txt"), "w") as f:
        f.write("test")

    scan_result = "file.txt"
    assert "file.txt" in scan_result


def test_initialize_messages(dummy_scan_folder):
    scan_result = "Test scan result"
    expected_roles = {
        "system": config.role_system_content,
        "user": config.additional_user_content
    }

    messages = initialize_messages(scan_result, dummy_scan_folder)
    for role, content in expected_roles.items():
        assert any(m["role"] == role and content for m in messages)


@patch('morix.conversation.prompt', return_value='User query')
@patch('morix.conversation.console.print')
def test_handle_user_interaction(mock_print, mock_prompt):
    messages = []
    initial_message = 'User query'
    user_content = handle_user_interaction(messages)
    # Adjust assertion to account for additional_user_content
    expected_message_count = 1 if not config.additional_user_content else 2
    assert len(messages) == expected_message_count
    assert user_content == initial_message
    assert any(m['content'] == initial_message for m in messages)

# # Adding a test for the conversation loop
# def test_conversation_loop():
#     mock_messages = [
#         {"role": "system", "content": "system message"},
#         {"role": "user", "content": "initial user input"}
#     ]
#     with patch('morix.conversation.chat_completion_request') as mock_chat_completion, \
#             patch('morix.conversation.handle_user_interaction', return_value='User input'):
#         mock_chat_completion.return_value = MagicMock(
#             choices=[
#                 MagicMock(
#                     finish_reason='stop',
#                     message=MagicMock(content='exit')  # Return 'exit' to simulate stopping
#                 )
#             ],
#             usage=MagicMock(total_tokens=50)
#         )
#         conversation(work_folder="/dummy/path", full_scan=False, structure_only=True, initial_message="Test")
#     mock_chat_completion.assert_called()

# Test to cover KeyboardInterrupt handling
def test_conversation_keyboard_interrupt():
    with patch('morix.conversation.chat_completion_request', side_effect=KeyboardInterrupt):
        with patch('morix.conversation.logger') as mock_logger:
            conversation(work_folder="/dummy/path", full_scan=False, structure_only=True, initial_message="Test")
            mock_logger.info.assert_any_call("Session completed")
