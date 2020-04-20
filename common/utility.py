import requests
from common import config
import math, random 

def getDictionaryLength(myobj):
    keyLen, valLen = 0, 0
    k_lst = list(myobj.keys())
    v_lst = list(myobj.values())

    for i in range(len(k_lst)):
        keyLen += len(k_lst[i].encode('utf-8'))
        valLen += len(v_lst[i].encode('utf-8'))
    
    final = keyLen + valLen

    return final

def sendOTP(mobilenumber, otpMessage):
    isSent = False

    try:
        # print("INSIDE TRY")    
        url = config.getSMSURL()
        # print("STRING URL: ",str(url))
        usr = config.get("BULKSMS_URL", "user")
        # print("USER AND URL: ","BULKSMS_URL", usr)
        pwd = config.get("BULKSMS_URL", "password")
        sdr = config.get("BULKSMS_URL", "sender")
        typ = config.get("BULKSMS_URL", "type")
        
        # print ("ALL VARIABLES", url, usr, pwd, sdr, typ)
        
        myobj = {'user': str(usr),
            'password': str(pwd),
            'sender': str(sdr),
            'mobile': str(mobilenumber),
            'type': str(typ),
            'message': str(otpMessage)}
        
        conlength = getDictionaryLength(myobj)

        resp = requests.post(url, data = myobj, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(conlength)})

        # print(resp.text)
        isSent = True
    except Exception as ex:
        print ("sendOTP:", ex)

    return isSent
    
def generateOTP():
	digits_in_otp = "0123456789"
	OTP = ""

# for a 4 digit OTP we are using 4 in range
	for i in range(4):
		OTP += digits_in_otp[math.floor(random.random() * 10)]

	return OTP