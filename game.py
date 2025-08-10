import pygame
import random
import time
import sys
import json
from datetime import datetime


pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Ninja")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
GRAY = (180, 180, 180)
YELLOW = (255, 255, 0)


font_large = pygame.font.SysFont("Arial", 60)
font_medium = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

# sounds
try:
    correct_sound = pygame.mixer.Sound("correct.wav")
    wrong_sound = pygame.mixer.Sound("wrong.wav")
except:
    correct_sound = pygame.mixer.Sound(buffer=bytearray([128] * 1000))
    wrong_sound = pygame.mixer.Sound(buffer=bytearray([128] * 1000))

# Words to choose from
EASY_WORDS = ["python", "loop", "list", "print", "true", "false", "open", "if", "else", "for", "def", "and", "or", "not", "min", "max", "file", "code", "math", "join", "name", "input", "zip", "break", "with"]
MEDIUM_WORDS = ["function", "return", "global", "import", "append", "remove", "index", "range", "lambda", "filter", "sorted", "format", "escape", "integer", "except", "binary", "syntax", "object", "method", "class", "string", "float", "assert", "debug", "module"]
HARD_WORDS = ["inheritance", "polymorphism", "encapsulation", "abstraction", "comprehension", "constructor", "destructor", "recursion", "asynchronous", "decorator", "generator", "algorithm", "enumerate", "serialization", "multithreading", "superclass", "namespace", "overloading", "interpreter", "expression", "comparator", "dictionary", "exception", "subclass", "operator"]

def get_word(level):
    if level == "easy":
        return random.choice(EASY_WORDS)
    elif level == "hard":
        return random.choice(HARD_WORDS)
    return random.choice(MEDIUM_WORDS)

def draw_text(text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y)) if align == "center" else text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, rect)
    return rect

def button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, hover_color if rect.collidepoint(mouse) else color, rect, border_radius=10)
    draw_text(text, font_medium, BLACK, x + w//2, y + h//2)
    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.wait(200)
        if action:
            return action
    return None

def save_score(wpm, accuracy):
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append({
        "wpm": round(wpm, 1),
        "accuracy": round(accuracy, 1),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open("scores.json", "w") as f:
        json.dump(data, f)

def get_highscore():
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
        return max([entry["wpm"] for entry in data])
    except:
        return 0

def show_results(correct, total, start, end):
    time_taken = end - start
    wpm = (correct / time_taken) * 60 if time_taken else 0
    accuracy = (correct / total) * 100 if total else 0
    save_score(wpm, accuracy)

    while True:
        screen.fill(BLACK)
        draw_text("RESULTS", font_large, BLUE, WIDTH//2, 100)
        draw_text(f"WPM: {wpm:.1f}", font_medium, YELLOW, WIDTH//2, 200)
        draw_text(f"Accuracy: {accuracy:.1f}%", font_medium, GREEN, WIDTH//2, 260)
        draw_text(f"High Score: {get_highscore():.1f} WPM", font_medium, WHITE, WIDTH//2, 320)

        restart = button("Restart", WIDTH//2 - 150, 400, 140, 60, GRAY, GREEN, True)
        quit_game = button("Quit", WIDTH//2 + 10, 400, 140, 60, GRAY, RED, False)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if restart is not None:
            return restart
        if quit_game is not None:
            return quit_game

        pygame.display.flip()
        clock.tick(60)

def main_game(level):
    correct, total = 0, 0
    user_input = ""
    word = get_word(level)
    start = time.time()

    while True:
        screen.fill(BLACK)
        draw_text(word, font_large, WHITE, WIDTH//2, HEIGHT//2 - 80)
        draw_text(user_input, font_large, GREEN, WIDTH//2, HEIGHT//2 + 20)
        draw_text(f"Correct: {correct}/{total}", font_small, WHITE, 30, 30, align="left")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    total += 1
                    if user_input == word:
                        correct += 1
                        correct_sound.play()
                    else:
                        wrong_sound.play()
                    word = get_word(level)
                    user_input = ""
                    if total == 10:
                        return show_results(correct, total, start, time.time())
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        pygame.display.flip()
        clock.tick(60)

def start_screen():
    difficulty = "medium"
    while True:
        screen.fill(BLACK)
        draw_text("PYTHON TYPING NINJA", font_large, BLUE, WIDTH//2, 100)
        draw_text(f"High Score: {get_highscore():.1f} WPM", font_medium, YELLOW, WIDTH//2, 180)
        draw_text("Select Difficulty", font_medium, WHITE, WIDTH//2, 250)

        if button("Easy", WIDTH//2 - 230, 300, 140, 60, GRAY, GREEN, "easy") == "easy":
            difficulty = "easy"
        if button("Medium", WIDTH//2 - 70, 300, 140, 60, GRAY, BLUE, "medium") == "medium":
            difficulty = "medium"
        if button("Hard", WIDTH//2 + 90, 300, 140, 60, GRAY, RED, "hard") == "hard":
            difficulty = "hard"

        if button("Start Game", WIDTH//2 - 100, 400, 200, 70, YELLOW, GREEN, True):
            return difficulty

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        difficulty = start_screen()
        if not main_game(difficulty):
            break

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
