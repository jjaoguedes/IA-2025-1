import torch
import ltn
import csv

# ----------- CONFIGURAÇÕES -----------
N = 9  # ou 9 para Sudoku 9x9

# ----------- CONECTIVOS COMPATÍVEIS COM SCALARS -----------

def to_2d(t):
    """Garante que o tensor tenha pelo menos 2 dimensões: [1, 1]"""
    if t.dim() == 0:
        return t.unsqueeze(0).unsqueeze(1)
    elif t.dim() == 1:
        return t.unsqueeze(1)
    return t

def And(*args):
    tensors = [to_2d(arg.value) for arg in args]
    return ltn.LTNObject(torch.min(torch.cat(tensors, dim=1), dim=1, keepdim=True).values, [])

def Or(*args):
    tensors = [to_2d(arg.value) for arg in args]
    return ltn.LTNObject(torch.max(torch.cat(tensors, dim=1), dim=1, keepdim=True).values, [])

def Not(x):
    return ltn.LTNObject(1. - to_2d(x.value), [])

# ----------- UTILITÁRIOS -----------
def const(v):
    return ltn.Constant(torch.tensor(v, dtype=torch.float))

def read_csv_board(path):
    with open(path) as f:
        return [[int(cell) for cell in row] for row in csv.reader(f)]

def board_to_tensor(board, N):
    tensor = torch.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            k = board[i][j] - 1
            tensor[i, j, k] = 1.0
    return tensor

# ----------- PREDICADO has_value -----------
class HasValueNet(torch.nn.Module):
    def __init__(self, board_tensor):
        super().__init__()
        self.board = board_tensor
    def forward(self, *x):
        x = torch.stack(x, dim=1)
        idxs = x.long()
        return self.board[idxs[:, 0], idxs[:, 1], idxs[:, 2]].unsqueeze(1)

# ----------- EXACTLY ONE (custom) -----------
def ExactlyOne(predicates):
    constraints = []
    constraints.append(Or(*predicates))
    for i in range(len(predicates)):
        for j in range(i+1, len(predicates)):
            constraints.append(Not(And(predicates[i], predicates[j])))
    return And(*constraints)

# ----------- AXIOMAS -----------
def OneHot(i, j):
    return ExactlyOne([has_value(i, j, const(k)) for k in range(N)])

def UniqueInRow(i, k):
    return ExactlyOne([has_value(i, const(j), k) for j in range(N)])

def UniqueInColumn(j, k):
    return ExactlyOne([has_value(const(i), j, k) for i in range(N)])

def UniqueInBlock(k):
    block_size = int(N ** 0.5)
    constraints = []
    for bi in range(0, N, block_size):
        for bj in range(0, N, block_size):
            cells = [(i, j) for i in range(bi, bi + block_size)
                              for j in range(bj, bj + block_size)]
            constraints.append(
                ExactlyOne([has_value(const(i), const(j), k) for (i, j) in cells])
            )
    return And(*constraints)

# ----------- CARREGAMENTO E EXECUÇÃO -----------
if __name__ == "__main__":
    board = read_csv_board("sudoku_data/sudoku9x9_valid1.csv")  # Exemplo de tabuleiro
    board_tensor = board_to_tensor(board, N)
    has_value = ltn.Predicate(HasValueNet(board_tensor))

    formulas = []
    for i in range(N):
        for j in range(N):
            formulas.append(OneHot(const(i), const(j)))
    for i in range(N):
        for k in range(N):
            formulas.append(UniqueInRow(const(i), const(k)))
    for j in range(N):
        for k in range(N):
            formulas.append(UniqueInColumn(const(j), const(k)))
    for k in range(N):
        formulas.append(UniqueInBlock(const(k)))

# calcula a média de satisfação de todas as fórmulas LTN. A média é uma forma padrão de agregação de satisfiabilidade fuzzy.
def aggregate(formulas):
    values = [to_2d(f.value) for f in formulas]
    return torch.mean(torch.cat(values, dim=0))

sat_level = aggregate(formulas)

print("Satisfação:", sat_level.item())
print("Válido" if sat_level.item() > 0.99 else "Inválido")
