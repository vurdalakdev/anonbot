default='ℹ Этот бот создан для приема и отправки анонимных сообщений 👻'

def get_msg(data):
	return f"✅ Вы получили сообщение:\n{data}"

def msgs(data):
	return f"Сообщения:\n{'\n-----\n'.join([f'{i[0]}' for i in data])}"