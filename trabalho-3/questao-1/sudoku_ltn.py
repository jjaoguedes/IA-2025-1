import torch
import ltn
import csv
import sys

# ----------- CONECTIVOS COMPATÍVEIS COM SCALARS -----------

def to_2d(t):
    """Garante que o tensor tenha pelo menos 2 dimensões: [1, 1]"""
    if t.dim() == 0:
        return t.unsqueeze(0).unsqueeze(1)
    elif t.dim() == 1:
        return t.unsqueeze(1)
    return t

def And(*args):
    """Agregador AND para múltiplos LTNObjects."""
    tensors = [to_2d(arg.value) for arg in args]
    return ltn.LTNObject(torch.min(torch.cat(tensors, dim=1), dim=1, keepdim=True).values, [])

def Or(*args):
    """Agregador OR para múltiplos LTNObjects."""
    tensors = [to_2d(arg.value) for arg in args]
    return ltn.LTNObject(torch.max(torch.cat(tensors, dim=1), dim=1, keepdim=True).values, [])

def Not(x):
    """Operador NOT para um LTNObject."""
    return ltn.LTNObject(1. - to_2d(x.value), [])

# ----------- UTILITÁRIOS -----------
def const(v):
    """Cria um ltn.Constant a partir de um valor."""
    return ltn.Constant(torch.tensor(v, dtype=torch.float))

def read_csv_board(path):
    """Lê um tabuleiro de um arquivo CSV."""
    try:
        with open(path) as f:
            return [[int(cell) for cell in row] for row in csv.reader(f)]
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit(1)

def board_to_tensor(board, N):
    """Converte uma lista de listas (tabuleiro) para um tensor one-hot."""
    tensor = torch.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            # Ignora células vazias (valor 0 no CSV)
            if board[i][j] != 0:
                k = board[i][j] - 1
                tensor[i, j, k] = 1.0
    return tensor

# ----------- PREDICADO has_value -----------
class HasValueNet(torch.nn.Module):
    """Rede neural que atua como o predicado has_value(i, j, k)."""
    def __init__(self, board_tensor):
        super().__init__()
        # O tabuleiro é armazenado como um parâmetro não treinável.
        self.register_buffer('board', board_tensor)
        
    def forward(self, *x):
        # Converte os tensores de entrada para índices.
        x_stacked = torch.stack(x, dim=1)
        idxs = x_stacked.long()
        # Retorna o valor de verdade do tabuleiro para os índices [i, j, k]
        return self.board[idxs[:, 0], idxs[:, 1], idxs[:, 2]].unsqueeze(1)

# ----------- EXACTLY ONE (custom) -----------
def ExactlyOne(predicates):
    """Restrição lógica que garante que exatamente um dos predicados é verdadeiro."""
    # Pelo menos um deve ser verdadeiro: Or(p1, p2, ..., pn)
    at_least_one = Or(*predicates)
    
    # No máximo um pode ser verdadeiro: para todo par (pi, pj) com i!=j, Not(And(pi, pj))
    at_most_one = []
    for i in range(len(predicates)):
        for j in range(i + 1, len(predicates)):
            at_most_one.append(Not(And(predicates[i], predicates[j])))
    
    return And(at_least_one, *at_most_one)

# ----------- FUNÇÃO PRINCIPAL DE VALIDAÇÃO -----------
def main(file_path, N):
    """
    Função principal que carrega o tabuleiro, define os axiomas do Sudoku
    e calcula o nível de satisfação das regras.
    """
    print(f"Validando o tabuleiro {file_path} de tamanho {N}x{N}...")
    
    # Validação do tamanho do tabuleiro
    block_size_float = N ** 0.5
    if block_size_float != int(block_size_float):
        print(f"Erro: O tamanho {N} não é um quadrado perfeito (necessário para os blocos). Use 4 ou 9.")
        sys.exit(1)
    block_size = int(block_size_float)

    # Carrega os dados e cria o predicado
    board = read_csv_board(file_path)
    
    # Verifica se as dimensões do tabuleiro no arquivo correspondem ao tamanho N
    if len(board) != N or any(len(row) != N for row in board):
        print(f"Erro: As dimensões do tabuleiro no arquivo ({len(board)}x{len(board[0])}) não correspondem ao tamanho especificado ({N}x{N}).")
        sys.exit(1)
        
    board_tensor = board_to_tensor(board, N)
    has_value = ltn.Predicate(HasValueNet(board_tensor))

    # ---- AXIOMAS (definidos aqui para ter acesso a 'N' e 'has_value') ----
    def OneHot(i, j):
        """Cada célula (i,j) tem exatamente um valor k."""
        return ExactlyOne([has_value(i, j, const(k)) for k in range(N)])

    def UniqueInRow(i, k):
        """Cada linha i tem exatamente um valor k."""
        return ExactlyOne([has_value(i, const(j), k) for j in range(N)])

    def UniqueInColumn(j, k):
        """Cada coluna j tem exatamente um valor k."""
        return ExactlyOne([has_value(const(i), j, k) for i in range(N)])

    def UniqueInBlock(k):
        """Cada bloco tem exatamente um valor k."""
        constraints = []
        for bi in range(0, N, block_size):
            for bj in range(0, N, block_size):
                cells = [(i, j) for i in range(bi, bi + block_size)
                                  for j in range(bj, bj + block_size)]
                constraints.append(
                    ExactlyOne([has_value(const(i), const(j), k) for (i, j) in cells])
                )
        return And(*constraints)

    # Coleta todas as restrições lógicas (axiomas) em uma lista
    formulas = []
    for i in range(N):
        for j in range(N):
            formulas.append(OneHot(const(i), const(j)))
    for k in range(N):
        for i in range(N):
            formulas.append(UniqueInRow(const(i), const(k)))
        for j in range(N):
            formulas.append(UniqueInColumn(const(j), const(k)))
        formulas.append(UniqueInBlock(const(k)))

    # Agrega a satisfação de todas as fórmulas
    # A média é uma forma padrão de agregação de satisfiabilidade fuzzy.
    def aggregate(formulas):
        values = [to_2d(f.value) for f in formulas]
        return torch.mean(torch.cat(values, dim=0))

    sat_level = aggregate(formulas)
    
    # Exibe o resultado
    print(f"Nível de Satisfação: {sat_level.item():.4f}")
    if sat_level.item() > 0.99:
        print("Resultado: Válido")
    else:
        print("Resultado: Inválido")

# ----------- PONTO DE ENTRADA DO SCRIPT -----------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python sudoku_ltn.py <caminho_csv> <tamanho_tabuleiro>")
        print("Exemplo: python sudoku_ltn.py sudoku_data/sudoku9x9.csv 9")
        sys.exit(1)

    path = sys.argv[1]
    try:
        N = int(sys.argv[2])
        if N not in [4, 9]:
            raise ValueError()
    except:
        print("Erro: o tamanho do tabuleiro deve ser 4 ou 9.")
        sys.exit(1)

    # Chama a função principal com os argumentos fornecidos
    main(path, N)
