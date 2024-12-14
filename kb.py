from aiogram import types
import db


def main_keyboard():
	kb = [
		[types.KeyboardButton(text="#️⃣ Получить ссылку")],
		[types.KeyboardButton(text='🗄 Получить все сообщения')]
	]
	return types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Выберите действие")

def cancel_state_keyboard():
	kb=[[types.KeyboardButton(text='❌Отмена❌')]]
	return types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)