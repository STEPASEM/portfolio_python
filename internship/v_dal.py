from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
import v_dal_take_with_website

"""
telegram bot for getting information about the meaning of a word from Dahl's dictionary
"""

TOKEN = "8187923844:AAFTTd3E8TaThPlKITmoBazNka0t9ediED0"
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

async def convert(sms):
    spis = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CA", "CB", "CC", "CD", "CE", "CF",
            "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DA", "DB", "DC", "DD", "DE", "DF"]
    spis_bukv = ['А', 'Б', 'В', 'Г', 'Д', 'ЕЁ', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
                 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
    cop_sms = ''
    for i in sms:
        for j in range(len(spis_bukv)):
            if i in spis_bukv[j]:
                cop_sms += ('%'+spis[j])
    if len(cop_sms) == (len(sms)*3):
        return cop_sms
    return sms

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(f'<b>Привет {message.from_user.first_name}!</b>\n\nНапиши мне слово'
                         f' и я выдам тебе его описание!')


@dp.message_handler()
async def echo_message(msg: types.Message):
    sms = msg.text.upper()
    copy_sms = sms
    sms = await convert(sms)
    if sms != copy_sms:
        ogid_sms = await bot.send_message(msg.from_user.id, 'Ожидайте, запрос выполняется...')
        data = await v_dal_take_with_website.poisk(sms).osn()
        if data != 'Такого слова нет в словаре Даля':
            data[0] = data[0].upper()
            str_data = ''
            for i in data:
                str_data += (i + '\n\n')
        else:
            str_data = data
        await ogid_sms.delete()
        if len(str_data) > 4096:
            for x in range(0, len(str_data), 4096):
                await bot.send_message(msg.from_user.id, str_data[x:x + 4096])
        else:
            await bot.send_message(msg.from_user.id, str_data)
    else:
        await bot.send_message(msg.from_user.id, 'Вы ввели слово неправильно')

if __name__ == '__main__':
    executor.start_polling(dp)
