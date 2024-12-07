import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_SIZE = 100
CARD_MARGIN = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
GRAY = (149, 165, 166)
BLACK = (0, 0, 0)

# Game Settings
CARD_SYMBOLS = ['🍎', '🍐', '🍊', '🍋', '🍌', '🍇', '🍉', '🍒']
SYMBOLS = CARD_SYMBOLS * 2  # Duplicate symbols for matching

class MemoryCardGame:
    def __init__(self):
        # Screen Setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Memory Card Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Game State
        self.cards = self.create_cards()
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0

    def create_cards(self):
        # Shuffle symbols
        random.shuffle(SYMBOLS)
        
        # Create card grid
        cards = []
        for i, symbol in enumerate(SYMBOLS):
            row = i // 4
            col = i % 4
            x = col * (CARD_SIZE + CARD_MARGIN) + 200
            y = row * (CARD_SIZE + CARD_MARGIN) + 150
            cards.append({
                'rect': pygame.Rect(x, y, CARD_SIZE, CARD_SIZE),
                'symbol': symbol,
                'flipped': False,
                'matched': False
            })
        return cards

    def draw_cards(self):
        for card in self.cards:
            # Draw card background
            color = BLUE
            if card['matched']:
                color = GRAY
            elif card['flipped']:
                color = GREEN
            
            pygame.draw.rect(self.screen, color, card['rect'])
            
            # Draw symbol if card is flipped
            if card['flipped'] or card['matched']:
                text = pygame.font.Font(None, 64).render(card['symbol'], True, BLACK)
                text_rect = text.get_rect(center=card['rect'].center)
                self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        for card in self.cards:
            if card['rect'].collidepoint(pos) and not card['flipped'] and not card['matched']:
                # Flip card
                card['flipped'] = True
                self.flipped_cards.append(card)
                
                # Check for match when two cards are flipped
                if len(self.flipped_cards) == 2:
                    self.moves += 1
                    pygame.time.delay(500)  # Pause to show cards
                    self.check_match()

    def check_match(self):
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            
            if card1['symbol'] == card2['symbol']:
                # Match found
                card1['matched'] = True
                card2['matched'] = True
                self.matched_pairs += 1
            else:
                # No match, flip cards back
                card1['flipped'] = False
                card2['flipped'] = False
            
            # Clear flipped cards
            self.flipped_cards.clear()

    def draw_moves(self):
        moves_text = self.font.render(f'Moves: {self.moves}', True, BLACK)
        self.screen.blit(moves_text, (350, 50))

    def check_win(self):
        if self.matched_pairs == len(SYMBOLS) // 2:
            win_text = self.font.render(f'You Won in {self.moves} Moves!', True, BLACK)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(win_text, win_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            return True
        return False

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw_cards()
            self.draw_moves()
            
            if self.check_win():
                running = False
            
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = MemoryCardGame()
    game.run()
