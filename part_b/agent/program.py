# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

import random
from referee.game import PlayerColor, Action, PlaceAction, Coord

# set the number of moves to be check and the depth of minimax as a global constant
MAX_MOVES = 64
MAX_DEPTH = 5

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    # Class attribute that stores all the place actions that has been played by both agents
    place_action_list = []
    place_action_red = []
    place_action_blue = []
    current_red = []
    current_blue = []
    player_move_count = 0

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.

        # adjust the depth of search based on the current game state (search deeper at the later stage)
        occupied = (len(self.current_red) + len(self.current_blue))
        depth = MAX_DEPTH
        if occupied <= 100:
            depth-=1
        if occupied <= 80:
            depth-=1
        if occupied <= 60:
            depth-=1
        if occupied <= 40:
            depth-=1
        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                if self.player_move_count == 0:
                    place_action_coords = self.random_move(PlayerColor.RED, self.current_red,
                                                           self.current_blue, self.player_move_count)
                    self.player_move_count+=1
                    return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
                value, place_action_coords = self.minimax(True, depth, self.current_red, self.current_blue, [], [])
                return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                if self.player_move_count == 0:
                    place_action_coords = self.random_move(PlayerColor.BLUE, self.current_red,
                                                           self.current_blue, self.player_move_count)
                    self.player_move_count+=1
                    return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
                value, place_action_coords = self.minimax(False, depth, self.current_red, self.current_blue, [], [])
                # print(f"Utility score of the move: {value}")
                return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.

        # Store all the place actions that has been played by both
        # agents in a list
    
        self.place_action_list.append(action)
        if color == PlayerColor.RED:
            self.place_action_red.append(action)
            for block in list(place_action.coords):
                self.current_red.append(block)
        else:
            self.place_action_blue.append(action)
            for block in list(place_action.coords):
                self.current_blue.append(block)

        self.current_red, self.current_blue, _ = self.eliminate_lines(self.current_red, self.current_blue)

    # generate a list of possible moves and number of moves given the current state
    def possible_moves(self, color: PlayerColor, red, blue):
        not_expandable_block = red[:] + blue[:]

        blocks = red
        if color == PlayerColor.BLUE:
            blocks = blue
        
        actions = []
        for block in blocks:
            if (block.up(1) not in not_expandable_block):
                temp_list = []
                temp_list.append(block.up(1))
                actions.append(temp_list)
            if (block.down(1) not in not_expandable_block):
                temp_list = []
                temp_list.append(block.down(1))
                actions.append(temp_list)
            if (block.left(1) not in not_expandable_block):
                temp_list = []
                temp_list.append(block.left(1))
                actions.append(temp_list)
            if (block.right(1) not in not_expandable_block):
                temp_list = []
                temp_list.append(block.right(1))
                actions.append(temp_list)
        # return None if no empty adjacent block
        if len(actions) == 0:
            return None
        # keep adding adjacent red blocks until it is long enough (4 blocks) to form a place action
        while len(actions[0]) < 4:
            possible_move = actions.pop(0)
            for block in list(possible_move):
                if (block.up(1) not in not_expandable_block and block.up(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.up(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate:
                        actions.append(clone)
                if (block.down(1) not in not_expandable_block and block.down(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.down(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate:
                        actions.append(clone)
                if (block.left(1) not in not_expandable_block and block.left(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.left(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate:
                        actions.append(clone)
                if (block.right(1) not in not_expandable_block and block.right(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.right(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate:
                        actions.append(clone)
            if len(actions) == 0: return None
        return actions

    # calculate utility of a possible move
    def utility(self, color: PlayerColor, new_red, new_blue, red, blue):
        # generate possible moves and calculate the utility score
        possible_moves = self.possible_moves(color, new_red, new_blue)
        # reward given when more possible moves are available
        possible_moves_reward = len(possible_moves) if possible_moves != None else 0
        # reward given when player's block is more than the opponent's block
        block_diff_reward = len(new_red) - len(new_blue)
        # reward given when the new state has less block than the old state, i.e. clearing lines
        block_clear_reward = len(red) + len(blue) - (len(new_red) + len(new_blue))
        # calculate the block eliminated for each player
        red_diff_reward = len(new_red) - len(red)
        blue_diff_reward = len(new_blue) - len(blue)
        # assign weighting for each state of the game based on the number of blocks occupied
        if (len(red) + len(blue)) >= 60:
            red_diff_reward*=3
            blue_diff_reward*=3
        if (len(red) + len(blue)) >= 80:
            red_diff_reward*=5
            block_diff_reward*=5
            possible_moves_reward*=3
            block_clear_reward*=3
        if (len(red) + len(blue)) >= 100:
            possible_moves_reward*=5
            red_diff_reward*=10
            block_diff_reward*=10
            block_clear_reward*=5

        # calculate utility for each player
        if color == PlayerColor.RED:
            # no possible move for red -> blue win, score = -inf
            if possible_moves == None: return float('-inf')
            score = block_diff_reward + possible_moves_reward + block_clear_reward - red_diff_reward + blue_diff_reward
        else:
            # no possible move for blue -> red win, score = inf
            if possible_moves == None: return float('inf')
            score = block_diff_reward - possible_moves_reward - block_clear_reward - red_diff_reward + blue_diff_reward
        return score

    
    # return an action based on the utility of given moves by using the minimax strategy
    # can implement ab pruning in this function
    def minimax(self, maximizing, depth, new_red, new_blue, red, blue, alpha=float('-inf'), beta=float('inf')):
        # determine the maximum moves to be checked based on the current game state (number of occupied blocks)
        occupied = len(new_red) + len(new_blue)
        initial_depth = MAX_DEPTH
        max_moves = MAX_MOVES
        if occupied <= 100:
            max_moves = MAX_MOVES/2
            initial_depth-=1
        if occupied <= 80:
            max_moves = MAX_MOVES/4
            initial_depth-=1
        if occupied <= 60:
            max_moves = MAX_MOVES/16
            initial_depth-=1
        if occupied <= 40:
            max_moves = MAX_MOVES/32
            initial_depth-=1
        move_check = (max_moves)/(2 ** (initial_depth - depth))
        if occupied <= 100 and depth != MAX_DEPTH: move_check/=2
        # return the utility score if no possible move or reached the maximum depth
        if maximizing:
            moves = self.possible_moves(PlayerColor.RED, new_red, new_blue)
            # cut off a node with the number of possible moves more than the maximum moves check number
            if moves is None or (len(moves) > move_check and depth != initial_depth) or depth == 0:
                return self.utility(PlayerColor.RED, new_red, new_blue, red, blue), None
        else:
            # do the same thing for the minimising player (blue)
            moves = self.possible_moves(PlayerColor.BLUE, new_red, new_blue)
            if moves is None or (len(moves) > move_check and depth != initial_depth) or depth == 0:
                return self.utility(PlayerColor.BLUE, new_red, new_blue, red, blue), None

        # counting the number of moves checked
        move_counts = 0
        # implementing minmax
        if maximizing:
            value = float('-inf')
            best_movement = None
            for move in moves:
                move_counts+=1
                # eliminate lines if there are filled lines
                new_red_, new_blue_, _ = self.eliminate_lines(new_red[:]+move, new_blue)
                score = self.minimax(False, depth - 1, new_red_, new_blue_, new_red, new_blue)[0]
                if score >= value:
                    value = score
                    best_movement = move
                # implementing alpha-beta pruning for maximizing player (red)
                if value >= beta:
                    break
                alpha = max(alpha, value)
                # cut off if the number of moves reached the maximum moves to be checked
                if move_counts >= max_moves: break
        else:
            value = float('inf')
            best_movement = None
            for move in moves:
                move_counts+=1
                # eliminate lines if there are filled lines
                new_red_, new_blue_, _ = self.eliminate_lines(new_red, new_blue[:]+move)
                score = self.minimax(True, depth - 1, new_red_, new_blue_, new_red, new_blue)[0]
                if score <= value:
                    value = score
                    best_movement = move
                # implementing alpha-beta pruning for minimizing player (blue)
                if value <= alpha:
                    break
                beta = min(beta, value)
                # cut off if the number of moves reached the maximum moves to be checked 
                if move_counts >= max_moves: break
        return value, best_movement
    
    def random_move(self, color, red, blue, move_count):
        # Randomly select 4 adjacent blocks on the board that hasn't been placed yet
        # Check whether the randomly selected blocks have been placed in the game board
        place_action_coords = []

        all_curr_coords = red + blue

        action_arr = red if color == PlayerColor.RED else blue

        coord_loop_count = 0

        while len(place_action_coords) < 4:

            if coord_loop_count > 500:
                place_action_coords.clear()
                coord_loop_count = 0
            
            coord_already_placed = False
            # Randomly select a coord
            xcoord = random.randint(0, 10)
            ycoord = random.randint(0, 10)

            right = xcoord + 1
            if right == 11: right = 0
            left = xcoord - 1
            if left == -1: left = 10
            up = ycoord + 1
            if up == 11: up = 0
            down = ycoord - 1
            if down == -1: down = 10
            
            # Check if the coord has been placed on the board
            for coord in all_curr_coords:
                if Coord(xcoord, ycoord) == coord:
                    coord_already_placed = True
                    break
            if coord_already_placed:
                continue

            # If this is the first move of the game and no coord has been chosen
            # then add the coord to the place_action_coords list
            if len(place_action_coords) == 0 and move_count == 0:
                if Coord(xcoord, ycoord) not in place_action_coords:
                    place_action_coords.append(Coord(xcoord, ycoord))
            
            # If this is not the first move of the game and no coord has been chosen
            # then check if the coord is adjacent to any of the coords that has been
            # chosen before by the player. If it is, add the coord to the place_action_coords list
            elif len(place_action_coords) == 0 and move_count != 0:
                if Coord(xcoord, ycoord) not in place_action_coords:

                    for coord in action_arr:
                        if right == coord.r and ycoord == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                            break
                        elif left == coord.r and ycoord == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                            break
                        elif xcoord == coord.r and up == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                            break
                        elif xcoord == coord.r and down == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                            break
                        else:
                            continue

            # If this is not the first move of the game and some coords have been chosen
            # then check if the coord is adjacent to any of the coords that has been
            # chosen in the place_action_coords list. If it is, add the coord to the place_action_coords list
            else:
                if Coord(xcoord, ycoord) not in place_action_coords:
                    for coord in place_action_coords:
                        if right == coord.r and ycoord == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif left == coord.r and ycoord == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif xcoord == coord.r and up == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif xcoord == coord.r and down == coord.c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                coord_loop_count += 1

        return place_action_coords


    def eliminate_lines(self, red, blue):
        elimiated = False
        red_clone = red[:]
        blue_clone = blue[:]
        block = red_clone + blue_clone
        eliminated_coords_list = []
        # check if there are any completed rows. If there are, add these coords to the eliminated_coords_list.
        for i in range(11):
            row = []
            for j in range(11):
                row.append(Coord(i, j))
            if set(row).issubset(set(block)):
                for coord in row:
                    eliminated_coords_list.append(coord)
        # check if there are any completed columns. If there are, add these coords to the eliminated_coords_list.
        for i in range(11):
            column = []
            for j in range(11):
                column.append(Coord(j, i))
            if set(column).issubset(set(block)):
                for coord in column:
                    eliminated_coords_list.append(coord)
        # Go through the eliminated_coords_list and remove all the non-expandable blocks that are a part of 
        # any complete rows or columns.
        for coord in eliminated_coords_list:
            if coord in red_clone: red_clone.remove(coord)
            if coord in blue_clone: blue_clone.remove(coord)
            if coord in block: block.remove(coord)
        if len(eliminated_coords_list) > 0 : elimiated = True
        return red_clone, blue_clone, elimiated
