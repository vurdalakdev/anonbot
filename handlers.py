from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram import Bot
import text, db, kb, asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
router = Router()

class MESSAGE(StatesGroup):
	userid = State()
	message = State()

@router.message(F.text.startswith('/start'))
async def start_handle(msg: types.Message, state: FSMContext):
	if len(msg.text.split(' '))!=1:
		await state.update_data(userid=msg.text.split(' ')[-1:])
		await state.set_state(MESSAGE.message)
		await msg.answer("Введите сообщение", reply_markup=kb.cancel_state_keyboard())
	else:
		db.create_user(msg.from_user.id)
		await msg.answer(text.default, reply_markup=kb.main_keyboard())

@router.message(F.text=='🗄 Получить все сообщения')
async def get_all_handle(msg: types.Message):
	if db.get_user(msg.from_user.id) == None: start_handle(msg)
	await msg.answer(text.msgs(db.get_all_msgs(msg.from_user.id)))

@router.message(F.text=='#️⃣ Получить ссылку')
async def create_link_handle(msg: types.Message):
	await msg.answer(f'https://t.me/messageanonymously_bot?start={msg.from_user.id}')

@router.message(F.text=='❌Отмена❌')
async def cancel_handler(msg: types.Message, state: FSMContext) -> None:
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.clear()
	await msg.answer('Отменено',reply_markup=kb.main_keyboard())

@router.message(MESSAGE.message)
async def send_last(msg: types.Message, state: FSMContext, bot: Bot):
	await state.update_data(message=msg.text)
	data = await state.get_data()
	await state.clear()
	if len(data['message'])==0:
		await msg.answer('Сообщение не содержит информации')
	else:
		await bot.send_message(''.join(data['userid']), text.get_msg(data['message']))
		db.add_msg(message=data['message'], userid=''.join(data['userid']))
		await msg.answer('Сообщение отправлено', reply_markup=kb.main_keyboard())

@router.message(F.text.startswith('/linking'))
async def admin_link_handle(msg: types.Message, bot: Bot):
	if msg.from_user.id in config.admin_ids:
		for u in db.get_users():
			await bot.send_message(u[0], ' '.join(msg.text.split(' ')[1:]))