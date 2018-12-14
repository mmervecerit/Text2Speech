import http.client, urllib.parse, json,requests,argparse,time
from gtts import gTTS

apiKey = "YOUR_API_KEY"
params = ""
headers = {"Ocp-Apim-Subscription-Key": apiKey}
#GET TOKEN WITH YOUR API KEY with auth
AccessTokenHost = "westeurope.api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"
print ("Connect to server to get the Access Token")
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
conn.close()
accesstoken = data.decode("UTF-8")
#Microsoft Text to Speech
def MSTTS(inputtext):
	URL="https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
	headers={'Authorization':'Bearer '+accesstoken,'Content-Type':'application/ssml+xml','X-Microsoft-OutputFormat':'riff-24khz-16bit-mono-pcm','User-Agent':'SpeechIsY'}
	data="<speak version='1.0' xml:lang='tr-TR'><voice xml:lang='tr-TR' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (tr-TR, SedaRUS)'>"+inputtext+"</voice></speak>"
	r=requests.post(URL,headers=headers,data=data.encode('utf-8'))
	if r.status_code == 200:
		with open('Microsoft'+str(int(time.time()))+'.wav', 'wb') as audio:
			audio.write(r.content)
	else:
		print("\nStatus code: " + str(r.status_code) + "\nBir sıkıntı var, key ve url ini kontrol edebilirsin.\n")
'''
example commands: python texttoSIsY.py -ms -g -f ./ReadME.txt
python texttoSIsY.py -ms
python texttoSIsY.py -g
python texttoSIsY.py -ms -g

'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-ms","--Microsoft",action="store_true")
	parser.add_argument("-g","--Google",action="store_true")
	parser.add_argument("-f","--file")
	args=parser.parse_args()
	inputfile=args.file
	MS=args.Microsoft
	G=args.Google
	F=args.file
	if F is not None:
		text=open(inputfile,encoding='utf-8')
		inputtext=text.read()
	else:
		inputtext="Direkt text olarak vermek isterseniz buraya yazıp okutabilirsiniz"	
	
	if MS:
		MSTTS(inputtext)

	if G:
		speech=gTTS(inputtext, lang="tr")
		speech.save('Google'+str(int(time.time()))+'.mp3')
