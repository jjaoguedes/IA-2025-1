Alunos:

**Aline da Conceição Ferreira Lima - 22250366**

**João Victor Félix Guedes - 22050227**

**Karen Letícia Santana da Silva - 22051416**


# Rede Neural CILP para Resolução de Regras Lógicas

Este projeto implementa uma rede neural simples baseada na abordagem **CILP (Connectionist Inductive Logic Programming)** para resolver regras lógicas, utilizando um conjunto de variáveis de entrada e de saída. O código processa um arquivo CSV com regras lógicas no formato `antecedentes => consequente`, ativa a rede neural e gera uma tabela de resultados.

## Funcionamento

A rede neural é construída a partir de regras lógicas fornecidas em um arquivo CSV. Essas regras são usadas para treinar uma rede que, a partir de um conjunto de variáveis de entrada, gera saídas binárias (`-1` ou `1`). O código utiliza uma rede neural simples com camadas de entrada, oculta e de saída.

### Passos principais:

1. **Leitura das Regras**:
    - As regras são fornecidas em um arquivo CSV e seguem o formato `antecedente => consequente`. Cada linha contém uma regra lógica que define a relação entre as variáveis de entrada e a saída.
    - O formato das regras é o seguinte:
      ```
      B, C, ~D => A
      E, F => A
      => B
      ```
      Onde o antecedente (lado esquerdo) define as condições para que a variável no consequente (lado direito) seja ativada.

2. **Construção da Rede Neural**:
    - A rede neural é construída com base nas variáveis extraídas das regras lidas.
    - A camada de entrada possui as variáveis do antecedente (como `B`, `C`, `D`, `E`, `F`), a camada oculta realiza o processamento das regras, e a camada de saída gera os resultados (como `A` e `B`).

3. **Geração de Combinações de Entrada**:
    - Para testar a rede neural, todas as combinações possíveis de valores binários (`1` e `-1`) para as variáveis de entrada são geradas. Cada combinação é testada na rede para gerar a saída correspondente.

4. **Processamento e Geração de Resultados**:
    - Para cada combinação de entradas, a rede neural calcula a saída com base nas regras. O resultado final é uma tabela que contém todas as combinações de entrada e suas respectivas saídas.

5. **Saída em CSV**:
    - Os resultados são salvos em um arquivo CSV (`resultados_rede.csv`) com as variáveis de entrada e saída.

## Arquivo CSV de Regras

O arquivo `regras.csv` deve conter uma coluna chamada **Regras**, onde cada linha segue o formato das regras lógicas. O conteúdo do arquivo pode ser algo assim:

Regras
"B, C, ~D => A"
"E, F => A"
"=> B"


### Exemplo de Regras:
1. **`B, C, ~D => A`**: Se `B = 1`, `C = 1` e `D = -1` (com negação), então `A = 1`.
2. **`E, F => A`**: Se `E = 1` e `F = 1`, então `A = 1`.
3. **`=> B`**: Não há antecedente, ou seja, `B` será sempre ativado.

## Código Explicado

### Leitura do CSV

A função `parse_regra` lê as regras do arquivo CSV, processando cada uma delas para extrair os antecedentes e os consequentes. As variáveis do antecedente podem incluir negações (como `~D`).

### Construção da Rede Neural

A função `construir_rede` cria a rede neural com base nas variáveis e regras lidas. Ela configura os pesos e bias para cada camada da rede com base nas regras lógicas fornecidas.

### Testes e Resultados

A função `gerar_tabela_testes` gera todas as combinações possíveis de valores para as variáveis de entrada, e a função `testar_rede` testa cada combinação na rede, gerando a saída correspondente.

### Saída

Os resultados (com todas as combinações de entrada e saídas) são salvos no arquivo `resultados_rede.csv` e podem ser visualizados posteriormente.
