import numpy as np
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

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
        "RESET_UPLINE": 0.15,
        "STACK_IN_CUT": 0.45,
        "STACK_BREAK_CUT": 0.05,
        "STACK_DEEP_CUT": 0.1,
    },

    "RESET_BREAK": {
        "START": 0.0,
        "RESET_BREAK": 0.0,
        "RESET_UPLINE": 1.0,
        "STACK_IN_CUT": 0.0,
        "STACK_BREAK_CUT": 0.0,
        "STACK_DEEP_CUT": 0.0,
    },

    "RESET_UPLINE": {
        "START": 0.0,
        "RESET_BREAK": 0.0,
        "RESET_UPLINE": 0.0,
        "STACK_IN_CUT": 0.2,
        "STACK_BREAK_CUT": 0.0,
        "STACK_DEEP_CUT": 0.8,
    },

    "STACK_IN_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.4,
        "RESET_UPLINE": 0.2,
        "STACK_IN_CUT": 0.2,
        "STACK_BREAK_CUT": 0.1,
        "STACK_DEEP_CUT": 0.1,
    },

    "STACK_BREAK_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.2,
        "RESET_UPLINE": 0.0,
        "STACK_IN_CUT": 0.5,
        "STACK_BREAK_CUT": 0.2,
        "STACK_DEEP_CUT": 0.1,
    },

    "STACK_DEEP_CUT": {
        "START": 0.0,
        "RESET_BREAK": 0.5,
        "RESET_UPLINE": 0.3,
        "STACK_IN_CUT": 0.1,
        "STACK_BREAK_CUT": 0.1,
        "STACK_DEEP_CUT": 0.0,
    },


}

#Complex transition matrix
# TRANSITION_MATRIX = {
#     "START": {
#         "START": 0.0,
#         "RESET_BREAK": 0.25,
#         "RESET_UPLINE": 0.15,
#         "STACK_IN_CUT": 0.45,
#         "STACK_BREAK_CUT": 0.05,
#         "STACK_DEEP_CUT": 0.05,
#         "HAIL_MARY": 0.05,
#     },

#     "RESET_BREAK": {
#         "START": 0.0,
#         "RESET_BREAK": 0.0,
#         "RESET_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.5,
#         "STACK_BREAK_CUT": 0.3,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.1,
#     },

#     "RESET_UPLINE": {
#         "START": 0.0,
#         "RESET_BREAK": 0.0,
#         "RESET_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.1,
#         "STACK_BREAK_CUT": 0.0,
#         "STACK_DEEP_CUT": 0.7,
#         "HAIL_MARY": 0.2,
#     },

#     "STACK_IN_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.4,
#         "RESET_UPLINE": 0.2,
#         "STACK_IN_CUT": 0.2,
#         "STACK_BREAK_CUT": 0.1,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.0,
#     },

#     "STACK_BREAK_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.2,
#         "RESET_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.5,
#         "STACK_BREAK_CUT": 0.2,
#         "STACK_DEEP_CUT": 0.1,
#         "HAIL_MARY": 0.0,
#     },

#     "STACK_DEEP_CUT": {
#         "START": 0.0,
#         "RESET_BREAK": 0.5,
#         "RESET_UPLINE": 0.3,
#         "STACK_IN_CUT": 0.1,
#         "STACK_BREAK_CUT": 0.1,
#         "STACK_DEEP_CUT": 0.0,
#         "HAIL_MARY": 0.0,
#     },

#     "HAIL_MARY": {
#         "START": 0.0,
#         "RESET_BREAK": 1.0,
#         "RESET_UPLINE": 0.0,
#         "STACK_IN_CUT": 0.0,
#         "STACK_BREAK_CUT": 0.0,
#         "STACK_DEEP_CUT": 0.0,
#         "HAIL_MARY": 0.0,
#     },


# }

# Format: (x, y)
players_starting = [
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
        self.last_in_stack = len(self.players) - 1
    
    def get_next_move(self, current_move="START"):
        return np.random.choice(
			self.moves,
			p = [self.transition_matrix[current_move][next_move] for next_move in self.moves],
		)
    
    def draw_players(self, screen):
        for i, player in enumerate(self.players):
            if i == self.holder:
                pygame.draw.circle(screen, (255, 0, 0), player, 15)
            else:
                pygame.draw.circle(screen, (0, 0, 255), player, 15)
    

        # Draw the field
    def draw_field(self, screen):
        screen.fill(GREEN)
        pygame.draw.rect(screen, WHITE, (FIELD_WIDTH, 0, SCREEN_WIDTH-FIELD_WIDTH, SCREEN_HEIGHT))  # Right stats zone

                                        # (x, y, width, height)
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, SCORING_ZONE_HEIGHT))  # Top scoring zone
        pygame.draw.rect(screen, WHITE, (0, FIELD_HEIGHT - SCORING_ZONE_HEIGHT, FIELD_WIDTH, SCORING_ZONE_HEIGHT))  # Bottom scoring zone

        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH - FIELD_WIDTH, 0), (SCREEN_WIDTH - FIELD_WIDTH, SCREEN_HEIGHT), 3)

    def move_all_players_detla(self, right=0, up=0, exclude_index=None):

        for index in range(len(self.players)):
            if index == exclude_index:
                continue
            self.players[index][0] += right
            self.players[index][1] -= up
    
    def move_player(self, index, x, y):
        if index == self.holder:
            raise ValueError(f'Cannot move the disc holder: {index}')
        
        self.players[index][0] = x
        self.players[index][1] = y
    
    def get_player_pos(self, index):
        return self.players[index]

    def update_disc_pos(self):
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]

    def check_point_scored(self):
        # print("POINT")
        return self.disc_pos[1] <= SCORING_ZONE_HEIGHT


    def return_to_position(self, index):
        if index == 0:  # Secondarily handler
            handler_pos = self.get_player_pos(1)
            self.move_player(index, handler_pos[0]-HANDLER_OFFSET ,handler_pos[1])
        
        elif index == 1:  # Primarily handler
            handler_pos = self.get_player_pos(0)
            self.move_player(index, handler_pos[0]+HANDLER_OFFSET, handler_pos[1])
       
        elif index == 2:  # First in stack
            stack_mid_pos = self.get_player_pos(3)
            self.move_player(index, stack_mid_pos[0], stack_mid_pos[1] + STACK_SPACING)

            # Fix for weird edge case would go here

        elif index == 3:  # Second in stack
            front_stack_pos = self.get_player_pos(2)
            self.move_player(index, front_stack_pos[0], front_stack_pos[1] - STACK_SPACING)

            self.last_in_stack == 4

        elif index == 4:  # Third in stack
            stack_mid_pos = self.get_player_pos(2)
            self.move_player(index, stack_mid_pos[0], stack_mid_pos[1] - STACK_SPACING*2)
            self.last_in_stack == 4

    def move_all_after_cut(self):
        self.move_all_players_detla(0, up=self.get_player_pos(0)[1] - self.disc_pos[1], exclude_index=self.holder)


    def pass_to_player_and_clear(self, player_index):

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
            self.pass_to_player_and_clear(1)

        else:
            self.pass_to_player_and_clear(0)

    def make_in_cut(self):
        current_pos = self.get_player_pos(self.last_in_stack)
        if self.last_in_stack == 4:
            self.move_player(self.last_in_stack, current_pos[0] + 100, current_pos[1] + 100) # Move a bit down and right
        elif self.last_in_stack == 3:
            self.move_player(self.last_in_stack, current_pos[0] + 100, current_pos[1]) # Just move right
        else:
            raise ValueError(f'Too many cuts: {self.last_in_stack}')

    def make_in_cut_break(self):
        current_pos = self.get_player_pos(self.last_in_stack)
        self.move_player(self.last_in_stack, current_pos[0] - 100, current_pos[1] + 100)


    def make_deep_cut(self):
        self.move_player(self.last_in_stack, FIELD_WIDTH * 0.75, SCORING_ZONE_HEIGHT/2)

    

    def pass_to_cut(self):
        self.pass_to_player_and_clear(self.last_in_stack)
        self.last_in_stack -= 1

    def handle_cut_transitions(self, clock, screen):
            self.draw_field(screen)
            self.draw_players(screen)
        
            pygame.display.flip()
            clock.tick(1)

            self.pass_to_cut()

            self.draw_field(screen)
            self.draw_players(screen)

            pygame.display.flip()
            clock.tick(1)

            self.move_all_after_cut()

            self.draw_field(screen)
            self.draw_players(screen)

            pygame.display.flip()
            clock.tick(1)
    
    def do_next_move(self, next_move, clock=None, screen=None):
        if next_move == "RESET_BREAK":
            self.pass_to_reset()
        elif next_move == "RESET_UPLINE":
            self.pass_to_reset()
        elif next_move == "STACK_IN_CUT":
            self.make_in_cut()
            self.handle_cut_transitions(clock, screen)

        elif next_move == "STACK_BREAK_CUT":
            self.make_in_cut_break()
            self.handle_cut_transitions(clock, screen)


        elif next_move == "STACK_DEEP_CUT":
            self.make_deep_cut()
            self.handle_cut_transitions(clock, screen)

        else:
            raise ValueError(f'Invalid move: {next_move}')


def main():
    playmaker = PlayMaker(players=players_starting)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PlayMaker Simulation")
    clock = pygame.time.Clock()

    playmaker.draw_field(screen)
    playmaker.draw_players(screen)
    
    running = True
    current_move = playmaker.get_next_move("START")
    i = 0
    # while running:
    #     i += 1
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #     if i == 3:
    #         print(f'Before in cut last in stack: {playmaker.last_in_stack}')
    #         playmaker.do_next_move("STACK_IN_CUT", clock=clock, screen=screen)
    #         print(f'After in cut last in stack: {playmaker.last_in_stack}')
        
    #     # if i == 5:
    #     #     playmaker.pass_to_cut()
        
    #     # if i == 7:
    #     #     playmaker.move_all_after_cut()

    #     # if i == 7:
    #     #     playmaker.do_next_move("RESET_BREAK")
        
    #     if i == 5:
    #         print(f'Before deep cut last in stack: {playmaker.last_in_stack}')
    #         playmaker.do_next_move("STACK_IN_CUT", clock=clock, screen=screen)
    #         print(f'After deep cut last in stack: {playmaker.last_in_stack}')

    #     if i == 7:
    #         playmaker.do_next_move("STACK_DEEP_CUT", clock=clock, screen=screen)

    #     playmaker.draw_field(screen)
    #     playmaker.draw_players(screen)

    #     pygame.display.flip()

    #     clock.tick(1)



    moves = [current_move]

    while running:

        i += 1
        print(f'\n\nIteration: {i}, Current Move: {current_move}')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False            

        
        playmaker.do_next_move(current_move, clock=clock, screen=screen)

        playmaker.draw_field(screen)
        playmaker.draw_players(screen)

        pygame.display.flip()

        if playmaker.check_point_scored():
            running = False
        else:
            current_move = playmaker.get_next_move(current_move)
            moves.append(current_move)

        clock.tick(1)  # Update once per second
        # pygame.time.wait(5000)


    print("Game Over")
    print(f'Moves: {moves}')
    # pygame.quit()


main()