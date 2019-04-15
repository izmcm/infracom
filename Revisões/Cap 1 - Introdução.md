## Introdução

### Formas de acesso à internet
* **DSL**: a mais usada, conhecida como banda larga. Usa das linhas telefônicas já existentes para transmitir dados, o que só é possível porque a voz é transmitida por meio de frequências muito baixas, o que deixa as frequências mais altas livras para serem usadas na transmissão de dados. Apesar dos dados e da voz seguirem o mesmo caminho inicialmente, quando chegam ao DSLAM a voz segue para a rede de telefone e os dados para a internet. Seu meio de transmissão é dedicado, ou seja, independente do uso não há queda na taxa de bits de transmissão.

###### Upload 2.5 Mbps e Download de 25 Mbps.

* **Rede a cabo**: ao contrário da DSL que usa a infraestrutura da rede de telefonia, a rede a cabo usa a infraestrutura das companhias de televisão. Possuem uma infraestrutura híbrida que mistura fibra óptica e cabos coaxiais (HFC) e meio de transmissão compartilhado, ou seja, se várias pessoas usarem a rede simultaneamente, a taxa de transmissão diminui.

###### Upload 30 Mbps e Download de 40 Mbps.

* **FTTH**: não faz uso de cabos metálicos como na rede a cabo, usa apenas fibra óptica na sua infraestrutura.
* **Satélite**: usada em áreas onde as outras formas de acesso à internet não estão disponíveis.
* **Dial-up**: rede discada muito usada antigamente que também faz uso da infraestrutura das redes de telefonia.

##### Mídias físicas
* **Cabos coaxiais**: dois cabos de cobre entrelaçados, bidirecional
* **Fibra óptica**: fibra de vidro que transmite dados por pulsos de luz, altíssima velocidade e pequena taxa de erro. Não sofre com eletromagnetismo ou com perda da potência do sinal, o que permite que os dados viajem por distâncias muito longas.
* **Rádio**: sinal viaja no espectro eletromagnético e sem um fio físico, mas sofrem com interferência e obstrução de objetos físicos. Alguns exemplos são wi-fi, 3G, 4G e satélite

### Roteadores e coisas do tipo
Há duas formas de mover dados numa rede de links, elas são:
* **Packet Switching**: nos roteadores do tipo **Store and Forward**, o pacote todo deve chegar ao roteador antes de ser retransmitido. Em roteadores que possuem vários links ligados a eles, há um buffer que "guarda" os pacotes numa fila (queue) para retransmiti-los. Se a taxa de chegada excede a taxa de transmissão e o buffer estiver cheio, os pacotes podem ser perdidos. Aqui, as duas funções principais de um roteador são: determinar o caminho que o pacote deve seguir a partir da leitura do seu header e mover o pacote para o caminho apropriado
* **Circuit Switching**: um exemplo desse tipo de mover dados eram as redes telefônicas tradicionais. Não há compartilhamento de recursos, o que garante a taxa de transmissão de dados constante e o seu uso quando o tempo de entrega da mensagem deve ser fundamental. Em estratégias tradicionais, suporta dois usuários simultaneamente.

###### Num link com capacidade de 2Mbps, onde cada usuário gasta 1Mbps quando está ativo e permanece ativo 10% do tempo, usando o circuit switching poderiamos ter apenas 2 usuários simultaneamente porque cada usuário precisa ter 1Mbps reservado para ele estando ativo ou não. Usando packet switching, deveriamos calcular a probabilidade de dois ou mais usuários estarem ativos ao mesmo tempo num universo de X usuários. Ou seja, o packet switching suporta mais usuários porque leva em conta o tempo de inatividade, mas, apesar disso, sofre com possibilidade de congestionamento e perda de pacotes.

### ISP e IXP
Provedores de acesso à internet que precisam se conectar para que exista transmissão de dados entre eles e, para isso e para tornar essa ligação mais eficiente (que todos não precisem se conectar com todos), há um ISP Regionais que conecta todos os ISPs de uma região. Para que os ISPs Regionais se conectem existe o IXP que funciona como um ponto de troca de informação entre os ISPs. Apesar de concorrentes, os ISPs precisam se conectar porque ninguém vai querer uma internet que só funcione para pessoas dentro do seu ISP.

### Continhas (os delays e otras cositas más)
* **Processamento**: tempo de checagem de erro dos bits e determinação do caminho do pacote, geralmente é menor que milissegundos.
* **Fila**: tempo de espera na fila para transmissão, depende do congestionamento no roteador. 

###### Seja um pacote de L bits sendo transmitido a uma taxa de transmissão de R bits/sec e A a taxa de chegada de pacotes, o delay de fila será de **LA/R**. Se LA/R ~ 0, o atraso será pequeno, LA/R = 1, o atraso será grande e se LA/R > 1, há mais pacotes chegando do que o que pode ser processado, tornando o delay de fila infinito.

* **Transmissão**: tempo que cada bit de um pacote leva para sair do roteador para o link. Seja um pacote de L bits sendo transmitido a uma taxa de transmissão de R bits/sec, o delay de transmissão do pacote será de **L/R** segundos.
* **Propagação**: tempo de viagem do pacote até o próximo nó. Seja D a extensão do link e S a velocidade de propagação no fio (depende do material), o delay de propagação do pacote será **D/S** segundos.

* **Throughput**: taxa (bits/unidade de tempo) em que os bits são transferidos do remetente para o receptor, é a quantidade de pacotes aproveitados. É calculado como o mínimo das taxas: T = min(Rs, Rc, ...)

### Camadas
1. **Aplicação**: HTTP, FTP, SMTP
2. **Transporte**: TCP, UDP
3. **Rede**: IP, protocolos de roteamento
4. **Enlace**: Wi-Fi, Ethernet
5. **Física**: bits no fio