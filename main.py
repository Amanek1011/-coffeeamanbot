
import asyncio


from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import keyboards as kb
from db import db

load_dotenv()

TOKEN = "7623486555:AAHsFKzlQn6kZ3r27bgT7T8XNk3_PfkDsxc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

coffee_images = {
    "kakao": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcR8Uau19ltJcyMZaakjtIlvM0ziAdaeEBnNkYPAvjOVMiJSEYBh2Baqv0mTudoLIv-AfXvMjnJ4Rfm_nlGXqcmkEvfGuWaIDMIhrv5ojQ",
    "latte": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Caffe_Latte_at_Pulse_Cafe.jpg/1200px-Caffe_Latte_at_Pulse_Cafe.jpg",
    "cappuccino": "https://www.allrecipes.com/thmb/chsZz0jqIHWYz39ViZR-9k_BkkE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8624835-how-to-make-a-cappuccino-beauty-4x3-0301-13d55eaad60b42058f24369c292d4ccb.jpg"
}


user_orders = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Какой кофе желаете?", reply_markup=kb.coffee_menu)

@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data in coffee_images:
        user_orders[user_id] = {"coffee": callback.data}
        await bot.send_photo(chat_id=user_id, photo=coffee_images[callback.data],
                             caption=f"Вы выбрали {callback.data}. Какой размер?", reply_markup=kb.size_menu)

    elif callback.data == "confirm":
        order = user_orders.get(user_id, {})
        coffee = order.get("coffee", "?")
        size = order.get("size", "?")
        comment = order.get("comment", "Без комментария")
        await callback.message.answer(
            f"Ваш заказ: {coffee}, {size}.\n"
            f"Комментарий: {comment}\n"
            "Заказ принят! Будет готов в течение 5 минут."
        )
        await db.add_user(user_id, callback.from_user.username, callback.from_user.first_name,
                          coffee, size, comment)
        user_orders.pop(user_id, None)

    elif callback.data == "cancel":
        await callback.message.answer("Заказ отменен.")
        user_orders.pop(user_id, None)

@dp.message()
async def process_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_orders and "coffee" in user_orders[user_id]:
        if message.text in ["Маленький", "Средний", "Большой"]:
            user_orders[user_id]["size"] = message.text
            await message.answer("Добавьте комментарий к заказу (или напишите 'Без комментария').")

        elif "size" in user_orders[user_id]:
            user_orders[user_id]["comment"] = message.text
            await message.answer("Подтвердите заказ.", reply_markup=kb.confirm_menu)

        else:
            await message.answer("Пожалуйста, выберите размер кофе.", reply_markup=kb.size_menu)


async def main():
    print("Bot started...")
    await db.connect()
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())