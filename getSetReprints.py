import urllib.request, json, sys

cubeId = sys.argv[1] #"SmallMagic"
cubeUrl = "https://cubecobra.com/cube/download/plaintext/" + cubeId

cubeCards = []

print(cubeUrl)

for line in urllib.request.urlopen(cubeUrl):
	card = line.decode('utf-8').replace('\r', '').replace('\n', '')
	if len(card) > 0 and card[0] != '#':
		cubeCards.append(card)

print(str(len(cubeCards)) + " cards")

setId = sys.argv[2] # "m20"
scryfallUrl = "https://api.scryfall.com/cards/search?q=set%3A" + setId
scryfallHeaders = {
    'Accept': '*/*',
	'User-Agent': 'MTGReprintScript/1.0'
}

setCards = []

print(scryfallUrl)

readScryfallPages = True

scryfallReq = urllib.request.Request(scryfallUrl, headers=scryfallHeaders)

while readScryfallPages:
	with urllib.request.urlopen(scryfallReq) as url:
		response = json.load(url)
		for card in response["data"]:
			setCards.append(card["name"])
		readScryfallPages = response["has_more"]
		if readScryfallPages:
			scryfallUrl = response["next_page"]
			scryfallReq = urllib.request.Request(scryfallUrl, headers=scryfallHeaders)

print(str(len(setCards)) + " cards")

reprints = list(set(cubeCards) & set(setCards))
reprints.sort()

for reprint in reprints:
	print(reprint)