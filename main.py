import time
from threading import Thread

from Requisicoes.Processar import Processar
from Funcoes import recarregar_lista
from Funcoes import controle_lista

class Mp:

    def __init__(self):
        self.rodando = 0
        ### CONFIGURAÇÕES WEB ###
        self.access_token = "ACCESS TOKEN DO MERCADO PAGO" # ACCESS TOKEN DO MERCADO PAGO
        self.fila_atual = []                               # FILA ATUAL DE PEDIDOS
        self.site = "SITE QUE VAI RETORNAR A FILA"         # LINK DO SEU SISTEMA ONDE SERÁ PEGO A LISTA PARA PROCESSAR
        self.key = "CHAVE DE SEGURANÇA"                    # CHAVE, CASO TENHA DEFINIDO ALGUM SISTEMA DE SEGURANÇA
        ### CONFIGURAÇÕES - BANCO DE DADOS ##
        self.host =  "HOST"
        self.login = "LOGIN"
        self.senha = "SENHA"
        self.banco = "BANCO"

        ### CONFIGURAÇÕES ###
        self.delay = 60                                     # DELAY ENTRE A REQUISIÇÃO DAS THREADS

        ### NÃO MEXER ####
        self.mensagem = str()
        self.controle_fila_rodando = False
        self.controle_lista_rodando = False
        self.iniciar()

    # HTML DE CONFIRMAÇÃO DE PAGAMENTO
    # QUE VAI SER ENVIADO VIA E-MAIL
    def carregar_modelo_email(self):
        f = open("Requisicoes/mensagem_email.ini", "r")
        self.mensagem = f.read()
        f.close()
        self.mensagem = self.mensagem.replace("ï»¿", "")
        return

    # SEMPRE QUE UMA LISTA É CARREGADA É SALVA NO ARQUIVO
    # PARA CASO O Mp PARE DE RODAR ELE RECARREGUE A LISTA ANTERIOR
    def recarregar_lista(self):
        recarregar_lista.recarregar(self)
        if len(self.fila_atual) > 0:
            print("[+] Lista carregada.")
        else:
            print("[+] Lista vazia.")

    # THREAD QUE PROCURA NOVOS PAGAMENTOS NO SEU SISTEMA
    def controle_lista(self):
        print("[+] Thread iniciada. [CONTROLE LISTA]")
        while self.rodando == 1:
            if not self.controle_fila_rodando:
                self.controle_lista_rodando = True
                controle_lista.controle(self)
                time.sleep(self.delay + 5)
            else:
                print("controle de fila sendo processado, aguardando...")
                time.sleep(5)

    # THREAD QUE PROCESSA A FILA ATUAL
    # BUSCANDO A SITUAÇÃO DE PAGAMENTO ATUAL NO MERCADO PAGO
    def controle_fila(self):
        print("[+] Thread iniciada. [CONTROLE FILA]")
        while self.rodando == 1:
            if not self.controle_lista_rodando:
                self.controle_fila_rodando = True
                Processar(self, "processar_fila")
                time.sleep(self.delay)
            else:
                print("controle de lista sendo processado, aguardando...")
                time.sleep(5)

    # INICIAR THREADS #
    def iniciar(self):
        print("[+] Iniciado.")
        self.rodando = 1
        self.carregar_modelo_email()
        self.recarregar_lista()
        Thread(target=self.controle_lista).start()
        Thread(target=self.controle_fila).start()

if __name__ == "__main__":
    Mp()