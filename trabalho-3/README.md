# Classificador de Sudoku com LTNTorch

Este projeto propõe uma solução lógica e simbólica para o problema do Sudoku utilizando **LTNTorch** (Logic Tensor Networks). A implementação aborda desde a verificação de um tabuleiro fechado até a recomendação de heurísticas para tabuleiros abertos, utilizando axiomas formulados com base em restrições do jogo e exemplos do repositório oficial do LTNTorch.

**Componentes do grupo:** 

- Aline da Conceição Ferreira Lima - 22250366
- Allan Carvalho de Aguiar - 22153696
- Karen Letícia Santana da Silva - 22051416
- João Victor Felix Guedes - 22050227 

## Descrição Geral

Este projeto foi desenvolvido com base na seguinte proposta:

> **"Considere o problema do Sudoku e projete e implemente uma solução em LTNTorch que aprenda os conceitos das questões 1 a 3. Tome como base as especificações lógicas do Sudoku, o artigo1 e os exemplos do repositório LTNTorch para escrever os axiomas."**



## Questões Atendidas

### Questão 1 – Classificar um tabuleiro fechado

Dado um tabuleiro completamente preenchido (fechado), o sistema determina se o preenchimento está correto de acordo com as regras do Sudoku. A saída é:

- `1` para **válido**
- `0` para **inválido**

> O tabuleiro é lido de um arquivo `.csv`.



### Questão 2 – Classificar um tabuleiro inicial/aberto

Para tabuleiros parcialmente preenchidos (abertos), o sistema utiliza **heurísticas lógicas** para estimar a validade do tabuleiro. Os axiomas utilizados nas restrições são adaptados para considerar as posições vazias como **desconhecidas**, e inferências são feitas sobre possíveis preenchimentos.


### Questão 3 – Indicar heurísticas recomendadas

Dado um tabuleiro aberto, o sistema analisa quais **heurísticas lógicas** são mais úteis na tentativa de completar o Sudoku. Isso é feito com base na **satisfatibilidade** das fórmulas LTN para diferentes heurísticas aplicadas ao tabuleiro incompleto.


## Estrutura Lógica do Sudoku

### Restrições principais levadas em consideração

- Cada **linha** deve conter todos os números de 1 a N exatamente uma vez
- Cada **coluna** deve conter todos os números de 1 a N exatamente uma vez
- Cada **bloco** (subgrid) deve conter todos os números de 1 a N exatamente uma vez
- Cada **célula** deve conter exatamente um número


## Representação e Domínios

- Representação binária em tensor 3D: `board_tensor[N][N][N]`
  - `1.0` se a célula (i, j) contém o número `k + 1`
  - `0.0` caso contrário
- Domínios:
  - `i`: índice da linha (0 até N−1)
  - `j`: índice da coluna (0 até N−1)
  - `k`: índice do valor (0 até N−1)


## Predicados

| Predicado            | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `has_value(i, j, k)` | Verdadeiro se a célula (i, j) contiver o valor `k + 1`                    |
| `are_equal(v1, v2)`  | Retorna verdadeiro se `v1 == v2`, útil para lógica de igualdade em blocos |


## Axiomas Utilizados

| Axioma                                | Descrição                                                                 |
|--------------------------------------|---------------------------------------------------------------------------|
| **Célula única**                     | Cada célula (i, j) contém exatamente um valor `k`                         |
| **Valor único por linha**           | Cada valor `k` aparece apenas uma vez por linha                          |
| **Valor único por coluna**          | Cada valor `k` aparece apenas uma vez por coluna                         |
| **Valor único por bloco (subgrid)** | Cada valor `k` aparece apenas uma vez por bloco de tamanho `√N x √N`     |

> Os axiomas são implementados como fórmulas lógicas fuzzy utilizando conectivos personalizados (`And`, `Or`, `Not`) e o operador `ExactlyOne()` para garantir exclusividade lógica entre combinações de valores.


## Estrutura dos Dados

**Exemplo de Tabuleiro 4x4 (formato CSV - Válido):**
```
1,2,3,4 
3,4,1,2
2,1,4,3
4,3,2,1
```

**Exemplo de Tabuleiro 9x9 (formato CSV - Válido):**
```
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```


## Requisitos

- Python 3
- PyTorch
- LTNTorch

## Organização / Estrutura do Projeto
- **ltn:** biblioteca utilizada;
- **questao-1:** solução questão 1;
- **questao-2:** solução questão 2;
- **questao-3:** solução questão 3;
- **requirements.txt:** bibliotecas para configuração;
- **config-ambiente.md:** configuração do ambiente para executar o código (caso não esteja configurado).

  OBS: Não esqueça de acessar o README específicos para cada questão.
  
## Referências
- Article: Designing Logic Tensor Networks for Visual Sudoku puzzle classification
- [LTNtorch no GitHub](https://github.com/tommasocarraro/LTNtorch)


