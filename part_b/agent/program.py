# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

import random
from referee.game import PlayerColor, Action, PlaceAction, Coord

MAX_MOVES = 32
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
                value, place_action_coords = self.minimax(True, MAX_DEPTH, self.current_red, self.current_blue, [], [])
                # print(f"Utility score of the move: {value}")
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
                value, place_action_coords = self.minimax(False, MAX_DEPTH, self.current_red, self.current_blue, [], [])
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
        c1, c2, c3, c4 = place_action.coords

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

        possible_moves = self.possible_moves(color, new_red, new_blue)
        block_clear_reward = 0
        possible_moves_reward = len(possible_moves) if possible_moves != None else 0
        block_diff_reward = len(new_red) - len(new_blue)
        if (len(red) + len(blue)) >= 80:
            prev_new_difference = len(red) + len(blue) - (len(new_red) + len(new_blue))
            block_clear_reward = prev_new_difference*2
            block_diff_reward*=3
            possible_moves_reward*=5

        if color == PlayerColor.RED:
            # no possible move for red -> blue win, score = -inf
            if possible_moves == None: return float('-inf')
            score = block_diff_reward + possible_moves_reward + block_clear_reward
        else:
            # no possible move for blue -> red win, score = inf
            if possible_moves == None: return float('inf')
            score = block_diff_reward - possible_moves_reward - block_clear_reward
        return score

    
    # return an action based on the utility of given moves by using the minimax strategy
    # can implement ab pruning in this function
    def minimax(self, maximizing, depth, new_red, new_blue, red, blue, alpha=float('-inf'), beta=float('inf')):
        # generate possible moves for given state (red and blue)
        # if no possible move, return the utility
        # extra_move_check = 0 if depth <= 1 else 2
        move_check = MAX_MOVES/(2 ** (MAX_DEPTH - depth)) if depth != 1 else MAX_MOVES - 20
        if maximizing:
            moves = self.possible_moves(PlayerColor.RED, new_red, new_blue) 
            if moves is None or (len(moves) > move_check and depth != MAX_DEPTH) or depth == 0:
                return self.utility(PlayerColor.RED, new_red, new_blue, red, blue), None
        else:
            moves = self.possible_moves(PlayerColor.BLUE, new_red, new_blue)
            if moves is None or (len(moves) > move_check and depth != MAX_DEPTH) or depth == 0:
                return self.utility(PlayerColor.BLUE, new_red, new_blue, red, blue), None

        # loop through the possible moves and search till the end of the tree
        move_counts = 0
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
                if value >= beta:
                    # print(f"AB pruned on depth {depth} and move number {move_counts} for {PlayerColor.RED}")
                    break
                alpha = max(alpha, value)
                if move_counts >= MAX_MOVES: break
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
                if value <= alpha:
                    # print(f"AB pruned on depth {depth} and move number {move_counts} for {PlayerColor.BLUE}")
                    break
                beta = min(beta, value)
                if move_counts >= MAX_MOVES: break
        # if (depth <= 2): print(f"Current Depth: {depth} | Possible Moves: {len(moves)} | Move Checked: {move_counts}")
        return value, best_movement
    
    def random_move(self, color, red, blue, move_count):
        # Randomly select 4 adjacent blocks on the board that hasn't been placed yet
        # Check whether the randomly selected blocks have been placed in the game board
        place_action_coords = []

        action_arr = self.place_action_red if color == PlayerColor.RED else self.place_action_blue

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
            for place_action_piece in self.place_action_list:
                for coord in place_action_piece.coords:
                    if Coord(xcoord, ycoord) == coord:
                        coord_already_placed = True
                        break
                if coord_already_placed:
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

                    coord_chosen = False

                    for action in action_arr:
                        for coord in action.coords:
                            if right == coord.r and ycoord == coord.c:
                                place_action_coords.append(Coord(xcoord, ycoord))
                                coord_chosen = True
                                break
                            elif left == coord.r and ycoord == coord.c:
                                place_action_coords.append(Coord(xcoord, ycoord))
                                coord_chosen = True
                                break
                            elif xcoord == coord.r and up == coord.c:
                                place_action_coords.append(Coord(xcoord, ycoord))
                                coord_chosen = True
                                break
                            elif xcoord == coord.r and down == coord.c:
                                place_action_coords.append(Coord(xcoord, ycoord))
                                coord_chosen = True
                                break
                            else:
                                continue
                        if coord_chosen:
                            break

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
