import json, os, time, requests, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector

class Processar:
    def __init__(self, parent, acao):
        # SMTP
        self.smtp =        "smtp.gmail.com"
        self.porta =       587
        self.email =       "seu email"
        self.senha_email = "sua senha"

        self.parent = parent
        exec(f"self.{acao}()")

    def pegar_lista(self):
        nova = 0
        data = {"key": self.parent.key}
        res = requests.post(self.parent.site, data=data)
        if res.status_code == 200:
            res = res.text.split("/")
            for item in res:
                if not item in self.parent.fila_atual:
                    self.parent.fila_atual.append(item)
                    nova+=1

        if nova > 0:
            print("[+] Nova ordem encontrada!\n")
        else:
            print("[+] Nenhuma ordem nova.\n")

    def processar_fila(self):
        f = open("fila.ini", "r+")
        ft = open("fila_temp.ini", "w+")
        ordens = f.readlines()
        for index, ordem in enumerate(ordens):
            time_atual = time.time()
            timestamp = str()
            ordem_atual = ordem
            checagens = 0
            # PEGAR TIMESTAMP DA ÚLTIMA REQUISIÇÃO
            try:
                ordem_atual = ordem.split("/")
                timestamp = ordem_atual[1]
                ordem_atual = ordem_atual[0]
                checagens = int(ordem_atual[2])
            except:
                ordem_atual = ordem_atual[0]
                pass
            ordem_atual = ordem_atual.replace("\n", "")
            # CHECAR SE FAZ POUCO TEMPO DESDE A ÚLTIMA REQUISIÇÃO E PULAR
            try:
                ultima_checagem = int(time_atual) - int(timestamp)
                if ultima_checagem < 300:  # 5 minutos
                    continue
                elif ultima_checagem < 3600 and checagens > 0: # 1 hora
                    continue
            except:
                pass

            status = requests.get(f"https://api.mercadopago.com/v1/payments/search?sort=date_created&external_reference={ordem_atual}&status=approved&access_token={self.parent.access_token}")
            if status.status_code == 200:
                checagens+=1
                try:
                    # VARIAVEIS
                    dados = json.loads(status.text)
                    status_pagamento = dados["results"][0]["status"]
                    metodo = dados["results"][0]["payment_method_id"]
                    email_pagador = dados["results"][0]["payer"]["email"]
                    email_cliente = str()
                    if status_pagamento == "approved":
                        try:
                            connection = mysql.connector.connect(host=self.parent.host, user=self.parent.login, password=self.parent.senha, database=self.parent.banco)
                            cursor = connection.cursor()
                            cursor.execute(f"SELECT * FROM mensalidades WHERE external_reference={ordem_atual} ORDER BY id DESC LIMIT 1")
                            res = cursor.fetchall()
                            status_atual = res[0][10]
                            if status_atual == "approved":
                                # ITEM JÁ FOI ATUALIZADO #
                                self.parent.fila_atual[index] = "processado"
                                continue
                            id = res[0][0]
                            email_cliente = res[0][1]
                            vencimento = time_atual + 2592000 * res[0][9]
                            sql = f"UPDATE mensalidades SET status='approved', data_ativação='{int(time_atual)}', vencimento='{int(vencimento)}', metodo='{metodo}' WHERE external_reference={ordem_atual} and id={id}"
                            cursor.execute(sql)
                            connection.commit()

                            # ENVIAR EMAIL #
                            enviar_email = smtplib.SMTP(host=self.smtp, port=self.porta)
                            enviar_email.ehlo()
                            enviar_email.starttls()
                            enviar_email.login(self.email, self.senha_email)
                            mensagem_modelo = self.parent.mensagem
                            mensagem_modelo = mensagem_modelo.replace("{mensagem_here}", f"Seu pagamento de nº {ordem_atual} foi processado! <br>Você já pode usar seu produto.")

                            msg = MIMEMultipart()
                            msg['From'] = self.email
                            msg['To'] = email_cliente
                            msg['Subject'] = f"Pagamento nº {ordem_atual} processado."
                            msg.attach(MIMEText(mensagem_modelo, 'html'))
                            enviar_email.sendmail(msg['From'], msg['To'], msg.as_bytes())
                            enviar_email.quit()
                            del msg
                        except Exception as e:
                            ft.write(ordem_atual)
                            ft.write("/" + str(int(time_atual)))
                            ft.write("/" + str(checagens))
                            ft.write("\n")
                    else:
                        ft.write(ordem_atual)
                        ft.write("/" + str(int(time_atual)))
                        ft.write("/" + str(checagens))
                        ft.write("\n")
                except Exception as e:
                    ft.write(ordem_atual)
                    ft.write("/" + str(int(time_atual)))
                    ft.write("/" + str(checagens))
                    ft.write("\n")
            time.sleep(10)
        f.close()
        ft.close()
        os.remove("fila.ini")
        os.rename("fila_temp.ini", "fila.ini")
        self.parent.controle_fila_rodando = False