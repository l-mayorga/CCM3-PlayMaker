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

HANDLER_OFFSET = 100
STACK_SPACING = 50

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
        "RESEST_UPLINE": 1.0,
        "STACK_IN_CUT": 0.0,
        "STACK_BREAK_CUT": 0.0,
        "STACK_DEEP_CUT": 0.0,
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

#Complex transition matrix
# TRANSITION_MATRIX = {
#     "START": {
#         "START": 0.0,
#         "RESET_BREAK": 0.25,
#         "RESEST_UPLINE": 0.15,
#         "STACK_IN_CUT": 0.45,
#         "STACK_BREAK_CUT": 0.05,
#         "STACK_DEEP_CUT": 0.05,
#         "HAIL_MARY": 0.05,
#     },

#     "RESET_BREAK": {
#         "START": 0.0,
#         "RESET_BREAK": 0.0,
#         "RESEST_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.5,
#         "STACK_BREAK_CUT": 0.3,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.1,
#     },

#     "RESEST_UPLINE": {
#         "START": 0.0,
#         "RESET_BREAK": 0.0,
#         "RESEST_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.1,
#         "STACK_BREAK_CUT": 0.0,
#         "STACK_DEEP_CUT": 0.7,
#         "HAIL_MARY": 0.2,
#     },

#     "STACK_IN_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.4,
#         "RESEST_UPLINE": 0.2,
#         "STACK_IN_CUT": 0.2,
#         "STACK_BREAK_CUT": 0.1,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.0,
#     },

#     "STACK_BREAK_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.2,
#         "RESEST_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.5,
#         "STACK_BREAK_CUT": 0.2,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.0,
#     },

#     "STACK_DEEP_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.5,
#         "RESEST_UPLINE": 0.3,
#         "STACK_IN_CUT": 0.1,
#         "STACK_BREAK_CUT": 0.1,
#         "STACK_DEEP_CUT": 0.0,
#         "HAIL_MARY": 0.0,
#     },

#     "HAIL_MARY": {
#         "START": 0.0,
#         "RESET_BREAK": 1.0,
#         "RESEST_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.0,
#         "STACK_BREAK_CUT": 0.0,
#         "STACK_DEEP_CUT": 0.0,
#         "HAIL_MARY": 0.0,
#     },


# }

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
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]
    
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

    def move_all_players_detla(self, right=0, up=0, exclude_index=None):

        for index in range(len(self.players)):
            if index == exclude_index:
                continue
            self.players[index][0] += right
            self.players[index][1] -= up
    
    def move_player(self, index, x, y):
        self.players[index][0] = x
        self.players[index][1] = y
    
    def get_player_pos(self, index):
        return self.players[index]

    def update_disc_pos(self):
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]


    def return_to_position(self, index):
        print("Returning to position: ", index)
        if index == 0:
            handler_pos = self.get_player_pos(1)
            self.move_player(index, handler_pos[0]-HANDLER_OFFSET ,handler_pos[1])
        
        elif index == 1:
            handler_pos = self.get_player_pos(0)
            # print("Handler pos: ", handler_pos)
            self.move_player(index, handler_pos[0]+HANDLER_OFFSET, handler_pos[1])

        elif index == 3:
            front_stack_pos = self.get_player_pos(2)
            self.move_player(index, front_stack_pos[0], front_stack_pos[1] - STACK_SPACING)

        elif index == 2:
            stack_mid_pos = self.get_player_pos(3)
            self.move_player(index, stack_mid_pos[0], stack_mid_pos[1] + STACK_SPACING)

        elif index == 4:
            stack_mid_pos = self.get_player_pos(3)
            self.move_player(index, stack_mid_pos[0], stack_mid_pos[1] - STACK_SPACING)



    def pass_to_player(self, player_index):

        if player_index < 0:
            raise ValueError(f'Player index {player_index} is out of bounds; it must be non-negative.')
        if player_index >= len(self.players):
            raise ValueError(f'Player index {player_index} is out of bounds; it must be less than {len(self.players)}.')
        if player_index == self.holder:
            raise ValueError(f'Player index {player_index} is the current holder; it must be a different player.')
        old_holder = self.holder
        self.holder = player_index
        self.update_disc_pos()
        self.return_to_position(old_holder)

    def pass_to_reset(self):
        if self.holder != 1:
            self.pass_to_player(1)

        else:
            self.pass_to_player(0)

    
    def pass_to_in_cut(self):
        self.pass_to_player(2)
    
    def pass_to_deep_cut(self):
        self.pass_to_player(4)
    
    def do_next_move(self, next_move):
        if next_move == "RESET_BREAK":
            self.pass_to_reset()
        
        elif next_move == "RESEST_UPLINE":
            self.pass_to_reset()
        elif next_move == "STACK_IN_CUT":
            self.pass_to_in_cut()
        elif next_move == "STACK_BREAK_CUT":
            pass
        elif next_move == "STACK_DEEP_CUT":
            pass
        elif next_move == "HAIL_MARY":
            pass



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

    # pygame.display.flip()
    # # pygame.display.update()

    # # clock.tick(1)  # Update once per second

    # playmaker.draw_field(screen)
    # playmaker.draw_players(screen)
    # pygame.display.flip()

    # playmaker.move_all_players_detla(0, up=20, exclude_index=playmaker.holder)


    # pygame.display.flip()

    # if playmaker.holder != 4:
    #     playmaker.pass_to_deep_cut()

    i = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # next_move = playmaker.get_next_move(current_move)
        # text = font.render(f"Current Move: {current_move}", True, (0, 0, 0))
        # screen.blit(text, (50, 50))
        # text = font.render(f"Next Move: {next_move}", True, (0, 0, 0))
        # screen.blit(text, (50, 100))

        pygame.display.flip()
        # pygame.display.update()

        clock.tick(1)  # Update once per second

        playmaker.draw_field(screen)
        playmaker.draw_players(screen)

        # playmaker.move_all_players_detla(0, up=20, exclude_index=playmaker.holder)
        if i <= 2:
            playmaker.move_all_players_detla(0, up=20, exclude_index=playmaker.holder)
        
        if i == 3:
            playmaker.do_next_move("RESET_BREAK")

        if i == 4:
            playmaker.move_player(3, 100,  100)

        if i == 5 or i == 6:
            playmaker.move_all_players_detla(0, up=20, exclude_index=playmaker.holder)

        if i == 7:
            playmaker.return_to_position(3)

        if i == 8:
            playmaker.pass_to_reset()

        # if playmaker.holder != 4:
        #     playmaker.pass_to_deep_cut()


        # current_move = next_move

        i += 1

    pygame.quit()


main()