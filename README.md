# Visione_del_paradiso
## Visione del paradiso

### Introdução

O projeto de engenharia de software consistirá no desenvolvimento de um sistema de gerenciamento de hotéis com funcionalidades de check-in e check-out. O objetivo principal é criar uma solução eficiente e completa para o setor hoteleiro, buscando facilitar o controle e a organização das reservas, além de agilizar o processo de entrada e saída dos hóspedes.

O sistema terá uma interface amigável e intuitiva, permitindo que os funcionários do hotel realizem as tarefas de check-in e check-out de forma simples e rápida. Além disso, o sistema será capaz de armazenar as informações dos hóspedes, como nome, contato, data de entrada e saída, número de quartos reservados, entre outros dados relevantes.

**[Uma das principais funcionalidades do sistema será a geração de relatórios, que permitirão aos gerentes do hotel acompanhar a ocupação dos quartos, a taxa de ocupação, o faturamento diário, entre outras informações importantes para a gestão do estabelecimento. Esses relatórios poderão ser visualizados de forma gráfica e exportados em diferentes formatos, como PDF e planilhas.]**

Além disso, o sistema contará com um módulo de reserva online, que permitirá aos clientes realizar reservas de quartos de forma prática e segura. Os hóspedes poderão consultar a disponibilidade dos quartos, selecionar as datas de entrada e saída desejadas, **[fazer o pagamento online e receber a confirmação da reserva por e-mail.]**

Para garantir a segurança dos dados dos hóspedes, o sistema contará com medidas de proteção, como criptografia de informações e acesso restrito aos dados sensíveis. **[Também serão implementados backups periódicos dos dados, garantindo a recuperação das informações em caso de falhas ou incidentes.]**

Em resumo, o sistema de gerenciamento de hotéis com funcionalidades de check-in e check-out será uma solução completa e eficiente para o setor hoteleiro, facilitando as tarefas diárias dos funcionários e proporcionando uma melhor experiência tanto para os hóspedes quanto para os gerentes do hotel.

*As partes em negrito nesse texto são pontos que poderemos rever dependendo do tempo que teremos para a realização do trabalho.*


### Instalação

Para fazer o programa rodar, você precisará realizar alguns comandos de instalação.

_Primeiramente, certifique-se que o python 3.11 ou superior esteja instalado em sua máquina. Caso não esteja, instale pelo [Site Oficial do Python](https://www.python.org/downloads/)._

#### Passo 1

Antes de tudo, é necessário criar um ambiente virtual python, para que os pacotes não sejam instalados diretamente na sua máquina, evitando assim interferência em outros projeto, faremos isso com o seguinte comando:

```bash
python -m venv <nome_do_ambiente>
```

_Substitua o '<nome_do_ambiente>' por um nome de sua escolha_

#### Passo 2

Ao executar o passo anterior, irá surjir no diretório uma pasta com o nome do ambiente que você escolheu, neste passo iremos ativar esse ambiente, com os seguintes comandos dependendo do seu sistema operacional:

- Linux
```bash
source <nome_do_ambiente>/bin/activate
```
- Windows
```bash
<nome_do_ambiente>/Scripts/activate
```

#### Passo 3

Após o passo 1 e 2, o ambiente já estara pronto para receber os pacotes, neste projeto há um arquivo chamado `requirements.txt`, no qual está os pacotes principais que deverão ser instalados, com este arquivo não é necessário instalar pacote por pacote, basta usar o comando:

```bash
pip install -r requirements.txt
```

#### Passo 4

Para finalizar, é preciso criar manualmente dois arquivos de configurações com o nome: `settings.toml` e `.env`, dentro deles deve estar algumas informações, no primeiro arquivo, duas variáveis de ambiente, desta forma:

```toml
[default]
SECRET_NUM=7
SECRET_KEY='vdp_es_project'
SQLALCHEMY_DATABASE_URI='sqlite:///database.db'
```

no segundo arquivo apenas as variáveis de ambiente que estivermos utilizando, assim:


- Windows
```env
FLASK_APP=api_vdp\main.py
```

- Linux

```
FLASK_APP=api_vdp/main.py
```

_Caso esteja apenas testando, não será necessário preencher os dados do banco de dados em produção._

### Inicialização do projeto

Após todos os passos de instalação realizados, podemos iniciar o servidor flask em modo de desenvolvimento. Para isso utilizamos os comandos:

```bash
flask --debug run
```

O servidor estará aberto em [localhost:5000](localhost:5000)
