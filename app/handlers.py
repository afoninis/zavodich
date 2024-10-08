from calendar import *
from datetime import datetime

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from functions import get_current_schedule
from app import keyboards
from datetime import *

router = Router()

now = datetime.now()
now_date = date(day=now.day, month=now.month, year=now.year)
next_vacation = date(day=19, month=7, year=2025)
days_before_vacation = (next_vacation-now_date).days

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Мой аккаунт</b>\n<i>Информация о вашем аккаунте</i>\n\n💨️\tID:\t\t{message.from_user.id}\n💨️\tДней до отпуска: {days_before_vacation}\n\n🗺️ Моя статистика:\n├ Всего запросов: 0", reply_markup=keyboards.show_main, parse_mode=ParseMode.HTML)

@router.message()
async def echo(message: types.Message):
    data = get_current_schedule(2, 9, 2024)

    now = datetime.now()
    target_month = [i for i in data if i["month"] == int(message.text) and i["year"] == now.year]

    result_month = [[i["day"], i["month"], i["year"], i["activity"]] for i in target_month]
    result_month.sort(key=lambda x: x[0])

    result = "\n".join([f"[{i[0]}.{i[1]}.{i[2]}] {i[3]}" for i in result_month])

    await message.reply(result)


@router.callback_query(F.data == "KB_MAIN")
async def main(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"<b>Мой аккаунт</b>\n<i>Информация о вашем аккаунте</i>\n\n💨️\tID:\t\t{callback.message.from_user.id}\n💨️\tДней до отпуска: {days_before_vacation}\n\n🗺️ Моя статистика:\n├ Всего запросов: 0", reply_markup=keyboards.show_main, parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "KB_SCHEDULE")
async def schedule(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"<b>Мой аккаунт</b>\n<i>Информация о вашем аккаунте</i>\n\n💨️\tID:\t\t{callback.message.from_user.id}\n💨️\tДней до отпуска: {days_before_vacation}\n\n🗺️ Моя статистика:\n├ Всего запросов: 0", reply_markup=await keyboards.show_schedule(), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "KB_TODAY")
async def today(callback: types.CallbackQuery):
    await callback.answer()
    now = datetime.now()
    data = get_current_schedule(2, 9, 2024)
    await callback.message.answer(f"<b>Сегодня:</b>\n<i>Вид активности</i>\n\n{[item for item in data if item["day"] == now.day and item["month"] == now.month and item["year"] == now.year][0]["activity"]}", parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "KB_TOMORROW")
async def tomorrow(callback: types.CallbackQuery):
    await callback.answer()
    now = datetime.now()
    data = get_current_schedule(2, 9, 2024)
    delta = timedelta(days=1)
    tomorrow_date = now+delta
    await callback.message.answer(f"<b>Завтра:</b>\n<i>Вид активности</i>\n\n{[item for item in data if item["day"] == tomorrow_date.day and item["month"] == tomorrow_date.month and item["year"] == tomorrow_date.year][0]["activity"]}", parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "KB_THIS_MONTH")
async def this_month(callback: types.CallbackQuery):
    await callback.answer()
    now = datetime.now()
    data = get_current_schedule(2, 9, 2024)
    current_month_dates = [item for item in data if item["month"] == now.month and item["year"] == now.year]

    result_month = [[i["day"], i["month"], i["year"], i["activity"]] for i in current_month_dates]
    result_month.sort(key=lambda x: x[0])
    # result = "\n".join([f"[{i[0]}.{i[1]}.{i[2]}] {i[3]}" for i in result_month])

    result = f"{month_name[now.month]} ({now.month}/12) - {now.year} г.\n\n"
    # result += "\n".join([f"[{i[0]}.{i[1]}.{i[2]}] {i[3]}" for i in result_month])
    result += "\n".join([f"{i[0]}) {i[3]}" for i in result_month])


    await callback.message.answer(
        f"<b>Этот месяц:</b>\n<i>Вид активности</i>\n\n{result}",
        parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "KB_NEXT_MONTH")
async def next_month(callback: types.CallbackQuery):
    await callback.answer()
    now = datetime.now()
    data = get_current_schedule(2, 9, 2024)
    delta = timedelta(days=monthrange(now.year, now.month)[1] - now.day + 1)
    tomorrow_date = now + delta

    current_month_dates = [item for item in data if item["month"] == tomorrow_date.month and item["year"] == tomorrow_date.year]

    result_month = [[i["day"], i["month"], i["year"], i["activity"]] for i in current_month_dates]
    result_month.sort(key=lambda x: x[0])
    result = f"{month_name[tomorrow_date.month]} ({tomorrow_date.month}/12) - {tomorrow_date.year} г.\n\n"
    # result += "\n".join([f"[{i[0]}.{i[1]}.{i[2]}] {i[3]}" for i in result_month])
    result += "\n".join([f"{i[0]}) {i[3]}" for i in result_month])

    await callback.message.answer(
        f"<b>Следующий месяц:</b>\n<i>Вид активности</i>\n\n{result}",
        parse_mode=ParseMode.HTML)