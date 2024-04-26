# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    # Class attribute that stores all the place actions that has been played by both agents
    place_action_list = []
<<<<<<< Updated upstream
=======
    place_action_red = []
    place_action_blue = []
    red_move_count = 0
    blue_move_count = 0
>>>>>>> Stashed changes

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
                if self.red_move_count == 0:
                    # random_move()
                    return PlaceAction(
                        Coord(3, 3), 
                        Coord(3, 4), 
                        Coord(4, 3), 
                        Coord(4, 4)
                    )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                if self.blue_move_count == 0:
                    # random_move()
                    return PlaceAction(
                        Coord(2, 3), 
                        Coord(2, 4), 
                        Coord(2, 5), 
                        Coord(2, 6)
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

        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")
        print('\n')
        print(self.place_action_list)
        print('\n')

    # generate a list of possible moves and number of moves given the current state
    def possible_moves(color: PlayerColor, red, blue, goal_check):
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
            # return true if performing goal check
            if goal_check: return True
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
                        # return false when it is checking if the terminal state is reached
                        if (goal_check & len(clone) == 4): return False
                        # if not checking terminal state, proceed to append actions
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
                        if (goal_check & len(clone) == 4): return False
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
                        if (goal_check & len(clone) == 4): return False
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
                        if (goal_check & len(clone) == 4): return False
                        actions.append(clone)
        if (goal_check & len(actions) == 0): return True
        return actions

    # calculate utility of a possible move
    def utility(self, color: PlayerColor, red, blue):
        # no possible move for red -> blue win, score = -1
        if color == PlayerColor.RED:
            if self.possible_moves(color, red, blue, True): return -1
        # no possible move for blue -> red win, score = 1
        elif color == PlayerColor.BLUE:
            if self.possible_moves(PlayerColor.BLUE, red, blue, True): return 1
        else:
            return 0
    
    # return an action based on the utility of given moves by using the minimax strategy
    # can implement ab pruning in this function
    def minimax(self, color: PlayerColor, red, blue):
        # generate possible moves for given state (red and blue)
        moves =  self.possible_moves(color, red, blue, False)
        # if no possible move, return the utility and the move
        if moves is None: return [self.utility(self, color, red, blue), None]

        # loop through the possible moves and search till the end of the tree
        for move in moves:
            if color == PlayerColor.RED:
                score, action = self.minimax(self, color, red[:].append(move), blue)
            if color == PlayerColor.BLUE:
                score, action = self.minimax(self, color, red, blue[:].append(move))


        return action
    
    def random_move():
        return None
    
    

