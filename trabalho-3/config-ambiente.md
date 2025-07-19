
# Configuração do Ambiente para IA-2025-1

Este documento descreve o passo a passo para configurar o ambiente de desenvolvimento para o projeto IA-2025-1.

## Passos para Configuração

### 1. Navegar até o diretório desejado

Primeiro, abra o terminal e navegue até o diretório `Documentos` (ou qualquer outro diretório onde você deseja armazenar o projeto).

```bash
cd Documentos
```

### 2. Criar o diretório do projeto

Crie um novo diretório para o projeto:

```bash
mkdir IA-2025-1
```

### 3. Clonar o repositório

Entre no diretório recém-criado e clone o repositório do projeto:

```bash
cd IA-2025-1/
git clone https://github.com/jjaoguedes/IA-2025-1.git
```

### 4. Navegar até o diretório do trabalho específico

Após o repositório ser clonado, entre no diretório específico do trabalho:

```bash
cd trabalho-3
```

### 5. Instalar o `virtualenv`

Agora, instale a ferramenta `virtualenv` para gerenciar ambientes virtuais. Execute o seguinte comando:

```bash
pip install virtualenv
```

### 6. Criar um ambiente virtual

Crie um ambiente virtual com a versão do Python desejada (Python 3.10):

```bash
python3.10 -m venv venvLTN
```

### 7. Ativar o ambiente virtual

Para ativar o ambiente virtual, execute o comando adequado para o seu sistema operacional:

#### Linux/Mac:

```bash
source venvLTN/bin/activate
```

#### Windows:

```bash
.envLTN\Scriptsctivate
```

### 8. Verificar a versão do Python

Após ativar o ambiente virtual, verifique a versão do Python para garantir que tudo esteja configurado corretamente:

```bash
python --version
```

## Instalação do LTNtorch

É possível instalar o LTNtorch usando pip:

```bash
pip3 install LTNtorch
```

Alternativamente, é possível instalar o LTNtorch clonando este repositório. Nesse caso, certifique-se de instalar todos os requisitos:

```bash
pip3 install -r requirements.txt
```

## Estrutura do Repositório

- `ltn/core.py`: este módulo contém a implementação do framework LTN. Em particular, contém a definição de constantes, variáveis, predicados, funções, conectivos e quantificadores.
- `ltn/fuzzy_ops.py`: este módulo contém a implementação de semântica de lógica fuzzy comum usando primitivas PyTorch.
- `tutorials/`: esta pasta contém alguns tutoriais importantes para começar a codificar em LTN.

## Mais Informações

Para mais informações, acesse o repositório oficial: [LTNtorch no GitHub](https://github.com/tommasocarraro/LTNtorch)
