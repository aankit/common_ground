
f = open('/Users/Aankit/Documents/SocialDataAnalysis/common_core/toggle', 'r')
whichKey = f.read(1)
whichKey = int(whichKey)
f.close()

def toggleKey(newKey):
	f = open('./toggle', 'w')
	f.write(newKey)
	f.close

if whichKey:
	print 'it was 1'
	toggleKey('0')
else:
	print 'it was 0'
	toggleKey('1')