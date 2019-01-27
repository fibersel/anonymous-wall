from aiohttp import web
import random
import asyncio



class alistIterator():
	def __init__(self, collection):
		self.lst = collection
		self.index = 0

	async def __anext__(self):
		while self.index == len(self.lst):
			await asyncio.sleep(1)
		self.index += 1
		return self.lst[self.index - 1]



class alist(list):
	def __init__(self):
		self.lst = []

	def add(self, item):
		self.lst.append(item)

	async def __aiter__(self):
		return alistIterator(self.lst)


messages = alist()

id_ctr = 0



async def handle(request):
	print('REQUEST CAME')	
	return web.FileResponse('index.html')


async def updater(request):

	ws = web.WebSocketResponse()
	await ws.prepare(request)
	print('Websocket connection ready')

	async for msg in messages:
		await ws.send_str(msg)

	return ws

async def reciever(request):
	global id_ctr
	res = await request.text()
	id_ctr += 1
	messages.add(res)
	return web.Response()


port = 8080



app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/updates', updater)
app.router.add_post('/reciever', reciever)
app.router.add_static('/static/', path='./static/', name='static')
web.run_app(app,  port=port)
