# Solução LTNTorch - Questão 1

**Classificar um tabuleiro fechado:** Dado um tabuleiro qualquer 4x4 ou 9x9, que esteja **fechado**, i.e. com todas as células ou posições preenchidas, que deve ser lido de um aquivo csv, seu sistema deve responder com 1 para o caso de o tabuleiro estar corretamente preenchindo e 0 caso contrário (tiver violado algumas das restrições/constraints).	

## Nossa Solução

**Descrição geral:** Dada uma matriz `4x4` ou `9x9` representando um Sudoku fechado (sem células vazias), o sistema lê esse tabuleiro de um arquivo `.csv` e utiliza **fórmulas lógicas fuzzy** para verificar se as **restrições do Sudoku** são atendidas: 
- Cada célula deve conter **exatamente um número**;
- Cada número deve aparecer **uma vez por linha**;
- Cada número deve aparecer **uma vez por coluna**;
- Cada número deve aparecer **uma vez por bloco**.

## Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [PyTorch](https://pytorch.org/)
- [LTNtorch no GitHub](https://github.com/tommasocarraro/LTNtorch)

## Estrutura esperada do arquivo CSV

O Sudoku deve estar salvo como um arquivo `.csv` com números de 1 a N (onde N = 4 ou 9), sem espaços ou células vazias.

**Exemplo de arquivo para Sudoku 4x4 (`sudoku4x4_valid1.csv`):**
```
1,2,3,4 
3,4,1,2
2,1,4,3
4,3,2,1
```

## Como Executar 
### 1. **Clone o repositório**:
```bash
git clone https://github.com/jjaoguedes/IA-2025-1.git
cd trabalho-3\questao-1
```

### 2. **Se atente a estrutura:**

**Estrutura do Repositório**

- `ltn/core.py`: este módulo contém a implementação do framework LTN. Em particular, contém a definição de constantes, variáveis, predicados, funções, conectivos e quantificadores.
- `ltn/fuzzy_ops.py`: este módulo contém a implementação de semântica de lógica fuzzy comum usando primitivas PyTorch.
- `tutorials/`: esta pasta contém alguns tutoriais importantes para começar a codificar em LTN.

OBS: Para mais informações, acesse o repositório oficial: [LTNtorch no GitHub](https://github.com/tommasocarraro/LTNtorch)

### 3. **Instale as dependências:**
```bash
pip3 install LTNtorch
```
OBS: Se atentar aos requirimentos presentes no arquivo **requirements.txt**

### 4. **Coloque o seu CSV de Sudoku na pasta sudoku_data/.**
### 5. **Execute o script:**
```bash
python3 sudoku_ltn.py
```

## Saídas Esperadas:

Para sudokus fechados válidos, o programa imprimirá algo como:
```bash
Satisfação: 1.0
Válido
```
Para sudokus fechados inválidos:

```bash
Satisfação: 0.93
Inválido
```
## Organização do Código

- **read_csv_board** – lê o arquivo .csv e transforma em matriz
- **board_to_tensor** – converte o tabuleiro para representação tensora
- **HasValueNet** – predicado para verificar valores nas células
- **ExactlyOne, OneHot, UniqueInRow, UniqueInColumn, UniqueInBlock** – fórmulas de restrição do Sudoku
- **aggregate** – mede o nível de satisfação das regras
