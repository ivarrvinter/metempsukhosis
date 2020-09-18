import json

SMALL_SAMPLE = False
SRC = '../Source/Source.json'
DST = '00.Groups.json'
	
def ExtractGroups(s: dict):
	ret = []
	cGroup = []
	chs = s['children'] if 'children' in s else []
	for ch in chs:
		if 'text' in ch and ';' in ch['text']:
			texts = ch['text'].split(';')
			parts = ExtractGroups(ch)
			tCount = len(texts)
			pCount = len(parts)
			chObjects = []
			if pCount == 0:
				for i in range(0, tCount):
					chObjects.append({
						'text': texts[i]
					})
			elif tCount == pCount:
				for i in range(0, tCount):
					chObjects.append({
						'text': texts[i],
						'children': parts[i]
					})
			else:
				raise Exception('Invalid Number of Child elements, Expected 0 or ' + str(tCount) + ', Found ' + str(pCount))
			if tCount > 0:
				cGroup.append(chObjects[0])
			ret.append(cGroup)
			cGroup = []
			if tCount > 1:
				lastIndex = tCount - 1
				cGroup.append(chObjects[lastIndex])
				if tCount > 2:
					for i in range(1, lastIndex):
						ret.append(chObjects[i])
		else:
			cGroup.append(ch)
	if len(cGroup) > 0:
		ret.append(cGroup)
	return ret

def TransformLines(lines:list):
	d = []
	lineCount = len(lines)
	rng = range(int(lineCount / 2) - 50, int(lineCount / 2) + 50) if SMALL_SAMPLE else range(0, lineCount)
	for i in rng:
		line = lines[i]
		print('\rExtracting Sample ' + str(i) + ' / ' + str(lineCount), end='\t')
		obj = {}
		if 'html' in line:
			obj['html'] = line['html']
			groups = ExtractGroups(line)
			gCount = len(groups)
			for i in range(0, gCount):
				g = groups[i]
				if type(g) is dict:
					groups[i] = [g]
			obj['groups'] = groups
		d.append(obj)
	print()
	return d

f = open(SRC, 'r')
src = json.loads(f.read())
f.close()
dst = TransformLines(src)
f = open(DST, 'w')
f.write(json.dumps(dst, sort_keys=False, indent=4))
f.close()