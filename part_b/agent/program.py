# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

import random
from referee.game import PlayerColor, Action, PlaceAction, Coord


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
                if self.player_move_count < 12:
                    place_action_coords = self.random_move(PlayerColor.RED, self.current_red,
                                                           self.current_blue, self.player_move_count)
                    self.player_move_count+=1
                    return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
                place_action_coords = self.minimax(True, self.current_red, self.current_blue)[1]
                return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                if self.player_move_count < 12:
                    place_action_coords = self.random_move(PlayerColor.BLUE, self.current_red,
                                                           self.current_blue, self.player_move_count)
                    self.player_move_count+=1
                    return PlaceAction(
                        place_action_coords[0], 
                        place_action_coords[1], 
                        place_action_coords[2], 
                        place_action_coords[3]
                    )
                place_action_coords = self.minimax(False, self.current_red, self.current_blue)[1]
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

        self.current_red, self.current_blue = self.eliminate_lines(self.current_red, self.current_blue)

        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

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
    def utility(self, color: PlayerColor, red, blue):
        if self.possible_moves(color, red, blue) == None: 
        # no possible move for red -> blue win, score = -1
            if color == PlayerColor.RED:
                return -1
        # no possible move for blue -> red win, score = 1
            else:
                return 1
        else:
            return 0
    
    # return an action based on the utility of given moves by using the minimax strategy
    # can implement ab pruning in this function
    def minimax(self, maximizing, red, blue, alpha=float('-inf'), beta=float('inf')):
        # generate possible moves for given state (red and blue)
        # if no possible move, return the utility
        if maximizing:
            moves = self.possible_moves(PlayerColor.RED, red, blue)            
            if moves is None:
                return self.utility(PlayerColor.RED, red, blue), None
        else:
            moves = self.possible_moves(PlayerColor.BLUE, red, blue)
            if moves is None:
                return self.utility(PlayerColor.BLUE, red, blue), None

        # loop through the possible moves and search till the end of the tree
        if maximizing:
            value = float('-inf')
            best_movement = None
            for move in moves:
                # eliminate lines if there are filled lines
                # new_red, new_blue = self.eliminate_lines(red[:]+move, blue)
                score = self.minimax(False, red[:]+move, blue)[0]
                if score > value:
                    value = score
                    best_movement = move
                if value >= beta:
                    break
                alpha = max(alpha, value)
        else:
            value = float('inf')
            best_movement = None
            for move in moves:
                # eliminate lines if there are filled lines
                # new_red, new_blue = self.eliminate_lines(red, blue[:]+move)
                score = self.minimax(True, red, blue[:]+move)[0]
                if score < value:
                    value = score
                    best_movement = move
                if value <= alpha:
                    break
                beta = min(beta, value)
        
        return value, best_movement
    
    def random_move(self, color, red, blue, move_count):
        # Randomly select 4 adjacent blocks on the board that hasn't been placed yet
        # Check whether the randomly selected blocks have been placed in the game board
        place_action_coords = []
        if move_count == 0:
            while len(place_action_coords) < 4:
                xcoord = random.randint(0, 10)
                ycoord = random.randint(0, 10)
                for place_action_piece in self.place_action_list:
                    for coord in place_action_piece.coords:
                        if Coord(xcoord, ycoord) == coord:
                            continue
                if len(place_action_coords) == 0:
                    if Coord(xcoord, ycoord) not in place_action_coords:
                        place_action_coords.append(Coord(xcoord, ycoord))
                else:
                    if Coord(xcoord, ycoord) not in place_action_coords:
                        if xcoord + 1 == place_action_coords[0].r and ycoord == place_action_coords[0].c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif xcoord - 1 == place_action_coords[0].r and ycoord == place_action_coords[0].c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif xcoord == place_action_coords[0].r and ycoord + 1 == place_action_coords[0].c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        elif xcoord == place_action_coords[0].r and ycoord - 1 == place_action_coords[0].c:
                            place_action_coords.append(Coord(xcoord, ycoord))
                        else:
                            continue
        else:
            place_action_coords = random.choice(self.possible_moves(color, red, blue))
        return place_action_coords


    def eliminate_lines(self, red, blue):
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

        return red_clone, blue_clone
    
    """
    def eliminate_lines(self,red, blue):
        # check if there are any completed rows. If there are, remove the non-expandable blocks that are part of the completed row
        red = red[:]
        blue = blue[:]
        block = red + blue

        for i in range(11):
            row = []
            for j in range(11):
                row.append(Coord(i, j))
            if set(row).issubset(set(block)):
                for coord in row:
                    if coord in red: red.remove(coord)
                    if coord in blue: blue.remove(coord)
                    block.remove(coord)
        # check if there are any completed columns. If there are, remove the non-expandable blocks
        # that are part of the completed column
        for i in range(11):
            column = []
            for j in range(11):
                column.append(Coord(j, i))
            if set(column).issubset(set(block)):
                for coord in column:
                    if coord in red: red.remove(coord)
                    if coord in blue: blue.remove(coord)
                    block.remove(coord)
            
        return red, blue
    """