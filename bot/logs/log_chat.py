from ..config import settings, bot


async def custom_log(log_message: str) -> None:
    """Отправляет сообщение в лог-канал

    Args:
        log_message (str): сообщение, которое отправится в лог-канал
    """
    if not settings.LOG_MODE:
        return

    chat_id = settings.LOG_GROUP_ID
    if chat_id:
        bot_user = await bot.get_me()
        bot_name = bot_user.username
        text = f"[{bot_name}] : {log_message}"

        await bot.send_message(chat_id=chat_id, text=text)