from classes.Navegador import Navegador
from classes.libs import * 
import json
from icecream import ic 


class Olx():
    
    lista_itens = pd.DataFrame()
    
    def __init__(self, executar_processos=True, qtde_paginas:int =10, delay_entre_acessos:int = 2, usar_selenium=True, navegador_abrir="edge", url:str=""):
        print("Iniciando site OLX")
        self.qtde_paginas = qtde_paginas
        self.delay_entre_acessos = delay_entre_acessos
        self.usar_selenium = usar_selenium
        self.navegador_abrir = navegador_abrir
        self.url = url
        if executar_processos:
            if usar_selenium:
                self.instanciar_selenium()
            self.preparar_urls()
            self.acessar_urls()
            # self.acessar_urls()

    def instanciar_selenium(self):
        self.navegador = Navegador(usar_selenium=self.usar_selenium, navegador=self.navegador_abrir)
    
    def preparar_urls(self, ):
        ic()
        # self.url = "https://www.olx.com.br/imoveis/venda/estado-pr?f=p&q=apartamento"
        # https://www.olx.com.br/imoveis/venda/estado-pr?f=p&q=apartamento&o=2
        if "?" in self.url:
            self.lista_urls = [f"{self.url}&o={str(i +1)}"  for i in range(self.qtde_paginas) ]
        else:
            self.lista_urls = [f"{self.url}?&o={str(i +1)}"  for i in range(self.qtde_paginas) ]
        
    def acessar_urls(self):
        ic()
        for url in self.lista_urls:
            print(url)
            conteudo = self.navegador.abrir_com_selenium(url)
            self.converter_conteudo(conteudo)
            sleep(self.delay_entre_acessos)
            
            
    def converter_conteudo(self, conteudo):
        ic()
        # print()
        soup = BeautifulSoup(conteudo, 'lxml')
        # soup = BeautifulSoup(self.navegador.driver.page_source, 'lxml')
        script = soup.find('script', {'id': '__NEXT_DATA__'})
        itens = pd.DataFrame(json.loads(script.text)["props"]["pageProps"]["ads"])
        
        resultados = pd.DataFrame()
        ## pegar properties e deixar na mesma linha que cada imóvel
        for index, row in itens.iterrows():
            try:
                pivot_table = pd.DataFrame(row["properties"]).pivot_table( values="value",columns="label", aggfunc="max")
                # pivot_table.reset_index(inplace=True)
                pivot_table["index"] = index
                resultados = pd.concat([resultados, pivot_table])
            except Exception as err:
                print(err)
                pass
            
        
        itens = (itens.reset_index()
        .merge(resultados, on=["index"], how="left")
        )
        self.lista_itens = pd.concat([self.lista_itens, itens])
        