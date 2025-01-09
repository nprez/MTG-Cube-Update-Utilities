import urllib.request, json, csv, sys, time

ignoreDigital = True
ignorePromos = True
ignoreMasterpieces = True
ignoreSecretLair = True
ignoreOldFrames = True
ignoreUniversesBeyond = True
ignoreWhiteBorder = True
keepSameIllustration = True

cubeId = sys.argv[1] #"SmallMagic"
cubeUrl = "https://cubecobra.com/cube/download/csv/" + cubeId
scryfallUrl = "https://api.scryfall.com/cards/"

reprints = []

print(cubeUrl)

#name = 0
#Set = 4
#Collector Number = 5
#maybeboard = 10

text = urllib.request.urlopen(cubeUrl).read().decode('utf-8').split("\n")

cardCount = sum(1 for row in csv.reader(text)) - 2 #ignore header and empty line
print(str(cardCount) + " total cards")

cr = csv.reader(text)

progress = 1 #which chunk of 45 cards we're currently processing
i = -1 #ignore header line

for row in cr:
	i = i + 1
	if(i == progress * 45):
		progress = progress + 1
		print(str(i) + " cards processed...")
	
	if len(row) == 0 or row[0] == "name" or row[10] == "TRUE":
		continue
	
	name = row[0]
	setCode = row[4]
	collectorNum = row[5]
	
	cardUrl = scryfallUrl + setCode + "/" + collectorNum
	
	reprintSets = []
	
	time.sleep(0.1) #rate limiting for scryfall api
	
	with urllib.request.urlopen(cardUrl) as url:
		response = json.load(url)
		releaseDate = response["released_at"]
		printsUrl = response["prints_search_uri"]
		illustration = response["illustration_id"]
		
		with urllib.request.urlopen(printsUrl) as url2:
			response2 = json.load(url2)
			for printing in response2["data"]:
				if ignoreDigital and "paper" not in printing["games"]:
					continue
				if ignorePromos and (
					printing["set_type"] in ["promo", "memorabilia"] or
					printing.get("promo_types") is not None or
					(
						printing.get("frame_effects") is not None and (
							"inverted" in printing["frame_effects"] or
							"showcase" in printing["frame_effects"] or
							"extendedart" in printing["frame_effects"] or
							"etched" in printing["frame_effects"]
						)
					)
				):
					continue
				if ignoreMasterpieces and printing["set_type"] == "masterpiece":
					continue
				if ignoreSecretLair and "Secret Lair" in printing["set_name"]:
					continue
				if ignoreOldFrames and printing["frame"] in ["1993", "1997", "future"]:
					continue
				if ignoreUniversesBeyond and printing.get("security_stamp") == "triangle":
					continue
				if ignoreWhiteBorder and printing["border_color"] == "white":
					continue
				if keepSameIllustration and printing["illustration_id"] != illustration:
					continue
				if "The List" in printing["set_name"]:
					continue
				if(printing["released_at"] > releaseDate):
					reprintSets.append(printing["set"])

	if len(reprintSets) > 0:
		reprints.append(name + " | " + (", ").join(reprintSets))

for reprint in reprints:
	print(reprint)