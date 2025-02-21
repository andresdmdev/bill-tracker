import os, sys,pytest
from unittest.mock import patch, AsyncMock
from pathlib import Path

# Asegurar que el directorio raíz del proyecto está en el PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

# Modificar la importación para usar el módulo raíz
from lambda_function import lambda_handler, main

@pytest.fixture
def mock_env():
    with patch.dict(
        os.environ,
        {
            "ALLOWED_CHAT_IDS": "",
            "BOT_TOKEN": ""
        }
    ):
        yield

@pytest.mark.asyncio
async def test_message_processing_text(mock_env):
    """Test para verificar el procesamiento de mensajes"""
    sample_event = {
        "update_id": 184522457,
        "message": {
            "message_id": 62,
            "from": {
                "id": 7993663512,
                "is_bot": False,
                "first_name": "Andres",
                "language_code": "en"
            },
            "chat": {
                "id": 7993663512,
                "first_name": "Andres",
                "type": "private"
            },
            "date": 1739749682,
            "text": "hola"
        }
    }
    
    # Mock del bot de Telegram
    with patch('lambda_function.main') as mock_app:
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.run = AsyncMock()
        mock_app.return_value = mock_instance
        
        result = await lambda_handler(sample_event, None)
        
        assert result['statusCode'] == 200
        mock_instance.initialize.assert_awaited_once()
        mock_instance.run.assert_awaited_once()

@pytest.mark.asyncio
async def test_message_processing_command(mock_env):
    """Test para verificar el procesamiento de mensajes"""
    sample_event = {
        "update_id": 184522463,
        "message": {
            "message_id": 98,
            "from": {
                "id": 7993663512,
                "is_bot": False,
                "first_name": "Andres",
                "language_code": "en"
            },
            "chat": {
                "id": 7993663512,
                "first_name": "Andres",
                "type": "private"
            },
            "date": 1739754883,
            "text": "/start",
            "entities": [
                {
                    "offset": 0,
                    "length": 6,
                    "type": "bot_command"
                }
            ]
        }
    }
    
    with patch('lambda_function.main') as mock_app:
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.run = AsyncMock()
        mock_app.return_value = mock_instance
        
        result = await lambda_handler(sample_event, None)
        
        assert result['statusCode'] == 200
        mock_instance.initialize.assert_awaited_once()
        mock_instance.run.assert_awaited_once()

@pytest.mark.asyncio
async def test_message_processing_photo(mock_env):
    """Test para verificar el procesamiento de photos"""
    sample_event = {
        "update_id": 184522465,
        "message": {
            "message_id": 101,
            "from": {
                "id": 7993663512,
                "is_bot": False,
                "first_name": "Andres",
                "language_code": "en"
            },
            "chat": {
                "id": 7993663512,
                "first_name": "Andres",
                "type": "private"
            },
            "date": 1739755051,
            "photo": [
                {
                    "file_id": "AgACAgEAAxkBAANlZ7KOK-jx7fnQk_R7AgeBiftJPwgAAk6uMRvO_ZhFGhwablc3zuMBAAMCAANzAAM2BA",
                    "file_unique_id": "AQADTq4xG879mEV4",
                    "file_size": 962,
                    "width": 42,
                    "height": 90
                },
                {
                    "file_id": "AgACAgEAAxkBAANlZ7KOK-jx7fnQk_R7AgeBiftJPwgAAk6uMRvO_ZhFGhwablc3zuMBAAMCAANtAAM2BA",
                    "file_unique_id": "AQADTq4xG879mEVy",
                    "file_size": 13017,
                    "width": 148,
                    "height": 320
                },
                {
                    "file_id": "AgACAgEAAxkBAANlZ7KOK-jx7fnQk_R7AgeBiftJPwgAAk6uMRvO_ZhFGhwablc3zuMBAAMCAAN4AAM2BA",
                    "file_unique_id": "AQADTq4xG879mEV9",
                    "file_size": 63952,
                    "width": 369,
                    "height": 800
                },
                {
                    "file_id": "AgACAgEAAxkBAANlZ7KOK-jx7fnQk_R7AgeBiftJPwgAAk6uMRvO_ZhFGhwablc3zuMBAAMCAAN5AAM2BA",
                    "file_unique_id": "AQADTq4xG879mEV-",
                    "file_size": 85344,
                    "width": 590,
                    "height": 1280
                }
            ]
        }
    }
    
    with patch('lambda_function.main') as mock_app:
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.run = AsyncMock()
        mock_app.return_value = mock_instance
        
        result = await lambda_handler(sample_event, None)
        
        assert result['statusCode'] == 200
        mock_instance.initialize.assert_awaited_once()
        mock_instance.run.assert_awaited_once()

@pytest.mark.asyncio
async def test_message_processing_voice(mock_env):
    sample_event = {
        "update_id": 184522464,
        "message": {
            "message_id": 100,
            "from": {
                "id": 7993663512,
                "is_bot": False,
                "first_name": "Andres",
                "language_code": "en"
            },
            "chat": {
                "id": 7993663512,
                "first_name": "Andres",
                "type": "private"
            },
            "date": 1739754931,
            "voice": {
                "duration": 2,
                "mime_type": "audio/ogg",
                "file_id": "AwACAgEAAxkBAANkZ7KNstb4jGyLDMC62Yf0ztvv6s8AApYEAALO_ZhFREJzoiIcpDk2BA",
                "file_unique_id": "AgADlgQAAs79mEU",
                "file_size": 9934
            }
        }
    }
    
    with patch('lambda_function.main') as mock_app:
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.run = AsyncMock()
        mock_app.return_value = mock_instance
        
        result = await lambda_handler(sample_event, None)
        
        assert result['statusCode'] == 200
        mock_instance.initialize.assert_awaited_once()
        mock_instance.run.assert_awaited_once()

@pytest.mark.asyncio
async def test_message_processing_document(mock_env):
    sample_event = {
        "update_id": 184522468,
        "message": {
            "message_id": 110,
            "from": {
                "id": 7993663512,
                "is_bot": False,
                "first_name": "Andres",
                "language_code": "en"
            },
            "chat": {
                "id": 7993663512,
                "first_name": "Andres",
                "type": "private"
            },
            "date": 1739755919,
            "document": {
                "file_name": "IMG_0847.PNG",
                "mime_type": "image/jpeg",
                "thumbnail": {
                    "file_id": "AAMCAQADGQEAA25nspGOrlIYFxrkgAo6RR0TuddGbwACmQQAAs79mEXimKdPmIVCAgEAB20AAzYE",
                    "file_unique_id": "AQADmQQAAs79mEVy",
                    "file_size": 25241,
                    "width": 261,
                    "height": 320
                },
                "thumb": {
                    "file_id": "AAMCAQADGQEAA25nspGOrlIYFxrkgAo6RR0TuddGbwACmQQAAs79mEXimKdPmIVCAgEAB20AAzYE",
                    "file_unique_id": "AQADmQQAAs79mEVy",
                    "file_size": 25241,
                    "width": 261,
                    "height": 320
                },
                "file_id": "BQACAgEAAxkBAANuZ7KRjq5SGBca5IAKOkUdE7nXRm8AApkEAALO_ZhF4pinT5iFQgI2BA",
                "file_unique_id": "AgADmQQAAs79mEU",
                "file_size": 1586684
            }
        }
    }
    
    with patch('lambda_function.main') as mock_app:
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.run = AsyncMock()
        mock_app.return_value = mock_instance
        
        result = await lambda_handler(sample_event, None)
        
        assert result['statusCode'] == 200
        mock_instance.initialize.assert_awaited_once()
        mock_instance.run.assert_awaited_once()

if __name__ == '__main__':
    import asyncio
    asyncio.run(pytest.main())
