import subprocess
import threading

i=0

def myloop():
    global i
    i=i+1
    print(i)
    CurlUrl = "curl --request GET 'https://targetwebsitetochange0123.fr/'"
    status, output = subprocess.getstatusoutput(CurlUrl)
    #print(status)
    #print(output)

while True:
    try:
        threading.Thread(target=myloop).start()
    except:
        pass
