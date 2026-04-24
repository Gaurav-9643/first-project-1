import pygame
import pygame_gui
import random

pygame.init()

WIDTH, HEIGHT = 900, 750
CELL = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake & Ladder ULTRA PRO")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# COLORS
BG = (25,25,25)
WHITE = (220,220,220)
GREEN = (80,255,80)
RED = (255,80,80)
BLUE = (80,80,255)
GOLD = (255,215,0)
YELLOW = (255,255,0)

# GAME DATA
LADDERS = {2:38, 7:14, 8:31, 28:84, 51:67}
SNAKES = {16:6, 49:11, 62:19, 87:24}

BONUS = [5, 22, 44]
TRAPS = [13, 37, 66]
QUESTIONS = [10, 30, 55, 77]

player_pos = [1,1]
turn = 0
dice = 1
winner = None
rolling = False

# UI
roll_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((720, 200), (150, 50)),
    text='Roll Dice',
    manager=manager
)

restart_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((720, 270), (150, 50)),
    text='Restart',
    manager=manager
)

# ---------------- FUNCTIONS ----------------
def get_pos(n):
    n -= 1
    row = n // 10
    col = n % 10
    if row % 2:
        col = 9 - col
    x = col * CELL + CELL//2
    y = HEIGHT - 100 - (row * CELL + CELL//2)
    return x,y

def draw_board():
    for i in range(100):
        row = i // 10
        col = i % 10
        x = col * CELL
        y = HEIGHT - 100 - (row+1)*CELL

        color = (40,40,40) if (row+col)%2==0 else (60,60,60)
        pygame.draw.rect(screen, color, (x,y,CELL,CELL))
        pygame.draw.rect(screen, WHITE, (x,y,CELL,CELL),1)

        font = pygame.font.SysFont("Arial", 14)
        txt = font.render(str(i+1), True, WHITE)
        screen.blit(txt,(x+5,y+5))

    # ladders & snakes
    for s,e in LADDERS.items():
        pygame.draw.line(screen, GREEN, get_pos(s), get_pos(e), 4)

    for s,e in SNAKES.items():
        pygame.draw.line(screen, RED, get_pos(s), get_pos(e), 4)

    # SPECIAL TILES
    for b in BONUS:
        pygame.draw.circle(screen, GREEN, get_pos(b), 8)

    for t in TRAPS:
        pygame.draw.circle(screen, RED, get_pos(t), 8)

    for q in QUESTIONS:
        pygame.draw.circle(screen, YELLOW, get_pos(q), 8)

def apply_special(p):
    pos = player_pos[p]

    # BONUS
    if pos in BONUS:
        player_pos[p] += 10

    # TRAP
    if pos in TRAPS:
        player_pos[p] -= 10

    # QUESTION TILE (RANDOM EVENT)
    if pos in QUESTIONS:
        if random.choice([True, False]):
            player_pos[p] += 15
        else:
            player_pos[p] -= 15

    # LIMITS
    if player_pos[p] < 1:
        player_pos[p] = 1

def move(p, steps):
    global winner

    player_pos[p] += steps

    if player_pos[p] in LADDERS:
        player_pos[p] = LADDERS[player_pos[p]]

    elif player_pos[p] in SNAKES:
        player_pos[p] = SNAKES[player_pos[p]]

    apply_special(p)

    if player_pos[p] >= 100:
        winner = p+1

def ai_move():
    global turn, dice, rolling
    if not rolling:
        rolling = True
        pygame.time.delay(500)
        dice = random.randint(1,6)
        move(1, dice)
        if dice != 6:
            turn = 0
        rolling = False

# ---------------- MAIN LOOP ----------------
running = True

while running:
    time_delta = clock.tick(60)/1000.0
    screen.fill(BG)

    draw_board()

    # PLAYERS
    for i,color in enumerate([BLUE, RED]):
        x,y = get_pos(player_pos[i])
        pygame.draw.circle(screen, color, (x,y), 12)

    # TURN HIGHLIGHT
    hx,hy = get_pos(player_pos[turn])
    pygame.draw.circle(screen, GOLD, (hx,hy), 20, 2)

    # UI TEXT
    font = pygame.font.SysFont("Arial", 20)
    info = [
        f"Turn: Player {turn+1}",
        f"Dice: {dice}",
        f"P1: {player_pos[0]}",
        f"P2: {player_pos[1]}"
    ]

    for i,text in enumerate(info):
        txt = font.render(text, True, WHITE)
        screen.blit(txt,(720,50 + i*30))

    if winner:
        big = pygame.font.SysFont("Arial", 40)
        win = big.render(f"PLAYER {winner} WINS!", True, GOLD)
        screen.blit(win,(200,300))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == roll_btn and not winner:
                if turn == 0 and not rolling:
                    rolling = True
                    dice = random.randint(1,6)
                    move(0,dice)

                    if dice != 6:
                        turn = 1

                    rolling = False

            if event.ui_element == restart_btn:
                player_pos = [1,1]
                turn = 0
                winner = None

    # AI TURN (ONE BY ONE)
    if turn == 1 and not winner and not rolling:
        ai_move()

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()