from classes.libs import *
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class Navegador:
    
    
    def __init__(self, usar_selenium=True, navegador='chrome'):
        self.navegador = navegador    
        
        if usar_selenium:
            self.preparar_selenium()    
    
    def preparar_selenium(self):
            if self.navegador == 'chrome':
                options = ChromeOptions()
                # Adicione quaisquer opções de Chrome específicas aqui
                # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                self.driver = webdriver.Chrome()
            elif self.navegador == 'edge':
                options = EdgeOptions()
                # Adicione quaisquer opções de Edge específicas aqui
                # self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
                self.driver = webdriver.Edge()
                
            else:
                raise ValueError("Navegador não suportado. Escolha 'chrome' ou 'edge'.")

    def definir_headers(self, cookie):
        
        self.headers = {
            "authority": "www.olx.com.br",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "max-age=0",
            "cookie": cookie,
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }



    def abrir_site(self, url:str, cookie:str=""):
        """
        Faz uma solicitação GET para o URL fornecido e retorna o conteúdo da página.
        """
        self.definir_headers(cookie=cookie)
        try:
            response = requests.get(url, headers=self.headers, timeout=25)
            response.raise_for_status()  # Isso lançará um erro se o status não for 200
            return response.text
        except requests.HTTPError as e:
            print(f"Erro na solicitação HTTP: {e}")
        except requests.RequestException as e:
            print(f"Erro na conexão: {e}")
        return None

    def abrir_com_selenium(self, url):
        # Inicializa o ChromeDriver
       
        # Acessa uma página
        # url = "https://www.exemplo.com"
        self.driver.get(url)
        
        return self.driver.page_source
    
    def fechar_selenium(self):
        self.driver.quit()