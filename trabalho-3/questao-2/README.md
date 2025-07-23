# Solução utilizando heurísticas - Questão 2

## Classificador de Sudoku Aberto

Este projeto implementa um classificador de Sudoku que analisa se um tabuleiro possui solução e verifica a segurança de possíveis jogadas com 1 ou 2 passos futuros, utilizando uma abordagem de simulação e verificação de restrições.

---

## Estrutura de Diretórios

```
.
├── classificador_sudoku_aberto.py
├── sudoku_data/
│   └── sudoku9x9.csv
└── Makefile
```

---

## Requisitos

- Python 3.x
- Biblioteca padrão (`csv`, `sys`)

---

## Como Executar

### Opção 1: Executar com o `Makefile`

#### Comando padrão:

```bash
make run
```

> Usa o arquivo `sudoku_data/sudoku9x9.csv` com tabuleiro 9x9.

#### Comando personalizado:

```bash
make custom CSV_PATH=caminho/para/seuarquivo.csv BOARD_SIZE=4
```

> Substitua o caminho e o tamanho do tabuleiro conforme necessário (`4` ou `9`).

#### Verificar erros de sintaxe:

```bash
make check
```

#### Limpar arquivos temporários:

```bash
make clean
```

---

### Opção 2: Executar diretamente via terminal

```bash
python classificador_sudoku_aberto.py <caminho_csv> <tamanho_tabuleiro>
```

**Exemplo:**
```bash
python classificador_sudoku_aberto.py sudoku_data/sudoku9x9.csv 9
```

---

## O que o script faz?

1. **Verifica se o tabuleiro possui solução:**
   - Detecta se alguma célula está bloqueada (sem valores válidos).

2. **Classifica possíveis jogadas seguras ou inseguras:**
   - Considera o impacto de jogar determinado número em uma célula vazia.
   - Analisa segurança com:
     - **1 jogada futura** (imediato)
     - **2 jogadas futuras** (cenário mais profundo)

---

## Exemplo de Makefile

```makefile
# Nome do script
SCRIPT = classificador_sudoku_aberto.py

# Caminho padrão do CSV e tamanho do tabuleiro
CSV_PATH = sudoku_data/sudoku9x9.csv
BOARD_SIZE = 9

# Alvo padrão - executa com os parâmetros padrão
run:
	python $(SCRIPT) $(CSV_PATH) $(BOARD_SIZE)

# Alvo para execução personalizada
custom:
	@echo "Executando com: $(CSV_PATH) e tabuleiro de tamanho $(BOARD_SIZE)"
	python $(SCRIPT) $(CSV_PATH) $(BOARD_SIZE)

# Verifica erros de sintaxe
check:
	python -m py_compile $(SCRIPT)

# Limpa arquivos de cache
clean:
	rm -rf __pycache__ *.pyc
```

---

## Exemplo de entrada (`sudoku9x9.csv`)

```csv
5,3,0,0,7,0,0,0,0
6,0,0,1,9,5,0,0,0
0,9,8,0,0,0,0,6,0
8,0,0,0,6,0,0,0,3
4,0,0,8,0,3,0,0,1
7,0,0,0,2,0,0,0,6
0,6,0,0,0,0,2,8,0
0,0,0,4,1,9,0,0,5
0,0,0,0,8,0,0,7,9
```

---

