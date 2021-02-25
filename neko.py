#!/data/data/com.termux/files/usr/bin/python
# Nekopoi / zippyshare downloader
# dtz-aditia 2021.02
# how to find zippyshare url?
# see -> https://github.com/dtz-aditia/zp-finder

from bs4 import BeautifulSoup, re, sys, os
from requests import logging, Session
from tqdm import tqdm
from time import sleep

logging.basicConfig(format="%(message)s", level=logging.INFO)

class NekoExtractor(object):
	def __init__(self, file):
		self.file = file
		self.session = Session()
		self.session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
		self.__main__(self.file, cek=True)

	def _extract(self, url):
		logging.info(
			f" [*] !- MENGEKSTRAK LINK UNDUHAN -> {url}")
		page = self.session.get(url).text
		res = re.search(r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', page)
		if res is not None:
			res = res.groupdict()
			return {
				"url": re.search(r"(^https://www\d+.zippyshare.com)", url).group(1) +
				res["i"] + str(eval(res["t"])) + res["f"]}
		else:
			return False

	def _getinfo(self, url):
		page = self.session.get(url)
		soup = BeautifulSoup(page.text,"html.parser")
		d = {}
		for c in soup.findAll("div",class_="center"):
			if "Name:" in str(c):
				dat = c.text.strip().split('\n')
				if len(dat) != 0:
					for k in dat[2:]:
						if ":" not in k:
							d["name"] = k
							continue
						k = k.split(':')
						d[k[0]] = k[1]
				else:
					break
		if "name" in d.keys():
			d.update({"url":url})
			return d
		else:
			return False

	def download(self, url, name):
		req = self.session.get(url, stream=True)
		path = input(" [*] !- PATH SAVE -> ")
		progres = tqdm(
			total=int(
				req.headers.get(
					'content-length',
					0)),
			unit="B",
			unit_scale=True)
		if not name.endswith(".mp4"):
			name = f"{name}.mp4"
		with open(path+name,"wb") as f:
			for data in req.iter_content(1024):
				progres.update(len(data))
				f.write(data)
		progres.close()
		logging.info(
			f" [*] !- FILE SAVED -> {path}/{name}")
		sleep(0.7)

	def _write(self, _dats, name="logs", Fail=False):
		if isinstance(_dats, list):
			logging.info(
				" [*] !- MENYIMPAN LOGS!")
			if Fail:
				name = "logs-failed"
			with open(name,"w") as f:
				f.write(
					str(_dats))

	def _cekrek(self, file):
		data = []
		fail = 0
		failed = []
		f = open(file).read().splitlines()
		for demo, koi in enumerate(f,start=1):
			cuki = self._getinfo(koi)
			logging.info(
				f" [*] ({demo} OF {len(f)}) !- ADD -> {koi}")
			if cuki:
				data.append(cuki)
			else:
				print(
					f" [*] ({demo} OF {len(failed)} !- DELETE -> {koi}")
				failed.append(koi)
				fail +=1
				continue
		if len(data) != 0:
			with open(file,"w") as f:
				f.write(
					"\n".join([i["url"] for i in data]))
			self._write(data)
		if len(failed) != 0:
			self._write(failed, Fail=True)

	def _cekupdet(self, file, _logs):
#		if verify is True:
		logging.info(" [*] !- MEMERIKSA UPDATE LIST!")
		if os.path.isfile("logs"):
			f = open(file).read().splitlines()
			for v, dk in enumerate(f,start=1):
				if len(dk) != 0 and dk not in str(_logs):
					logging.info(f" [*] ++ Add -> {dk} -> {v}")
					_cu = self._getinfo(dk)
					if _cu:
						_logs.append(_cu)
			with open(file,'w') as f:
				f.write("\n".join([i["url"] for i in _logs]))
			self._write(
				_logs)

	def __main__(self, file, cek=False):
		global ceks
		if os.path.isfile("logs"):
			logging.info(
				" [*] !- LOGS FILE DI TEMUKAN!")
			ceks = eval(open("logs").read())
			if cek is True:
				self._cekupdet(
					file, ceks)
		else:
			logging.info(
				" [*] !- LOGS TIDAK DI TEMUKAN, MEMULAI MENDAPATKAN INFO!")
			self._cekrek(file)
			self.__main__(file)
		sleep(1)
		os.system("clear")
		logging.info(
			"\n                ZippyShare Extractor\n"
			"            Author : dtz-aditia © 2021.02\n"
			"          Find Me : https://t.me/aditia_dtz\n"
			"      -------------------------------------------\n")
		for k,v in enumerate(ceks,start=1):
			print(f"{k}. {v['name']}")
		while True:
			try:
				ces = int(input("\n [*] !- PILIH -> "))
				if ces != '' and (ces-1) < len(ceks):
					index = ceks[ces-1]
					print(
						f"\n [*] NAME : {index['name']}\n"
						f" [*] SIZE : {index['Size']}\n"
						f" [*] UPLOADED: {index['Uploaded']}\n")
					dl = input(" [*] !- DOWNLOAD ? , Y/N -> ")
					if dl.lower() == "y":
						self.download(self._extract(index["url"])["url"], index["name"])
						self.__main__(file, cek=False)
					elif dl.lower() == "n":
						self.__main__(file)
					else:
						break
				else:
					logging.info(" [*]\x1b[91m !- KELEBIHAN!")
					break
			except:
				break

if __name__=="__main__":
	if len(sys.argv) < 2:
		sys.exit("Usage : neko.py <file_list>")
	else:
		NekoExtractor(sys.argv[1])

# contact : https://t.me/aditia_dtz
