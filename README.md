# Relatório Trabalho de Redes 2
## Daniel Henrique Vieira - GRR20206889

## Introdução

Este relatório traz os detalhes da implementação do sistema de Blockchain "MiniCoins" proposto no trabalho da disciplina Rede de Computadores 2, da turma de 2025 do professor Elias Duarte. A implementação foi realizada utilizando a linguagem *Python* e a biblioteca *asyncio*. 

## Resumo

A Blockchain "MiniCoins" é composta de um servidor e um cliente. O servidor é responsável por gerenciar a Blockchain e validar transações, enquanto o cliente fica a cargo de enviar blocos com transações a serem adicionadas na Blockchain. Cada bloco enviado pelo cliente deve vir acompanhado de uma *hash* gerada pelo cliente, como prova de trabalho.

## Implementação

A conexão realizada entre o servidor e o cliente é feita utilizando *websockets* com a ajuda da biblioteca *asyncio* (esta foi adicionada no diretório da implementação, visto que a biblioteca não está disponível nas máquinas do DINF). Para realizar a conexão, podemos tanto utilizar o *localhost* quanto um IP estabelecido pelo primeiro argumento ao inicializar o servidor/cliente. 

Para inicializar com o *localhost*, utilizamos:

    python3 server.py

    python3 client.py

Para inicializar com um IP específico, utilizamos:

    python3 server.py <ENDERECO_IP>

    python3 client.py <ENDERECO_IP>

A conexão sempre é feita utilizando a porta 8038.

A implementação da Blockchain possui duas partes principais: o [*server.py*](codigo_txt/server.py.txt) e o [*client.py*](codigo_txt/client.py.txt). Ambos os códigos utilizam as classes definidas em [*classes.py*](codigo_txt/classes.py.txt).

### *classes.py*
Este arquivo possui a definição das classes utilizadas pela Blockchain. Ao todo, utilizamos três classes na implementação: *Transaction*, *Block* e *Blockchain*.

#### *Transaction*
Classe utilizada para representar uma transação em nossa blockchain. 

 |  Atributo  |  Tipo  |  Função  |
 |  --  |  --  |  --  | 
 |  *amount*  |  int  |  Define a quantia de valor transferido na transação | 
 |  *destiny*  |  string  |  Define o usuário que irá receber o valor da transferência  | 
 |  *source*  |  string  |  Define o usuário cujo valor será retirado  | 

Note que a classe não possui um campo que indica o tipo de transação: todas as transações de nossa Blockchain são transações de transferência, bastando apenas indicar a origem e destino dela. 
Caso o cliente deseje "sacar" ou "depositar" uma quantia, basta criar uma instância *Transaction* com o atributo *source*/*destiny* igual a "MiniCoins" (o nome de usuário do servidor).

#### *Block*
Classe utilizada para representar um bloco com transação armazenado em nossa 

 |  Atributo  |  Tipo  |  Função  | 
 |  --  |  --  |  --  | 
 |  *transaction*  |  Transaction  |  Transação armazenada no bloco | 
 |  *previous_hash*  |  string  |  Hash do bloco antecessor deste bloco   | 
 |  *timestamp*  |  datetime  |  Data e hora da criação do bloco  | 
 |  *nonce*  |  int  |  Valor inteiro aleatório definido na criação de um hash válido  | 
 | *hash* | string | Hash do bloco | 
 | *next_block* | *Block* | O bloco posterior a este | 

##### Geração da *hash*
O hash de um bloco é definido (quase) sempre na inicialização de uma instância dessa classe. A única exceção é quando desejamos reconstruir um bloco.
A geração do hash (que é feita pelo método [*utils.py*](codigo_txt/utils.py.txt))é feita utilizando os campos da *transaction*, a *previous_hash*, o *timestamp* e o valor *nonce*, todos unificados em um string único que é então criptografado. O valor de *nonce* é gerado aleatoriamente, e, em seguida, é incrementado de um em um até que um hash válido seja alcançado. Em nossa Blockchain, um hash é considerado válido se ele iniciar com a substring "038".

#### *Blockchain*

Diferente das outras classes, este se encontra no arquivo [*blockchain.py*](codigo_txt/blockchain.py.txt). Esta classe contém a lógica principal de nossa Blockchain, e é responsável por armazenar e validar os blocos das transações.

 |  Atributo  |  Tipo  |  Função  | 
 |  --  |  --  |  --  | 
 |  *first_block*  |  Block  |  Primeiro bloco da Blockchain | 

##### Adicionando blocos

Para adicionar um bloco na Blockchain, a Blockchain primeiro faz duas validações: primeiro, verifica se a operação a adicionar é válida (a conta cujo valor está sendo transferido possui valor suficiente?) e em seguida, verifica se a *hash* é válida, comparando a *previous_hash* do bloco a ser adicionado com a hash do bloco mais recente da Blockchain, além da regra da substring "038". Caso as duas validações sejam bem-sucedidas, o bloco é anexado ao final da blockchain.

### Servidor

A responsabilidade do gerenciamento da Blockchain reside completamente no servidor. Ao inicializar, o servidor cria a Blockchain com um bloco único e *previous_hash* vazio, contendo o valor inicial que transitará pela rede. Após isso, o *websocket* é aberto e fica disponível para o recebimento de requisições por parte dos clientes.
O tipo de requisição é definido pelo campo inteiro *"type"* da mensagem. O servidor aceita os seguintes tipos definido pelo arquivo [*settings.py*](codigo_txt/settings.py.txt): 

 |  Configuração  |  Valor  | 
 |   --   |   --   | 
 |  REQUEST_BLOCKCHAIN_HASH  |   1   | 
 |  REQUEST_ADD_BLOCK  |   2   | 
 |  REQUEST_VERIFY_BLOCKCHAIN  |   3   | 

Quaisquer outros valores são recusados, resultando no servidor enviando uma mensagem de erro ao cliente que requisitou.

#### REQUEST_BLOCKCHAIN_HASH
Para que o cliente possa gerar uma *hash* válida, é necessário utilizar a *hash* do bloco mais recente na Blockchain. A requisição REQUEST_BLOCKCHAIN_HASH indica que o cliente deseja saber qual é a *hash* mais recente.
Ao receber uma requisição deste tipo, o servidor acessa todos os blocos da Blockchain até chegar ao último bloco, e retorna sua *hash*. A resposta desse tipo de requisição consiste em:

 |  Nome |  Tipo  |  Descrição  | 
 |  --  |  --  |  --  | 
 |  status  |  string  |  Indica o resultado da requisição (sempre "success", a não ser que haja uma exceção no código) | 
 |  hash  |  string  |  Hash do bloco mais recente da Blockchain | 

#### REQUEST_ADD_BLOCK

Esse tipo de requisição indica que o cliente deseja adicionar um novo bloco com transação na Blockchain (ver seção Adicionando blocos). A resposta desse tipo de requisição consiste em:

 |  Nome  |  Tipo  |  Descrição  | 
 |  --  |  --  |  --  | 
 |  status  |  string  |  Indica o resultado da requisição ("success" em caso de sucesso, "error" caso o bloco não seja válido)  | 
 |  message  |  string  |  Contém detalhes do resultado da requisição, como motivo do bloco ter sido rejeitado  | 

Note que a hash do bloco a ser adicionado **não é gerada pelo servidor.** A responsabilidade da geração da hash é totalmente do cliente. Isso é feito para garantir que haja uma prova de trabalho por parte do cliente.

#### REQUEST_VERIFY_BLOCKCHAIN
Esse tipo de requisição indica que o cliente deseja verificar se a Blockchain ainda é válida e não há nenhuma inconsistência nos blocos. Essa verificação é feita com o servidor passando entre cada bloco e comparando suas hashes. A resposta desse tipo de requisição consiste em:

 |  Nome |  Tipo |  Descrição  | 
 |  --  |  --  |  --  | 
 |  status  |  string  |  Indica o resultado da requisição ("success" em caso de sucesso, "error" caso o bloco não seja válido)  | 
 |  message  |  string  |  Contém detalhes do resultado da requisição, e em caso de erro, indica o bloco que está comprometido  | 

Esse tipo de requisição faz com que o servidor gere um *log* no terminal com as comparações e hashes dos blocos.

### Cliente

Ao inicializar o cliente, o usuário deve definir seu nome de usuário, que também irá definir sua conta na Blockchain. Com o cliente em execução, podemos escolher a operação que desejamos efetuar. Entre elas, podemos efetuar um "saque", um "depósito", uma "transferência" ou uma "verificação da blockchain".

#### Saque

Para efetuar um saque, o cliente deve informar a quantidade que deseja sacar. Então, o cliente solicita a hash do bloco mais recente para que ele possa gerar o bloco para adicionar na Blockchain.
##### Corpo da requisição
 | Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_BLOCKCHAIN_HASH  |  Indica o tipo de requisição feita para o servidor | 
 | message | string | Contém detalhes do resultado da requisição, e em caso de erro, indica o bloco que está comprometido | 

Feito isso, o cliente envia uma requisição contendo um bloco de transação com o valor desejado, sua própria conta como conta destino e a conta "MiniCoins" como conta de origem.
##### Corpo da requisição
 |  Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_ADD_BLOCK  | Indica o tipo de requisição feita para o servidor | 
 | block |  string contendo o bloco em formato JSON  | O bloco a ser adicionado na Blockchain | 

#### Depósito
Para efetuar um depósito, o cliente deve informar a quantidade que deseja depositar. Então, o cliente solicita a hash do bloco mais recente para que ele possa gerar o bloco para adicionar na Blockchain.
##### Corpo da requisição
 | Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_BLOCKCHAIN_HASH  |  Indica o tipo de requisição feita para o servidor | 
 | message | string | Contém detalhes do resultado da requisição, e em caso de erro, indica o bloco que está comprometido | 

Feito isso, o cliente envia uma requisição contendo um bloco de transação com o valor desejado, a conta "MiniCoins" como conta destino e sua própria conta como conta de origem.
##### Corpo da requisição
 |  Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_ADD_BLOCK  | Indica o tipo de requisição feita para o servidor | 
 | block |  string contendo o bloco em formato JSON  | O bloco a ser adicionado na Blockchain | 

#### Transferência
Para efetuar um saque, o cliente deve informar a quantidade que deseja transferir e a conta de destino. Então, o cliente solicita a hash do bloco mais recente para que ele possa gerar o bloco para adicionar na Blockchain.
##### Corpo da requisição
 | Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_BLOCKCHAIN_HASH  |  Indica o tipo de requisição feita para o servidor | 
 | message | string | Contém detalhes do resultado da requisição, e em caso de erro, indica o bloco que está comprometido | 

Feito isso, o cliente envia uma requisição contendo um bloco de transação com o valor desejado, a conta definida como destino e sua própria conta como conta de origem. Note que não é possível realizar uma transferência de outra conta para a conta do próprio cliente (isso seria uma falha de segurança gravíssima).
##### Corpo da requisição
 |  Campo | Valor | Descrição | 
 | -- | -- | -- | 
 | type |  REQUEST_ADD_BLOCK  | Indica o tipo de requisição feita para o servidor | 
 | block |  string contendo o bloco em formato JSON  | O bloco a ser adicionado na Blockchain | 
