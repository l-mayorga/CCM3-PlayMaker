import numpy as np
import pygame

SCREEN_WIDTH = 800
SCREEN_HIGHT = 700

# Define field dimensions
FIELD_WIDTH = 400
FIELD_HEIGHT = 700
SCORING_ZONE_HEIGHT = 75

# Define colors
GREEN = (44, 128, 44)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



TRANSITION_MATRIX = {
    "START": {
        "START": 0.0,
        "RESET_BREAK": 0.25,
        "RESEST_UPLINE": 0.15,
        "STACK_IN_CUT": 0.45,
        "STACK_BREAK_CUT": 0.05,
        "STACK_DEEP_CUT": 0.05,
        "HAIL_MARY": 0.05,
    },

    "RESET_BREAK": {
        "START": 0.0,
        "RESET_BREAK": 0.0,
        "RESEST_UPLINE": 0.0,
        "STACK_IN_CUT": 0.5,
        "STACK_BREAK_CUT": 0.3,
        "STACK_DEEP_CUT": 0.1,
        "HAIL_MARY": 0.1,
    },

    "RESEST_UPLINE": {
        "START": 0.0,
        "RESET_BREAK": 0.0,
        "RESEST_UPLINE": 0.0,
        "STACK_IN_CUT": 0.1,
        "STACK_BREAK_CUT": 0.0,
        "STACK_DEEP_CUT": 0.7,
        "HAIL_MARY": 0.2,
    },

    "STACK_IN_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.4,
        "RESEST_UPLINE": 0.2,
        "STACK_IN_CUT": 0.2,
        "STACK_BREAK_CUT": 0.1,
        "STACK_DEEP_CUT": 0.1,
        "HAIL_MARY": 0.0,
    },

    "STACK_BREAK_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.2,
        "RESEST_UPLINE": 0.0,
        "STACK_IN_CUT": 0.5,
        "STACK_BREAK_CUT": 0.2,
        "STACK_DEEP_CUT": 0.1,
        "HAIL_MARY": 0.0,
    },

    "STACK_DEEP_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.5,
        "RESEST_UPLINE": 0.3,
        "STACK_IN_CUT": 0.1,
        "STACK_BREAK_CUT": 0.1,
        "STACK_DEEP_CUT": 0.0,
        "HAIL_MARY": 0.0,
    },

    "HAIL_MARY": {
        "START": 0.0,
        "RESET_BREAK": 1.0,
        "RESEST_UPLINE": 0.0,
        "STACK_IN_CUT": 0.0,
        "STACK_BREAK_CUT": 0.0,
        "STACK_DEEP_CUT": 0.0,
        "HAIL_MARY": 0.0,
    },


}

# Format: (x, y)
players = [
    [100, FIELD_HEIGHT-SCORING_ZONE_HEIGHT - 50],
    [200, FIELD_HEIGHT-SCORING_ZONE_HEIGHT - 50],
    [200, FIELD_HEIGHT-SCORING_ZONE_HEIGHT - 150],
    [200, FIELD_HEIGHT-SCORING_ZONE_HEIGHT - 200],
    [200, FIELD_HEIGHT-SCORING_ZONE_HEIGHT - 250]]



class PlayMaker:
    def __init__(self, players=[]):
        self.transition_matrix = TRANSITION_MATRIX
        self.moves = list(TRANSITION_MATRIX.keys())
        self.players = players
        self.holder = 1
    
    def get_next_move(self, current_move="START"):
        return np.random.choice(
			self.moves,
			p = [self.transition_matrix[current_move][next_move] for next_move in self.moves],
		)
    
    def draw_players(self, screen):
        # print("Drawing players: ", self.players)
        for i, player in enumerate(self.players):
            if i == self.holder:
                pygame.draw.circle(screen, (255, 0, 0), player, 15)
            else:
                pygame.draw.circle(screen, (0, 0, 255), player, 15)
    

        # Draw the field
    def draw_field(self, screen):
        screen.fill(GREEN)
        pygame.draw.rect(screen, WHITE, (FIELD_WIDTH, 0, SCREEN_WIDTH-FIELD_WIDTH, SCREEN_HIGHT))  # Top scoring zone

                                        # (x, y, width, height)
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, SCORING_ZONE_HEIGHT))  # Top scoring zone
        pygame.draw.rect(screen, WHITE, (0, FIELD_HEIGHT - SCORING_ZONE_HEIGHT, FIELD_WIDTH, SCORING_ZONE_HEIGHT))  # Bottom scoring zone

        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH - FIELD_WIDTH, 0), (SCREEN_WIDTH - FIELD_WIDTH, SCREEN_HIGHT), 3)

    def move_all_players(self, right=0, up=0):
        for index in range(len(self.players)):
            self.players[index] = [self.players[index][0] + right, self.players[index][1] - up]


def main():
    playmaker = PlayMaker(players=players)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
    pygame.display.set_caption("PlayMaker Simulation")
    clock = pygame.time.Clock()


    running = True
    current_move = "START"
    font = pygame.font.Font(None, 36)

    playmaker.draw_field(screen)
    # playmaker.draw_players(screen)

    # playmaker.move_all_players(0, up=100)

    # playmaker.draw_players(screen)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # screen.fill((255, 255, 255))

        # next_move = playmaker.get_next_move(current_move)
        # text = font.render(f"Current Move: {current_move}", True, (0, 0, 0))
        # screen.blit(text, (50, 50))
        # text = font.render(f"Next Move: {next_move}", True, (0, 0, 0))
        # screen.blit(text, (50, 100))

        pygame.display.flip()
        # pygame.display.update()

        clock.tick(2)  # Update once per second

        playmaker.draw_field(screen)
        playmaker.draw_players(screen)

        playmaker.move_all_players(0, up=20)


        # current_move = next_move

    pygame.quit()


main()