# test_bot.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import discord
from app import bot, monitoring


@pytest.mark.asyncio
async def test_on_ready():
    bot._connection = MagicMock()
    bot._connection.user = MagicMock()
    bot._connection.user.name = 'TestBot'

    with patch('builtins.print') as mock_print:
        await bot.on_ready()
        mock_print.assert_called_with('Logged in as TestBot')


@pytest.mark.asyncio
async def test_on_message_mention_start_monitoring():
    global monitoring
    monitoring = False

    message = MagicMock()
    message.author = MagicMock()
    message.content = '@Veritas start monitoring'
    message.attachments = []
    message.channel.send = AsyncMock()
    message.guild = MagicMock()

    bot._connection = MagicMock()
    bot._connection.user = MagicMock()
    bot._connection.user.mentioned_in.return_value = True

    await bot.on_message(message)
    message.channel.send.assert_awaited_with('Monitoring started!')


@pytest.mark.asyncio
async def test_on_message_mention_stop_monitoring():
    global monitoring
    monitoring = True

    message = MagicMock()
    message.author = MagicMock()
    message.content = '@Veritas stop monitoring'
    message.attachments = []
    message.channel.send = AsyncMock()
    message.guild = MagicMock()

    bot._connection = MagicMock()
    bot._connection.user = MagicMock()
    bot._connection.user.mentioned_in.return_value = True

    await bot.on_message(message)
    message.channel.send.assert_awaited_with('Monitoring stopped!')


@pytest.mark.asyncio
async def test_on_message_mention_stop_monitoring():
    global monitoring
    monitoring = True

    message = MagicMock()
    message.author = MagicMock()
    message.content = '@Veritas stop monitoring'
    message.attachments = []
    message.channel.send = AsyncMock()
    message.guild = MagicMock()

    bot._connection = MagicMock()
    bot._connection.user = MagicMock()
    bot._connection.user.mentioned_in.return_value = True

    await bot.on_message(message)
    message.channel.send.assert_awaited_with('Monitoring stopped!')

