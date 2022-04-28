def recarregar(self):
    try:
        f = open("fila.ini", "r")
        fila = f.readlines()
        f.close()
        for ordem in fila:
            ordem = ordem.replace("\n", "")
            self.fila_atual.append(ordem)
    except:
        pass