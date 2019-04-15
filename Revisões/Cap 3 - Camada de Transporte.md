## Camada de Transporte

### UDP
Protocolo mais básico, não garante chegada de pacotes (mas essa garantia pode ser adicionada na camada de aplicação) e nem ordem em que eles chegam. Não hã handshaking entre client e server antes do envio dos pacotes. Única vantagem é rapidez, por isso que é usado em serviços que toleram perda de dados mas que necessitam de rapidez na entrega, como streaming.

* **Checksum**: código guardado no header de um pacote UDP para verificar se houve erro durante a entrega. O valor é calculado antes do envio e armazenado no campo checksum do header, quando chega ao destino o receptor calcula o valor novamente e compara ao checksum do header. Se forem iguais não houve erro.

### TCP
* **Timeout e RTT**: o timeout do TCP, ou seja, o tempo que ele espera para receber a confirmação de chegada de um pacote antes de enviá-lo novamente é dado a partir do RTT, que é o tempo médio de ida e volta de um pacote. 

**Timeout = RTTestimado + 4*RTTmargem**

O RTT estimado é dado por:

**RTTestimado = (1 - alfa) * RTTestimado + alfa * RTTsimples**, onde alfa é igual a 0.125

E o RTTmargem é dado por:

**RTTmargem = (1 - beta) * RTTmargem + beta * |RTTsimples - RTTestimado|**, onde beta é igual a 0.25

###### Além do timeout, o TCP também usa o método de ACKs repetidos para saber se um pacote foi perdido. Isso porque, se um pacote foi perdido, o receptor não consegue reconhecer os pacotes acima daquele número e reenvia o ACK do pacote anterior. Para o sender, receber três ACKs repetidos significa que ele deve reenviar aquele pacote.

* **Controle de fluxo**: o receptor do segmento assim que recebe os dados envia segmentos ACK confirmando o recebimento. No segmento, o receptor envia o tamanho restante do seu buffer para o sender e, de acordo com esse número, o sender pode controlar o fluxo de envio de pacotes a partir da rwnd para evitar perdas ocasionadas por um buffer cheio. Quando o tamanho do buffer informado for 0, o remetente para de enviar pacotes e inicia um cronômetro. O fim do tempo estabelecido faz o remetente enviar um novo pacote pequeno para testar o buffer.

* **Controle de congestionamento**: no controle de fluxo, o sender começa com uma taxa de transmissão pré-estabelecida e vai aumentando-a linearmente até começar a perder pacotes. Quando o sender percebe que perdeu pacotes (seja pelo timeout ou pelos ACKs duplicados), ele corta a taxa de transmissão a partir da cwnd pela metade e recomeça a aumentá-la linearmente. Uma variação desse algoritmo é o Slow Start, que começa subindo a cwnd linearmente até um limite pré-estabelecido e, quando ocorre perda de pacote, pode voltar novamente para a cwnd inicial e recomeçar ou pode cortar a cwnd pela metade e voltar a incrementá-la linearmente.

###### A taxa de transmissão real do TCP será igual a mínimo(rwnd, cwnd)/RTT e o throughput será 3/4 disso.