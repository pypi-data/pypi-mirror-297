
import os
import sys
import time
import hashlib
import threading

import uvicorn
from fastapi import FastAPI, Request, Response, status, Body

from petdb import PetDB, PetCollection, PetArray
from petdb.service.api import DEFAULT_PORT
from petdb.service.qlock import QLock

if sys.platform != "linux":
	raise Exception("PetDB.service supports only Linux system")

STORAGE_PATH = "/var/lib/petdb"
if not os.path.exists(STORAGE_PATH):
	os.makedirs(STORAGE_PATH, exist_ok=True)

db = {}
locks = {}
app = FastAPI()

def get_db(name: str) -> PetDB:
	if name not in db:
		db[name] = PetDB.get(os.path.join(STORAGE_PATH, name))
	return db[name]

def get_lock(name: str) -> QLock:
	if name not in locks:
		locks[name] = QLock()
	return locks[name]

@app.post("/collections")
def get_collections(request: Request):
	return request.state.db.collections()

@app.post("/drop")
def drop_collections(request: Request):
	request.state.db.drop()

@app.post("/drop/{name}")
def drop_collection(request: Request, name: str):
	request.state.db.drop_collection(name)

@app.post("/mutate/{name}")
def mutate(request: Request, name: str, mutations: list[dict] = Body(embed=True)):
	array = request.state.db.collection(name)
	for mutation in mutations:
		array: PetArray = array.__getattribute__(mutation["type"])(*mutation["args"])
	return array.list()

@app.post("/insert/{name}")
def insert(request: Request, name: str, doc: dict = Body(embed=True)):
	return request.state.db.collection(name).insert(doc)

@app.post("/insert_many/{name}")
def insert_many(request: Request, name: str, docs: list[dict] = Body(embed=True)):
	return request.state.db.collection(name).insert_many(docs)

@app.post("/update_one/{name}")
def update_one(request: Request, name: str, update: dict = Body(embed=True), query: dict = Body(embed=True)):
	return request.state.db.collection(name).update_one(update, query)

@app.post("/update/{name}")
def update(request: Request, name: str, update: dict = Body(embed=True), query: dict = Body(embed=True)):
	return request.state.db.collection(name).update(update, query)

@app.post("/remove/{name}")
def remove(request: Request, name: str, query: dict = Body(embed=True)):
	return request.state.db.collection(name).remove(query)

@app.post("/clear/{name}")
def clear(request: Request, name: str):
	return request.state.db.collection(name).clear()

def cache_monitor():
	while True:
		print("start cache checking...")
		now = int(time.time())
		instances = PetCollection.instances()
		for path in list(instances.keys()):
			dbname = os.path.relpath(path, STORAGE_PATH).split(os.sep)[0]
			with get_lock(dbname):
				print(f"check {instances[path]["instance"].dbname}...")
				if now - instances[path]["created"] > 3 * 24 * 3600:
					print(f"clear {instances[path]["instance"].dbname}")
					del instances[path]
		time.sleep(24 * 3600)

def run(port: int = DEFAULT_PORT, password_hash: str = ""):

	@app.middleware("http")
	async def authentication(request: Request, call_next):
		body = await request.json()
		if hashlib.sha256(body["password"].encode("utf-8")).hexdigest() == password_hash:
			with get_lock(body["dbname"]):
				request.state.db = get_db(body["dbname"])
				return await call_next(request)
		return Response(status_code=status.HTTP_401_UNAUTHORIZED)

	threading.Thread(target=cache_monitor).start()

	uvicorn.run(app, host="127.0.0.1", port=port)
