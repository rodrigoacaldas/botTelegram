import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

class TelegramBot:
	def __init__(self):
		token = os.getenv("TOKEN")
		self.url_base = f'https://api.telegram.org/bot{token}/'
		list_all_messages = requests.get(self.url_base+'getUpdates')
		print(list_all_messages.json())

	#iniciar o bot
	def iniciar(self):
		update_id = None
		while True:
			atualizacao = self.obter_mensagens(update_id)
			mensagens = atualizacao['result']
			if mensagens:
				for mensagem in mensagens:
					update_id = mensagem['update_id']
					#add bot em um grupo
					if 'my_chat_member' in mensagem:
						chat_id = mensagem['my_chat_member']['chat']['id']
						resposta = self.criar_resposta_group_start(mensagem['my_chat_member'])
						self.enviar_mensagem(resposta, chat_id)

					#Envia comando para o BOT
					elif 'entities' in mensagem['message']:
						chat_id = mensagem['message']['chat']['id']
						resposta = self.criar_resposta_group(mensagem['message'])
						self.enviar_mensagem(resposta,chat_id)

					#BOT recebe mensagem em conversa
					else:
						chat_id = mensagem['message']['from']['id']
						resposta = self.criar_resposta_chat(mensagem['message'])
						self.enviar_mensagem(resposta,chat_id)

	#Obtem as mensagens novas
	def obter_mensagens(self,update_id):
		link_requisicao = f'{self.url_base}getUpdates?timeout=100'
		if update_id:
			link_requisicao = f'{link_requisicao}&offset={update_id+1}'
		resultado = requests.get(link_requisicao)
		print(resultado.json())
		return json.loads(resultado.content)

	#Cria uma resposta para chats
	def criar_resposta_chat(self,mensagem):
		texto = mensagem['text']
		primeiraMensagem = mensagem['message_id']
		if primeiraMensagem == '1':
			resposta = f'Bem vindo ao Bot da Vapt Fotos{os.linesep}O que você deseja saber?'
			return resposta
		elif texto == '1':
			return 'Você digitou 1'
		else:
			return f'Desculpe não entendi o comando: {texto}'

	#Mensagem quando incluir o bot em um grupo
	def criar_resposta_group_start(self,mensagem):
		id = mensagem['chat']['id']
		return f'Eu sou o Bot da VaptFotos!{os.linesep}O nosso chat id é:{os.linesep}{id}'


	# Mensagem quando incluir o bot em um grupo
	def criar_resposta_group(self, mensagem):
		id = mensagem['chat']['id']
		if mensagem['text'] == '/start':
			return f'Bem vindo ao Bot da VaptFotos!{os.linesep}O seu chat id é:{os.linesep}{id}'
		else:
			return 'Esse comando não existe'

	#Enviar mensagem
	def enviar_mensagem(self,mensagem,chat_id):
		link_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={mensagem}'
		print(link_envio)
		requests.get(link_envio)


bot = TelegramBot()
bot.iniciar()