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
    current_red = []
    current_blue = []
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

        total_actions_arr = self.current_red + self.current_blue

        action_arr = self.current_red if self._color == PlayerColor.RED else self.current_blue

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
            for coord in total_actions_arr:
                if Coord(xcoord, ycoord) == coord:
                    coord_already_placed = True
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
            for coord in place_action.coords:
                self.current_red.append(coord)
        else:
            self.place_action_blue.append(action)
            for coord in place_action.coords:
                self.current_blue.append(coord)
        
        self.current_red, self.current_blue = self.eliminate_lines(self.current_red, self.current_blue)
    
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
            