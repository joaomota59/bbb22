# %%
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import time
from threading import Thread, Lock
import sys
import undetected_chromedriver.v2 as uc

# %%
def start(url, nomeDaVitima):
    s=Service(ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(service=s,options=op)
    driver = uc.Chrome(service=s,options=op)
    driver.get(url)
    input("Faça o Login manualmente na página!\nEm seguida aperte Enter...")
    
    global quantDeVotos

    while True:
        try:
            maxTentativas = 0
            driver.get(url)
            for i in driver.find_elements(By.XPATH,f"//div[contains(text(),'{nomeDaVitima}')]"): 
                try:
                    i.click()
                    print(f"Clicou no(a) {nomeDaVitima}")
                except:
                    pass
            time.sleep(5)
            WebDriverWait(driver, 1).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")))
            driver.find_element(By.XPATH,"//div[contains(text(),'Sou humano')]").click()
            while(True):
                try:
                    driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                    driver.find_element(By.XPATH,"//button[contains(text(),'Votar Novamente')]")

                    lock.acquire() #RC - REGIÃO CRÍTICA
                    quantDeVotos+=1
                    lock.release()

                    print(f"Voto processado! Quantidade de votos: {quantDeVotos}")          
                    time.sleep(4)
                    break
                except:
                    maxTentativas+=1
                    if(maxTentativas==5): break #provavelmente captcha ativo.. recarregar pagina
                    print("Ainda nao processou o voto")
                    time.sleep(2)
                    pass
        except:
            pass
            
    #input("Faça Login na página!\nAperte Enter para continuar...")

    ### FAZER LOGIN MANUAL###

# %%
if __name__ == "__main__":
    procs = []
    numeroDeProcessos = 3 #obs para cada processo é indicado logar com uma conta diferente!

    lock = Lock()
    url = "https://gshow.globo.com/realities/bbb/bbb22/votacao/vote-na-final-do-bbb-22-quem-voce-quer-que-venca-15b3ec29-4d06-4db3-8bd7-d4d4bd050057.ghtml"
    nomeParticipante = "Arthur Aguiar"

    quantDeVotos = 0


    for i in range(numeroDeProcessos):
        proc = Thread(target=start, args=(url, nomeParticipante),daemon=True)
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()



