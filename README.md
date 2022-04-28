Checa status atual do pagamento diretamente no mercado pago, atualiza no banco de dados e envia e-mail de confirmação de pagamento pro e-mail.
***
#### Configurações iniciais podem ser encontradas no arquivo main
- A lista é lida separada por /, isso quer dizer que seu sistema deve retornar algo semelhante a 123/321/333.<br>
- Isso pode ser alterado em "Requisicoes/Processar.pegar_lista".<br>

##### Configurando o processamento dos pagamentos
- Pra configurar onde vai ser atualizado as informações sobre o pagamento atual edite o arquivo "Processar.py".<br>
--> Na linha 69 troque "mensalidades" pelo nome da sua tabela.<br>
--> Na linha 79 troque "status" pelo nome da coluna da sua tabela que recebe o status do pagamento.<br>
--> Outras informações podem ser editadas no mesmo arquivo.<br>


- Para configurar o servidor SMTP
--> Edite as informações no arquivo "Processar.py", dentro do init.<br>