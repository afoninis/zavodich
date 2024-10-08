from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


show_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Расписание", callback_data="KB_SCHEDULE")],
    [InlineKeyboardButton(text="🎃 Сообщить об ошибке", callback_data="KB_REPORT_BUG")]
])

async def show_schedule():
    options = [["Сегодня", "KB_TODAY"], ["Завтра", "KB_TOMORROW"],["Этот месяц", "KB_THIS_MONTH"], ["Следующий месяц", "KB_NEXT_MONTH"], ["← Главная", "KB_MAIN"]]

    keyboard = InlineKeyboardBuilder()

    for opt in options:
        keyboard.add(InlineKeyboardButton(text=opt[0], callback_data=opt[1]))

    return keyboard.adjust(1).as_markup()