import os, time, shutil, tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# ===== CONFIG =====
URL_HOME = "https://investidor10.com.br/"
TICKER   = "ITUB4"

HEADLESS = False
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 25
PROFILE_DIR = None

CHROMEDRIVER_PATH = r"C:\Users\aluno\Desktop\Selenium-Investidor10-main\Selenium-Investidor10-main\chromedriver\chromedriver.exe"
DOWNLOAD_DIR = r"C:\Users\aluno\Downloads\unieuro_downloads"

def create_driver(headless: bool = False):
    global PROFILE_DIR
    PROFILE_DIR = tempfile.mkdtemp(prefix="selenium_profile_")

    if not os.path.exists(CHROMEDRIVER_PATH):
        raise FileNotFoundError(f"ChromeDriver não encontrado em: {CHROMEDRIVER_PATH}")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

def clicar_elemento_por_texto(container, texto, timeout=EXPLICIT_WAIT):
    xpath = (
        ".//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÂÃÀÉÊÍÓÔÕÚÇ','abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç'),"
        f"{repr(texto.lower())})] | "
        ".//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÂÃÀÉÊÍÓÔÕÚÇ','abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç'),"
        f"{repr(texto.lower())})] | "
        ".//*[self::li or self::span or self::div][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÂÃÀÉÊÍÓÔÕÚÇ','abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç'),"
        f"{repr(texto.lower())})]"
    )
    el = WebDriverWait(container, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    el.click()
    return True

def tentar_fechar_cookies(driver):
    textos = ["Aceitar", "Aceitar todos", "Concordo", "Entendi", "OK", "Fechar", "Continuar", "Prosseguir", "Permitir"]
    for t in textos:
        try:
            clicar_elemento_por_texto(driver, t, timeout=5)
            time.sleep(0.4)
            return True
        except Exception:
            pass
    return False

def abrir_pagina_acao(driver, ticker: str):
    destino = f"https://investidor10.com.br/acoes/{ticker.lower()}/"
    try:
        driver.get(destino)
        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.XPATH, f"//h1[contains(., '{ticker.upper()}')] | //h2[contains(., '{ticker.upper()}')]"))
        )
        return True
    except TimeoutException:
        driver.get(URL_HOME)
        tentar_fechar_cookies(driver)
        try:
            clicar_elemento_por_texto(driver, "Ações", timeout=8)
            time.sleep(0.5)
        except Exception:
            pass
        try:
            clicar_elemento_por_texto(driver, ticker.upper(), timeout=8)
            return True
        except Exception:
            pass

        driver.get(destino)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h1[contains(., '{ticker.upper()}')] | //h2[contains(., '{ticker.upper()}')]"))
            )
            return True
        except TimeoutException:
            return False

def encontrar_aba_1_dia(container, timeout=EXPLICIT_WAIT):
    tentativas = [
        ".//a[normalize-space(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'))='1 dia']",
        ".//button[normalize-space(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'))='1 dia']",
        ".//*[self::li or self::span or self::div][normalize-space(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'))='1 dia']",
        ".//a[contains(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'),'1 dia')]",
        ".//button[contains(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'),'1 dia')]",
        ".//*[self::li or self::span or self::div][contains(translate(.,'ÂÃÁÀÉÊÍÓÔÕÚÇ','âãáàéêíóôõúç'),'1 dia')]",
        ".//*[@data-range='1d']",
        ".//a[contains(@href, '1d')]",
        ".//li[contains(@class,'active')]/a[contains(@href,'1d')]",
        ".//button[contains(@data-range, '1d')]",
        ".//*[contains(@aria-controls, '1d')]",
        ".//*[contains(@data-tab, '1d')]",
    ]

    fim = time.time() + timeout
    last_err = None
    while time.time() < fim:
        for xp in tentativas:
            try:
                el = container.find_element(By.XPATH, xp)
                return el
            except Exception as e:
                last_err = e
        time.sleep(0.25)

    raise TimeoutException(f"Não localizei a aba '1 dia'. Último erro: {last_err}")

def mostrar_aba_1_dia_e_exibir_cotacao(driver, ticker: str):
    wait = WebDriverWait(driver, EXPLICIT_WAIT)

    tentar_fechar_cookies(driver)

    sec = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//h2[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÂÃÀÉÊÍÓÔÕÚÇ','abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç'), 'cotação {ticker.lower()}')]/ancestor::*[self::section or self::div][1]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sec)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, -120);")

    try:
        aba = encontrar_aba_1_dia(sec, timeout=10)
    except TimeoutException:
        aba = encontrar_aba_1_dia(driver, timeout=8)

    try:
        aba.click()
    except:
        try:
            driver.execute_script("arguments[0].click();", aba)
        except:
            pass

    time.sleep(1.0)

    try:
        # Busca o valor com "R$" ou com classe comum
        cotacao_element = sec.find_element(By.XPATH, ".//*[contains(text(),'R$') or contains(@class,'value')]")
        valor = cotacao_element.text.strip()
        print(f"[COTAÇÃO {ticker.upper()} - 1 DIA] => {valor}")
    except Exception as e:
        print(f"[ERRO] Não foi possível encontrar o valor da cotação: {e}")

def main():
    driver = None
    try:
        driver = create_driver(HEADLESS)
        ok = abrir_pagina_acao(driver, TICKER)
        if not ok:
            print("Não consegui abrir a página da ação.")
            return

        mostrar_aba_1_dia_e_exibir_cotacao(driver, TICKER)

        if not HEADLESS:
            print("Deixando o navegador aberto por 6s para inspeção…")
            time.sleep(6)

    finally:
        if driver:
            driver.quit()
        global PROFILE_DIR
        if PROFILE_DIR and os.path.isdir(PROFILE_DIR):
            shutil.rmtree(PROFILE_DIR, ignore_errors=True)

if __name__ == "__main__":
    main()
