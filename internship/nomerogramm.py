from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
import nomerogramm_take_with_website

"""
telegram bot for getting general information about the car by number
"""

TOKEN = ""
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


async def prov_nomer(text):
    fl = True
    bukv_n = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х',
              'A', 'B', 'E', 'K', 'M', 'H', 'O', 'P', 'C', 'T', 'Y', 'X']  # 1стр русский 2стр английсткий
    cifr_n = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    text = text.upper()
    if len(text) in [8, 9]:
        if ((text[1] == '0') and (text[2] == text[3]) and (text[3] == text[1])):
            fl = False
        else:
            for i in range(len(text)):
                if i in [0, 4, 5]:
                    if text[i] not in bukv_n:
                        fl = False
                        break
                else:
                    if text[i] not in cifr_n:
                        fl = False
                        break
    else:
        fl = False
    return fl


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(f'<b>Привет {message.from_user.first_name}!</b>\n\nНапиши мне номер машины чтобы я смог'
                         f' выдать тебе основную информацию по ней!\n\nПример: <b>А000АА77</b>')


@dp.message_handler()
async def echo_message(msg: types.Message):
    if (await prov_nomer(msg.text) == True):
        ogid_sms = await bot.send_message(msg.from_user.id, 'Ожидайте, запрос выполняется...')
        sms = msg.text.upper()
        data = await nomerogramm_take_with_website.poisk(sms).osn()
        if type(data) == str:
            await ogid_sms.delete()
            await bot.send_message(msg.from_user.id, data)
        else:
            photo = data['previewImageUrl']
            pr_data = f'Отчет о машине c номером: <b>{sms}</b>\n\n' \
                      f'<b>VIN:</b> {data["vin"]}\n' \
                      f'<b>Модель:</b> {data["model"]}\n' \
                      f'<b>Бренд:</b> {data["brand"]}\n' \
                      f'<b>Год выпуска:</b> {data["year"]}\n' \
                      f'<b>Основные данные:</b> {data["equipmentSummary"]}\n'
            if photo != None:
                await ogid_sms.delete()
                await bot.send_photo(chat_id=msg.chat.id, photo=photo, caption=pr_data)
            else:
                await ogid_sms.delete()
                await bot.send_message(msg.from_user.id, pr_data)
    else:
        await bot.send_message(msg.from_user.id, 'Вы ввели номер некоректно\n\nПример: <b>А000АА77</b>')

if __name__ == '__main__':
    executor.start_polling(dp)
