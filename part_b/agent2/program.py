# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent
import random
from referee.game import PlayerColor, Action, PlaceAction, Coord

# Agent2 places actions by randomly selecting 4 adjecent blocks on the board that hasn't been placed yet

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    # Class attribute that stores all the place actions that has been played by both agents
    place_action_list = []
    place_action_red = []
    place_action_blue = []

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

        # Randomly select 4 adjacent blocks on the board that hasn't been placed yet
        # Check whether the randomly selected blocks have been placed in the game board
        place_action_coords = []
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

        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                return PlaceAction(
                    place_action_coords[0], 
                    place_action_coords[1], 
                    place_action_coords[2], 
                    place_action_coords[3]
                )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
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
        else:
            self.place_action_blue.append(action)


        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")
        print('\n')
        print("agent 2 place action list: " + str(self.place_action_list))
        print('\n')
        print("agent 2 red place action list: " + str(self.place_action_red))
        print('\n')
        print("agent 2 blue place action list: " + str(self.place_action_blue))
        

    # generate a list of possible moves and number of moves given the current state
    def possible_moves(color: PlayerColor, red, blue):
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
        if len(actions) == 0: return None
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
                    if not duplicate: actions.append(clone)
                if (block.down(1) not in not_expandable_block and block.down(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.down(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate: actions.append(clone)
                if (block.left(1) not in not_expandable_block and block.left(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.left(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate: actions.append(clone)
                if (block.right(1) not in not_expandable_block and block.right(1) not in list(possible_move)):
                    clone = list(possible_move)[:]
                    clone.append(block.right(1))
                    duplicate = False
                    for item in actions:
                        if set(item) == set(clone):
                            duplicate = True
                            break
                    if not duplicate: actions.append(clone)
        return actions, len(actions)

    # calculate utility of a possible move
    def utility(color: PlayerColor, action, red, blue):
        score = 1 + 1
        return score
    
    # return an action based on the utility of given moves by using the minimax strategy
    # can implement ab pruning in this function
    def minimax():
        return None