# Add C:\...\Tor Browser\Browser\TorBrowser\Tor to the current user's environment variables (Windows 10)
from random import randint

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from torrequest import TorRequest
from selenium import webdriver
import time
import requests

if __name__ == '__main__':
    print('Python + TOR')

    UserAgentList = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        # "Mozilla/5.0 (X11; CrOS x86_64 13421.99.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        # "Mozilla/5.0 (X11; CrOS armv7l 13421.99.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        # "Mozilla/5.0 (X11; CrOS aarch64 13421.99.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        # "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
        # "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
        # "Mozilla/5.0 (iPod; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
        # "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
        # "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36"
        ]

    for i in range(0, 1000):
        with TorRequest(proxy_port=9150, ctrl_port=9151, password=None) as tr:

            tr.reset_identity()

            resp = tr.get('http://www.ipecho.net/plain')
            print("Current IP : " + resp.text)

            chrome_options = webdriver.ChromeOptions()
            proxy = 'localhost:9150'
            chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)
            # chrome_options.add_argument('--headless')

            driver = webdriver.Chrome('C:/PATH_TO_CHROMEDRIVER.EXE/chromedriver.exe', options=chrome_options)

            iUserAgent = randint(0, len(UserAgentList)-1)
            newUserAgent = UserAgentList[iUserAgent]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": newUserAgent})
            print("New user agent = " + driver.execute_script("return navigator.userAgent;"))

            # print("Obtention page : Début")
            driver.get("https://youtu.be/bNeCXe0BVIw")
            # print("Obtention page : Fin")

            driver.add_cookie({"name": "CONSENT", "value": "YES+DE.fr+V10+BX"})

            # print("Vérif captcha : Début")
            src = driver.page_source
            if (src.find("Nos systèmes ont détecté un trafic exceptionnel sur votre réseau informatique")) != -1:
                print("Captcha detected ; Aborting and going to next IP address rotation")
                driver.quit()
                continue
            # print("Vérif captcha : Fin")

            # print("Recherche bouton NON MERCI : Début")
            try:
                driver.find_element_by_xpath(
                    "//paper-button[@class='style-scope yt-button-renderer style-text size-small'][.='Non merci']").click()
                print('Bouton "Non Merci" cliqué !')
            except NoSuchElementException:
                print('Bouton "Non Merci" non trouvé')
                pass
            except ElementNotInteractableException:
                print('ElementNotInteractableException')
                pass
            # print("Recherche bouton NON MERCI : Fin")

            time.sleep(5)

            driver.refresh()

            randomTime = randint(60, 120)
            print("Waiting for " + str(randomTime) + " seconds (random between 60 and 120).")
            time.sleep(randomTime)

            try:
                driver.quit()
            except:
                pass
