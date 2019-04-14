## Camada de Aplicação

### Arquiteturas
* **Cliente-servidor**: o servidor permanece sempre ativo e possui um IP permanente pelo qual os clients se conectam, sem estabalecer conexões diretas um com os outros
* **P2P**: muito usada nos serviços de torrent, é como se todos fossem clients e servers ao mesmo tempo. Todos podem requerer e prover serviços para qualquer outro sem um servidor central, apenas se conectando diretamente. É auto-escalável: quando um novo peer chega, além de pedir serviços ele também fornecerá.

##### Processos são programas em execução dentro de um host. Processos de clients iniciam a comunicação com o server, enquanto os processos de server aguardam serem requeridos. Em arquiteturas P2P, cada peers roda os dois processos. O processo de envio-recebimento de mensagens é um socket, ou seja, o socket funciona como a "porta" que conecta a camada de aplicação com a camada de transporte. Para receber mensagens, os processos precisam de um identificador que será um endereço de IP e uma porta.

### O que os apps precisam da camada de transporte?
* **Integridade de dados**: alguns apps suportam alguma perda de dados (streaming) enquanto outros necessitam de uma transferência 100% confiável (e-mail)
* **Tempo**: alguns apps precisam de pouco delay para serem funcionais (skype) enquanto outros podem suportar um pouco mais (e-mail)
* **Throughput**: alguns apps precisam de uma taxa de transferência mínima para trabalhar (streaming) enquanto outros não (e-mail)
* **Segurança**

### E o que a camada de transporte faz?
* **TCP**: e-mail, transferência de arquivos, web
    - Transporte confiável de dados
    - Controle de fluxo: remetente não sobrecarrega o receptor
    - Controle de congestionamento: funciona quando a rede está sobrecarregada
    - Orientado à conexão: necessário setup entre client e server
    - Não fornece garantia de tempo, throughput ou segurança

* **UDP**: streaming, jogos online
    - Não fornece nada que o TCP fornece (controle de fluxo, de congestionamento, transporte confiável)
    - É rápido!!!!!!

* **SSL**: providencia segurança ao TCP

### WEB
* **HTTP**: protocolo do modelo client-server que é usado para acessar páginas na web. 
    - Client inicia uma conexão TCP (cria um socket) com o server através da porta 80
    - Server aceita conexão TCP
    - A mensagem é trocada entre Client e Server
    - Conexão fechada

###### HTTP Persistente envia multiplos objetos numa única requisição, enquanto o Não Persistentes precisa de mútiplas conexões para enviar vários objetos

* **RTT**: tempo  que um pacote demora para ir do client pro server e voltar. No HTTP Não Persistente, o tempo de resposta será **2RTT + tempo de transmissão do arquivo** para cada objeto referenciado. No HTTP Persistente, o server deixa a conexão aberta após o envio da primeira resposta e, por isso, não há a necessidade de abrir uma nova conexão a cada objeto referenciado encontrado.

* **Cookies**: o cookie fica salvo no computador do client e funciona no sentido de fazer a experiência de um site mais personalizada. O site salva um ID no computador do client e sempre que esse computador se conectar ao server e enviar esse ID ao server, o database do site retornará o conteúdo q deve ser mostrado para o client.

* **Cache**: o client pede o objeto ao cache: se o cache possui o objeto já retorna pro client, se ele não possui, pede para o server. O cache funciona como client e server ao mesmo tempo e existe para diminuir o tempo de resposta e reduzir o tráfico para o link original.

Para ver a eficiência de um cache, vamos assumir:
    - um objeto de 0.1 Mbits
    - uma taxa de request para o server original de 15 requests/sec
    - uma taxa de transmissão pro browser de 1.50 Mbps
    - RTT do roteador para o server original de 2 segundos
    - uma taxa de acesso ao link de 1.54 Mbps
    - uma taxa de acesso a LAN de 1000 Mbps

SEM CACHE: 
    - **utilização da LAN** = (taxa de request para o server original * tamanho do request)/taxa de acesso a LAN = (15 requests/sec * 0.1Mbit)/1000 Mbps = 15%
Como a utilização da LAN é baixa, o delay que ela causa é desprezado.
    - **utilização do link** = (taxa de request para o server original * tamanho do request)/taxa de acesso ao link = (15 requests/sec * 0.1Mbit)/1.54 Mbps = 97%
Como a utilização do link é muito alta, o delay é exponencial, chegando a casa dos minutos.

No fim, o tempo total será = delay da internet (2 sec) + delay da LAN (desprezado) + delay do link (minutos).
A única forma de resolver o problema do altíssimo delay do link sem o cache é aumentando a taxa de acesso ao link em 100x, o que levaria seu tempo para milissegundos (desprezado), mas isso é extremamente caro.

COM CACHE:
Considerando um cache com taxa de acerto de 40%, pode-se dizer que cerca de 40% dos pedidos serão atendidos quase que instataneamente por causa da alta taxa de acesso da LAN. Em 60% dos casos apenas será necessário recorrer ao servidor original:
    - **utilização do link** = (taxa de request para o server original * tamanho do request * taxa de erro do cache)/taxa de acesso ao link = (15 requests/sec * 0.1Mbit * 0.6)/1.54 Mbps = 58%
Uma utilização de 58% do link faz com que o delay seja desconsiderado.

No fim, o tempo total será = 0.6*2 sec = 1.2 segundos, já que o server original será acionado apenas 60% das vezes.
