import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "your token"

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = {
    "Coffee": 800,
    "Tea": 500,
    "Cappuccino": 1000,
    "Latte": 1100,
    "Croissant": 900,
    "Sandwich": 1200
}

user_orders = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "☕ Welcome to our cafe!\n\n"
        "Type /menu to view the menu.\n"
        "Type /order to place an order."
    )

@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    text = "📋 Menu:\n\n"
    for item, price in menu.items():
        text += f"{item} — {price} тг\n"
    await message.answer(text)

@dp.message(Command("order"))
async def order_info(message: types.Message):
    user_orders[message.from_user.id] = []
    await message.answer(
        "Write the name of the item from the menu.\n"
        "When you're done, write 'done'"
    )

@dp.message()
async def handle_order(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if user_id in user_orders:
        if text.lower() == "done":
            order = user_orders[user_id]
            total = sum(menu[item] for item in order)

            result = "🛒 Your order:\n"
            for item in order:
                result += f"- {item}\n"

            result += f"\n💰 Total: {total} тг"
            await message.answer(result)
            del user_orders[user_id]
        elif text in menu:
            user_orders[user_id].append(text)
            await message.answer(f"✅ {text} added to order")
        else:
            await message.answer("❌ This product is not on the menu")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
