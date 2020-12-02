Project about ip rotation with TOR + user agent rotation ;)

Install tor browser + add path to tor.exe in environment variable Path (for user or system)

Install chromedriver

Modify code (for chromedriver path, and strings, eg. for Captcha detection)

Start Tor Browser

Run the script

You will have IP rotation + User Agent rotation and will be able to generate traffic for eg. a Youtube Video ;)

That does not work on Windows 7 (It might be due to Python39 that cannot be installed on Win7)...

That works on Windows 10 (and has been developped on Win10).

For Linux (Kali Linux) :

Update to latest python version with : sudo apt-get install python3

Download http://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip

With : wget -N http://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip

Then unzip with : unzip chromedriver_linux64.zip

Then install missing dependencies with : pip3 install ...

Then modify path to chromedriver in the main.py file (eg. "./chromedriver" if "main.py" is in the same path of the unzipped "chromedriver" file)

Then run it with : python3 main.py

And have fun !


