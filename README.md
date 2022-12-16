# trabalho-redes

Este trabalho possui como finalidade a implementação de uma aplicação de
depósito de arquivo com recuperação. Através do modelo cliente-servidor, a 
aplicação fornece os seguintes serviços:
  i) depósito de arquivos
 ii) recuperação de arquivos
iii) remoção de arquivos

No modo de depósito, o cliente informa ao servidor o arquivo a ser 
depositado e o número de cópias. O servidor guarda a quantidade informada
de cópias do arquivo em locais (abstrações para dispositivos) distintos.

No modo de recuperação, o cliente informa ao servidor o nome do arquivo a
ser recuperado do servidor. O servidor encontrará o arquivo, de algum dos
possíveis locais onde ele esteja armazenado, e o devolve ao cliente.

No modo de remoção, o cliente informa ao servidor o nome do arquivo a ser
removido do servido. O servidor então remove o arquivo solicitado em todas
os locais (abstrações para dispositivos) onde exista uma cópia do mesmo.

A implementação do projeto se deu através da programação, em python, de 
dois algoritmos: server.py e client.py. Como referenciado em seus nomes, 
ambos atuam como instâncias do servidor e cliente da aplicação, 
respectivamente. 

Através do uso de sockets, cliente e servidor comunicam entre si por uma 
conexão TCP. A escolha do protocolo em detrimento do UDP foi consequência 
da necessidade do serviço de transferência confiável de dados (já que a 
aplicação manuseia arquivos, transferindo-os de um hospedeiro a outro). 
Como somente o TCP é capaz de fornecer esse serviço, provendo a garantia
de que os dados serão entregues de um host a outro na ordem correta e sem 
estarem corrompidos, a escolha desse protocolo foi fundamental.

Seguindo as especificações solicitadas e incorporando os conceitos vistos 
em sala de aula, foi possível desenvolver uma aplicação coesa do modelo
cliente-servidor básico, mas fundamental para consolidação das discussões 
da disciplina.
