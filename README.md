# trabalho-redes

Então, coloquei uns arquivos básicos commo referência do funcionamento de um servidor e cliente simples em python, tendo como base um vídeo que vi no yt
Os algoritmos que estaremos desenvolvendo estão fora da pasta /referencias.

Adotei algumas definições e pressupostos:
* O cliente enviará mensagens do formato "operação nome_do_arquivo".
* As operações serão:
  * DEP := Depositar arquivo
  * REC := Recuperar arquivo
  * DEL := Deletar arquivo
* Aplicações diferentes do servidor serão instanciadas em portas diferentes. Daí a separação do algoritmo do servidor em server.py e n_servers.py.
* Os arquivos sempre serão armazenados, consultados e deletados nos diretórios do tipo dir/{PORT} ("dir" mesmo, por extenso. PORT se refere à porta de uma dada instância de um servidor)
* Instâncias diferentes do servidor podem receber consultas de mais de um cliente simultaneamente

Terminei (porcamente, eu acho) a implementação de server.py. Infelizmente preciso da aplicação completa (ou do cliente, pelo menos) para fazer os testes. Estou exausto enquanto escrevo isso, preciso desesperadamente dormir. Façam o que puderem para implementar o resto enquanto eu não acordo, por favor.
