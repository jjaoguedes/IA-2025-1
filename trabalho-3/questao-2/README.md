# Solução utilizando heurísticas - Questão 2

## Classificador de Sudoku com Logic Tensor Networks (LTN)

Este projeto implementa um classificador de Sudoku baseado em lógica heurística, com suporte à análise de risco e movimentos futuros. A estrutura usa conceitos de **Logic Tensor Networks** para representar inferências de forma interpretável e simbólica.

---

## Estrutura de Diretórios

```
.
├── sudoku_ltn.py
├── sudoku_data/
│   └── sudoku9x9.csv
└── Makefile
```

---

## Requisitos

- Python 3.x
- Bibliotecas:
  - `torch`
  - `ltn` (opcional, atualmente não usada diretamente)
  - `csv`, `math`, `itertools`, `sys` (nativas)

---

## Como Executar

### Via linha de comando

```bash
python sudoku_ltn.py <caminho_csv> <tamanho_tabuleiro>
```

**Exemplo:**
```bash
python sudoku_ltn.py sudoku_data/sudoku9x9.csv 9
```

---

## Funcionalidades

1. **Classificação do Tabuleiro**:
   - Determina se o tabuleiro tem uma solução viável com base na validade de preenchimento.

2. **Análise de Risco**:
   - Identifica os dígitos com menos posições possíveis (mais arriscados).

3. **Análise de Movimentos Futuros**:
   - Profundidade 1: Verifica se algum movimento causa beco sem saída imediato.
   - Profundidade 2: Explora combinações de dois movimentos e detecta possíveis becos sem saída.

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



