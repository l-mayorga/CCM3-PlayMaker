import numpy as np
import pygame

# Define screen dimensions
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
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Define various player field spacings
STARTING_HANDLER_Y_OFFSET = 50
SECONDARY_HANDLER_STARTING_X = 100
PLAYER_STARTING_X = 200
HANDLER_OFFSET = 100
STACK_SPACING = 50

# Define moves list spacing
MOVES_LIST_SPACING = 50

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

# The starting positions of the players.
# The ith player is at players_starting[i]
PLAYERS_STARTING_POSITIONS = [
    # format: [x, y]
    [
        SECONDARY_HANDLER_STARTING_X,
        FIELD_HEIGHT - SCORING_ZONE_HEIGHT - STARTING_HANDLER_Y_OFFSET,
    ],
    [PLAYER_STARTING_X, FIELD_HEIGHT - SCORING_ZONE_HEIGHT - STARTING_HANDLER_Y_OFFSET],
    [PLAYER_STARTING_X, FIELD_HEIGHT - SCORING_ZONE_HEIGHT - 3 * STACK_SPACING],
    [PLAYER_STARTING_X, FIELD_HEIGHT - SCORING_ZONE_HEIGHT - 4 * STACK_SPACING],
    [PLAYER_STARTING_X, FIELD_HEIGHT - SCORING_ZONE_HEIGHT - 5 * STACK_SPACING],
]


class PlayMaker:
    def __init__(self, players=[]):
        self.transition_matrix = TRANSITION_MATRIX
        self.moves = list(TRANSITION_MATRIX.keys())
        self.players = players
        self.holder = 1
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]
        self.last_in_stack = len(self.players) - 1

    def reset(self):
        self.players = PLAYERS_STARTING_POSITIONS
        self.holder = 1
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]
        self.last_in_stack = len(self.players) - 1
        self.update_disc_pos()

    def get_next_move(self, current_move="START"):
        return np.random.choice(
            self.moves,
            p=[
                self.transition_matrix[current_move][next_move]
                for next_move in self.moves
            ],
        )

    def draw_initial(self, screen):
        """Draw the initial screen elements that are not redrawn each turn."""
        # Right stats panel
        pygame.draw.rect(
            screen, WHITE, (FIELD_WIDTH, 0, SCREEN_WIDTH - FIELD_WIDTH, SCREEN_HEIGHT)
        )

        # Divider line
        pygame.draw.line(
            screen,
            BLACK,
            (SCREEN_WIDTH - FIELD_WIDTH, 0),
            (SCREEN_WIDTH - FIELD_WIDTH, SCREEN_HEIGHT),
            3,
        )

    def render_moves_list_text(self, moves, screen, font):
        """Render the list of moves on the right side of the screen."""
        for i, move in enumerate(moves):
            text_surface = font.render(move, True, BLACK)
            screen.blit(text_surface, (FIELD_WIDTH + 20, 20 + i * MOVES_LIST_SPACING))

    def render_score_text(self, screen, font):
        """Render the 'SCORE!' text on the screen."""
        print("SCORE!")
        text_surface = font.render("SCORE!", True, RED)
        screen.blit(text_surface, (FIELD_WIDTH + 20, SCREEN_HEIGHT * 0.8))

    def draw_players(self, screen):
        """Draw the players on the field according to the positions in self.players."""
        for i, player in enumerate(self.players):
            if i == self.holder:
                pygame.draw.circle(screen, (255, 0, 0), player, 15)
            else:
                pygame.draw.circle(screen, (0, 0, 255), player, 15)

    def draw_field_and_scoring_zones(self, screen):
        """Draw the field and scoring zones on the screen."""
        pygame.draw.rect(screen, GREEN, (0, 0, FIELD_WIDTH, FIELD_HEIGHT))  # Field
        pygame.draw.rect(  # Top scoring zone
            screen, ORANGE, (0, 0, FIELD_WIDTH, SCORING_ZONE_HEIGHT)
        )
        pygame.draw.rect(  # Bottom scoring zone
            screen,
            ORANGE,
            (0, FIELD_HEIGHT - SCORING_ZONE_HEIGHT, FIELD_WIDTH, SCORING_ZONE_HEIGHT),
        )

    def move_all_players_delta(self, right=0, up=0, exclude_index=None):
        """Move all players by the given delta values, except for the player at exclude_index.
        This should almost always be the disc holder.
        """
        for index in range(len(self.players)):
            if index == exclude_index:
                continue
            self.players[index][0] += right
            self.players[index][1] -= up

    def move_player(self, index, x, y):
        """Move the player at index to the given x and y coordinates."""
        if index == self.holder:
            raise ValueError(f"Cannot move the disc holder: {index}")

        self.players[index][0] = x
        self.players[index][1] = y

    def get_player_pos(self, index):
        """Return the position of the player at index."""
        return self.players[index]

    def update_disc_pos(self):
        """Update the disc position to the current holder's position."""
        self.disc_pos = [self.players[self.holder][0], self.players[self.holder][1]]

    def check_point_scored(self):
        """Check if a point has been scored."""
        print("SCORE!")
        return self.disc_pos[1] <= SCORING_ZONE_HEIGHT

    def return_to_position(self, index):
        """Return the player at index to their starting position."""
        if index == 0:  # Secondarily handler. Position based on primary handler.
            handler_pos = self.get_player_pos(1)
            self.move_player(index, handler_pos[0] - HANDLER_OFFSET, handler_pos[1])

        elif index == 1:  # Primarily handler. Position based on the secondary handler.
            handler_pos = self.get_player_pos(0)
            self.move_player(index, handler_pos[0] + HANDLER_OFFSET, handler_pos[1])

        elif index == 2:  # First in stack. Position based on 2nd in stack.
            stack_mid_pos = self.get_player_pos(3)
            self.move_player(index, stack_mid_pos[0], stack_mid_pos[1] + STACK_SPACING)

        elif index == 3:  # Second in stack. Position based on 1st in stack.
            front_stack_pos = self.get_player_pos(2)
            self.move_player(
                index, front_stack_pos[0], front_stack_pos[1] - STACK_SPACING
            )

            self.last_in_stack == 4

        elif index == 4:  # Third in stack. Position based on 1st in stack.
            stack_mid_pos = self.get_player_pos(2)
            self.move_player(
                index, stack_mid_pos[0], stack_mid_pos[1] - STACK_SPACING * 2
            )
            self.last_in_stack == 4

    def move_all_after_cut(self):
        """Move all players after a cut has been made."""
        self.move_all_players_delta(
            0,
            up=self.get_player_pos(0)[1] - self.disc_pos[1],
            exclude_index=self.holder,
        )

    def pass_to_player_and_clear(self, player_index):
        """Pass the disc to the player at player_index and "clear" (move) back to position."""
        if player_index < 0:
            raise ValueError(
                f"Player index {player_index} is out of bounds; it must be non-negative."
            )
        if player_index >= len(self.players):
            raise ValueError(
                f"Player index {player_index} is out of bounds; it must be less than {len(self.players)}."
            )
        if player_index == self.holder:
            raise ValueError(
                f"Player index {player_index} is the current holder; it must be a different player."
            )
        old_holder = self.holder
        self.holder = player_index
        self.update_disc_pos()
        self.return_to_position(old_holder)

    def pass_to_reset(self):
        """Pass the disc to the reset handler and clear back to position."""
        if self.holder != 1:
            self.pass_to_player_and_clear(1)

        else:
            self.pass_to_player_and_clear(0)

    def make_in_cut(self):
        """Make an in cut from the stack on the open (right) side of the field."""
        current_pos = self.get_player_pos(self.last_in_stack)
        if self.last_in_stack == 4:
            self.move_player(
                self.last_in_stack, current_pos[0] + 100, current_pos[1] + 100
            )  # Move a bit down and right
        elif self.last_in_stack == 3:
            self.move_player(
                self.last_in_stack, current_pos[0] + 100, current_pos[1]
            )  # Just move right
        else:
            raise ValueError(f"Too many cuts: {self.last_in_stack}")

    def make_in_cut_break(self):
        """Make an in cut from the stack on the break (left) side of the field."""
        current_pos = self.get_player_pos(self.last_in_stack)
        self.move_player(self.last_in_stack, current_pos[0] - 100, current_pos[1] + 100)

    def make_deep_cut(self):
        """Make a deep cut from the stack. This cut will go into the scoring zone."""
        self.move_player(
            self.last_in_stack, FIELD_WIDTH * 0.75, SCORING_ZONE_HEIGHT / 2
        )

    def pass_to_cut(self):
        """Pass the disc to the player who has just cut."""
        self.pass_to_player_and_clear(self.last_in_stack)
        self.last_in_stack -= 1

    def handle_cut_transitions(self, clock, screen):
        """Handle the transitions that occur after a cut has been made.
        This is required to show the cut, the pass, and the movement of the other players.
        """
        self.draw_field_and_scoring_zones(screen)
        self.draw_players(screen)

        pygame.display.flip()
        clock.tick(1)

        self.pass_to_cut()

        self.draw_field_and_scoring_zones(screen)
        self.draw_players(screen)

        pygame.display.flip()
        clock.tick(1)

        self.move_all_after_cut()

        self.draw_field_and_scoring_zones(screen)
        self.draw_players(screen)

        pygame.display.flip()
        clock.tick(1)

    def perform_next_move(self, next_move, clock=None, screen=None):
        """Perform the next move in the game."""
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
            raise ValueError(f"Unknown move: {next_move}")


def main():
    """
    Run the PlayMaker simulation.

    """
    playmaker = PlayMaker(players=PLAYERS_STARTING_POSITIONS)

    playmaker.reset()

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PlayMaker Simulation")

    moves_list_font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 56)

    clock = pygame.time.Clock()

    playmaker.draw_initial(screen)
    playmaker.draw_field_and_scoring_zones(screen)
    playmaker.draw_players(screen)

    running = True
    current_move = playmaker.get_next_move("START")
    moves = [current_move]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        playmaker.render_moves_list_text(moves, screen, moves_list_font)

        playmaker.perform_next_move(current_move, clock=clock, screen=screen)

        playmaker.draw_field_and_scoring_zones(screen)
        playmaker.draw_players(screen)

        pygame.display.flip()

        if playmaker.check_point_scored():
            playmaker.render_score_text(screen, score_font)
            pygame.display.flip()
            pygame.time.wait(5000)  # wait 5 seconds before closing
            running = False
        else:
            current_move = playmaker.get_next_move(current_move)
            moves.append(current_move)

        clock.tick(1)  # 1 fps

    print(f"Moves: {moves}")
    pygame.quit()


main()
