import random
import numpy as np
import pygame
import sys

from agent_Nstep import agent_Nstep

# ゲームの設定
class Config:
    def __init__(self):
        self.rows = 6  # ボードの行数
        self.columns = 7  # ボードの列数
        self.inarow = 4  # 勝利条件（4つの連続した駒）
class Observation:
    def __init__(self,board):
        self.board = board



# ボードの初期化
def init_board():
    return np.zeros((6, 7), dtype=int)  # 6行7列のボードをゼロで初期化

# 駒をボードに落とす関数
def drop_piece(board, col, piece, config):
    for row in range(config.rows - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            break

# ゲーム終了かどうかを判定
def is_game_over(board, config):
    for row in range(config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(board[row, col:col+config.inarow])
            if window.count(1) == config.inarow or window.count(2) == config.inarow:
                return True
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns):
            window = list(board[row:row+config.inarow, col])
            if window.count(1) == config.inarow or window.count(2) == config.inarow:
                return True
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(board[range(row, row + config.inarow), range(col, col + config.inarow)])
            if window.count(1) == config.inarow or window.count(2) == config.inarow:
                return True
    for row in range(config.inarow - 1, config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(board[range(row, row - config.inarow, -1), range(col, col + config.inarow)])
            if window.count(1) == config.inarow or window.count(2) == config.inarow:
                return True
    if np.all(board != 0):
        return True
    return False

# 画面にボードを描画する関数
def draw_board(board, screen, config):
    for c in range(config.columns):
        for r in range(config.rows):
            pygame.draw.rect(screen, (0, 0, 255), (c*100, r*100 + 100, 100, 100))  # ボードの枠
            pygame.draw.circle(screen, (0, 0, 0), (c*100 + 50, r*100 + 150), 40)  # 駒の背景色
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (c*100 + 50, r*100 + 150), 40)  # プレイヤー1の駒（赤）
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (c*100 + 50, r*100 + 150), 40)  # プレイヤー2の駒（黄色）

# エージェント（プレイヤー2）のAIロジック（簡易版）
def agent(board, config):
    List = []
    for i in range(config.columns*config.rows):
        
        List.append(board[i//config.columns][i%config.columns])


    return agent_Nstep(List, config)
    
    

# プレイヤーとエージェントのターンを交互に実行
def play_game():
    pygame.init()
    config = Config()  # Configインスタンスを作成
    screen = pygame.display.set_mode((config.columns * 100, (config.rows + 1) * 100))
    pygame.display.set_caption("Connect Four")
    font = pygame.font.SysFont("Arial", 50)  # フォントの設定
    board = init_board()
    current_player = 1
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # プレイヤー1（赤）はマウスクリックで駒を落とす
            if event.type == pygame.MOUSEMOTION:
                mouseX = event.pos[0]
                pygame.draw.rect(screen, (0, 255, 0), (0, 0, config.columns * 100, 100))
                pygame.draw.circle(screen, (255, 0, 0), (mouseX, 50), 40)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                col = mouseX // 100
                if board[0][col] == 0:
                    drop_piece(board, col, current_player, config)

                    # ゲーム終了判定
                    if is_game_over(board, config):
                        game_over = True
                        winner_text = font.render(f"Player {current_player} Wins!", True, (255, 255, 255))
                        screen.blit(winner_text, (config.columns * 50 - winner_text.get_width() // 2, config.rows * 100 + 50))

                    # プレイヤー交代
                    current_player = 3 - current_player  # プレイヤー1とプレイヤー2が交互に

        # プレイヤー2（エージェント）のターン
        if current_player == 2 and not game_over:
            col = agent(board, config)
            drop_piece(board, col, current_player, config)

            # ゲーム終了判定
            if is_game_over(board, config):
                game_over = True
                winner_text = font.render(f"Player {current_player} Wins!", True, (255, 255, 255))
                screen.blit(winner_text, (config.columns * 50 - winner_text.get_width() // 2, config.rows * 100 + 50))

            # プレイヤー交代
            current_player = 3 - current_player  # プレイヤー1とプレイヤー2が交互に

        draw_board(board, screen, config)
        pygame.display.update()

        if game_over:
            pygame.time.wait(2000)  # 2秒間表示して、再スタートの確認

            # 再プレイするかどうかを聞く
            restart_game(screen, font)

# ゲーム再開を確認する関数
def restart_game(screen, font):
    restart_text = font.render("Press Y to Restart or N to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Yキーで再プレイ
                    play_game()  # 再プレイ
                    waiting = False
                elif event.key == pygame.K_n:  # Nキーで終了
                    pygame.quit()
                    sys.exit()

# ゲーム開始
play_game()
