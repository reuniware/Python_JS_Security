# Add C:\...\Tor Browser\Browser\TorBrowser\Tor to the current user's environment variables (Windows 10)
from selenium.common.exceptions import NoSuchElementException
from torrequest import TorRequest
from selenium import webdriver
import time
import requests

if __name__ == '__main__':
    print('Python + TOR')

    for i in range(0, 1000):
        with TorRequest(proxy_port=9150, ctrl_port=9151, password=None) as tr:

            tr.reset_identity()

            resp = tr.get('http://www.ipecho.net/plain')
            print("Current IP : " + resp.text)

            chrome_options = webdriver.ChromeOptions()
            proxy = 'localhost:9150'
            chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)
            # chrome_options.add_argument('--headless')

            driver = webdriver.Chrome('C:/PATH_TO_CHROMEDRIVER_EXE/chromedriver.exe', options=chrome_options)

            print("Obtention page : Début")
            driver.get("https://youtu.be/00000000000")
            print("Obtention page : Fin")

            driver.add_cookie({"name": "CONSENT", "value": "YES+DE.fr+V10+BX"})

            print("Vérif captcha : Début")
            src = driver.page_source
            if (src.find("Nos systèmes ont détecté un trafic exceptionnel sur votre réseau informatique")) != -1:
                print("Captcha detected ; Aborting and going to next IP address rotation")
                driver.quit()
                continue
            print("Vérif captcha : Fin")

            print("Recherche bouton NON MERCI : Début")
            try:
                driver.find_element_by_xpath("//paper-button[@class='style-scope yt-button-renderer style-text size-small'][.='Non merci']").click()
                print('Bouton "Non Merci" cliqué !')
            except NoSuchElementException:
                print('Bouton "Non Merci" non trouvé')
                pass
            print("Recherche bouton NON MERCI : Fin")

            time.sleep(5)

            driver.refresh()

            time.sleep(120)

            driver.quit()

