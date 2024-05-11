# Random Agent

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
    move_count = 0

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
            coord_already_placed = False
            coord_not_adjecent = False
            # Randomly select a coord
            xcoord = random.randint(0, 10)
            ycoord = random.randint(0, 10)
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
            if len(place_action_coords) == 0 and self.move_count == 0:
                if Coord(xcoord, ycoord) not in place_action_coords:
                    place_action_coords.append(Coord(xcoord, ycoord))
            # If this is not the first move of the game and no coord has been chosen
            # then check if the coord is adjacent to any of the coords that has been
            # chosen before by the player. If it is, add the coord to the place_action_coords list
            elif len(place_action_coords) == 0 and self.move_count != 0:
                if Coord(xcoord, ycoord) not in place_action_coords:
                    right = xcoord + 1
                    if right == 11: right = 0
                    left = xcoord - 1
                    if left == -1: left = 10
                    up = ycoord + 1
                    if up == 11: up = 0
                    down = ycoord - 1
                    if down == -1: down = 10

                    action_arr = self.place_action_red if self._color == PlayerColor.RED else self.place_action_blue

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
                                coord_not_adjecent = True
                                break
                        if coord_not_adjecent or coord_chosen:
                            break
                    if coord_not_adjecent:
                        continue
            # If this is not the first move of the game and some coords have been chosen
            # then check if the coord is adjacent to any of the coords that has been
            # chosen in the place_action_coords list. If it is, add the coord to the place_action_coords list
            else:
                if Coord(xcoord, ycoord) not in place_action_coords:
                    right = xcoord + 1
                    if right == 11: right = 0
                    left = xcoord - 1
                    if left == -1: left = 10
                    up = ycoord + 1
                    if up == 11: up = 0
                    down = ycoord - 1
                    if down == -1: down = 10

                    if right == place_action_coords[0].r and ycoord == place_action_coords[0].c:
                        place_action_coords.append(Coord(xcoord, ycoord))
                    elif left == place_action_coords[0].r and ycoord == place_action_coords[0].c:
                        place_action_coords.append(Coord(xcoord, ycoord))
                    elif xcoord == place_action_coords[0].r and up == place_action_coords[0].c:
                        place_action_coords.append(Coord(xcoord, ycoord))
                    elif xcoord == place_action_coords[0].r and down == place_action_coords[0].c:
                        place_action_coords.append(Coord(xcoord, ycoord))
                    else:
                        continue
        
        self.move_count += 1

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
        