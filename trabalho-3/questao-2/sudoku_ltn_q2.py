import torch
import ltn
import csv
import math
import itertools
from collections import defaultdict
import sys # Para sair do script de forma limpa

class SudokuClassifier:
    """
    Classe para classificar um tabuleiro de Sudoku usando uma abordagem
    lógica/heurística baseada na representação de Logic Tensor Networks.
    """
    def __init__(self, N):
        if not math.sqrt(N).is_integer():
            raise ValueError(f"O tamanho N ({N}) deve ser um quadrado perfeito (ex: 4, 9, 16).")
        self.N = N
        self.box_size = int(math.sqrt(N))
        print(f"Inicializando classificador de Sudoku {N}x{N}...")

    def _load_board_from_csv(self, filepath):
        board = []
        try:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Ignora linhas vazias no CSV
                    if not row: continue
                    board.append([int(val) for val in row])
        except FileNotFoundError:
            print(f"ERRO: Arquivo '{filepath}' não encontrado.", file=sys.stderr)
            return None
        except ValueError:
            print(f"ERRO: O arquivo '{filepath}' contém valores que não são números inteiros.", file=sys.stderr)
            return None
        
        if not board or len(board) != self.N or any(len(row) != self.N for row in board):
            print(f"ERRO: O tabuleiro em '{filepath}' não tem as dimensões corretas de {self.N}x{self.N}.", file=sys.stderr)
            return None
            
        return board

    def _is_placement_valid(self, board, digit, r, c):
        # Verifica linha
        if digit in board[r]: return False
        # Verifica coluna
        if digit in [board[i][c] for i in range(self.N)]: return False
        # Verifica bloco
        box_r_start, box_c_start = (r // self.box_size) * self.box_size, (c // self.box_size) * self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if board[box_r_start + i][box_c_start + j] == digit: return False
        return True

    def find_possible_placements(self, board):
        empty_cells = [(r, c) for r in range(self.N) for c in range(self.N) if board[r][c] == 0]
        placements = defaultdict(list)
        for digit in range(1, self.N + 1):
            for r, c in empty_cells:
                if self._is_placement_valid(board, digit, r, c):
                    placements[digit].append((r, c))
        return placements

    def classify_board(self, board):
        possible_placements = self.find_possible_placements(board)
        for digit in range(1, self.N + 1):
            if not possible_placements[digit]:
                 count_on_board = sum(row.count(digit) for row in board)
                 if count_on_board < self.N:
                    return "Sem solução", f"O dígito {digit} não pode ser colocado em nenhuma célula vazia restante.", possible_placements
        return "Solução possível", "Todo dígito possui ao menos uma posição válida para ser jogado.", possible_placements

    def analyze_risk(self, possible_placements):
        risk_analysis = sorted(possible_placements.items(), key=lambda item: len(item[1]))
        print("\n--- Análise de Risco (Dígitos mais restritos primeiro) ---")
        for digit, placements in risk_analysis:
            count = len(placements)
            if count > 0:
                print(f"Dígito {digit}: {count} posições possíveis. {'(Mais arriscado)' if count <= (self.N // 2) else ''}")
            else:
                 print(f"Dígito {digit}: 0 posições possíveis.")

    def analyze_future_moves(self, board, possible_placements, depth=2):
        print(f"\n--- Análise de Movimentos Futuros (Profundidade: {depth}) ---")
        empty_cells = [(r, c) for r in range(self.N) for c in range(self.N) if board[r][c] == 0]
        if not empty_cells:
            print("O tabuleiro já está completo. Nenhuma análise de movimento futuro.")
            return

        # Profundidade 1
        print("\n[Profundidade 1]")
        moves_leading_to_dead_end_1 = []
        all_possible_first_moves = [{'digit': d, 'r': r, 'c': c} for d, places in possible_placements.items() for r, c in places]
        for move in all_possible_first_moves:
            temp_board = [row[:] for row in board]
            temp_board[move['r']][move['c']] = move['digit']
            classification, _, _ = self.classify_board(temp_board)
            if classification == "Sem solução":
                moves_leading_to_dead_end_1.append(move)
        
        if moves_leading_to_dead_end_1:
            print(f"AVISO: {len(moves_leading_to_dead_end_1)} movimentos de 1 passo levam a um beco sem saída imediato.")
            for move in moves_leading_to_dead_end_1[:5]:
                print(f"  - Jogar {move['digit']} em ({move['r']},{move['c']}) bloqueia outro dígito.")
        else:
            print("BOA NOTÍCIA: Nenhum movimento de 1 passo leva a um beco sem saída imediato.")
        
        if depth < 2: return

        # Profundidade 2
        print("\n[Profundidade 2]")
        risk_analysis = sorted(possible_placements.items(), key=lambda item: len(item[1]))
        moves_leading_to_dead_end_2 = []
        total_searched = 0
        search_limit = 4000 # Limite para evitar busca excessiva em tabuleiros 9x9
        
        for digit1, placements1 in risk_analysis:
            if total_searched > search_limit: break
            if not placements1: continue
            for r1, c1 in placements1:
                if total_searched > search_limit: break
                board_after_1 = [row[:] for row in board]; board_after_1[r1][c1] = digit1
                placements_after_1 = self.find_possible_placements(board_after_1)
                risk_after_1 = sorted(placements_after_1.items(), key=lambda item: len(item[1]))
                for digit2, placements2 in risk_after_1:
                    if not placements2: continue
                    for r2, c2 in placements2:
                        total_searched += 1
                        if total_searched > search_limit: break
                        board_after_2 = [row[:] for row in board_after_1]; board_after_2[r2][c2] = digit2
                        classification, _, _ = self.classify_board(board_after_2)
                        if classification == "Sem solução":
                            move_seq = (f"Jogar {digit1} em ({r1},{c1})", f"seguido por {digit2} em ({r2},{c2})")
                            if move_seq not in moves_leading_to_dead_end_2:
                                moves_leading_to_dead_end_2.append(move_seq)
        
        if moves_leading_to_dead_end_2:
            print(f"AVISO: Encontradas {len(moves_leading_to_dead_end_2)} sequências de 2 passos (em uma busca de {total_searched} caminhos) que levam a um beco sem saída.")
            for seq in moves_leading_to_dead_end_2[:5]:
                print(f"  - Sequência: {seq[0]} -> {seq[1]}")
        else:
            print(f"BOA NOTÍCIA: Nenhuma sequência de 2 passos problemática encontrada na busca limitada ({total_searched} caminhos).")

    def run_analysis(self, filepath):
        print("="*60)
        print(f"Analisando tabuleiro de '{filepath}' para tamanho {self.N}x{self.N}")
        print("="*60)
        board = self._load_board_from_csv(filepath)
        if board is None: return # Erro já foi impresso no método de carga
        
        print("Tabuleiro Inicial:")
        for row in board:
            print(" ".join(map(str, row)).replace('0', '.')) # Troca 0 por . para melhor visualização

        classification, message, possible_placements = self.classify_board(board)
        print(f"\n--- Classificação do Tabuleiro ---\nStatus: {classification}\nMotivo: {message}")
        if classification == "Solução possível":
            self.analyze_risk(possible_placements)
            self.analyze_future_moves(board, possible_placements, depth=2)
        print("="*60 + "\n")

def main(filename, size):
    """
    Função principal que processa argumentos da linha de comando para analisar um tabuleiro.
    """
    

    try:
        classifier = SudokuClassifier(size)
        classifier.run_analysis(filename)
    except ValueError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)

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

    main(path, N)
