from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type in ["private"]:
            return False
            
        member = await message.bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        
        return member.status in ["administrator", "creator"]
