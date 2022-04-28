import re
from Requisicoes.Processar import Processar


def controle(self):
    Processar(self, "pegar_lista")
    f = open("fila.ini", "r+")
    fila = f.readlines()
    for index, item in enumerate(self.fila_atual):
        item = item.replace("\n", "")
        if item == "processado" or item == "":
            self.fila_atual.pop(index)
            continue

        if not re.search(str(item), str(fila)):
            print("[+] Nova ordem adicionada a fila.")
            f.write(item)
            f.write("\n")
    f.close()
    self.controle_lista_rodando = False