from tkinter.constants import ALL, BOTTOM, NE, NW, TOP, TRUE, W, X, Y
from a3_support import *
import tkinter as tk
import random
from PIL import Image, ImageTk
import tkinter.messagebox
#random.seed(10017030)
"""
class Game:

    def generate_entities(self) -> None:
        
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # bomb = False
        # if not blocker:
        #     bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # if bomb:
        #     total_count += 1
        #     entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)
"""

class Entity(object):
    """
    Entity is an abstract class that is used to represent any element that can appear on the game's grid.
    """
    def display(self) -> str:
        """
        Return the character used to represent this entity in a text-based grid. An instance of
        the abstract Entity class should never be placed in the grid, so this method should only be
        implemented by subclasses of Entity. To indicate that this method needs to be implemented
        by subclasses, this method should raise a NotImplementedError.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Return a representation of this entity. This should be inherited by each subclass but should instead display the class name of that subclass rather than always Entity'.
        """
        return 'Entity()'

class Player(Entity):
    """
    A subclass of Entity representing a Player within the game.
    """
    def display(self) -> str:
        """
        Return the character representing a player: 'P'
        """
        return PLAYER

class Destroyable(Entity):
    """
    A subclass of Entity representing a Destroyable within the game. A destroyable can be destroyed by the player but not collected.
    """
    def display(self) -> str:
        """
        Return the character representing a destroyable: 'D'
        """
        return DESTROYABLE

class Collectable(Entity):
    """
    A subclass of Entity representing a Collectable within the game. A collectable can be destroyed or collected by the player.
    """
    def display(self) -> str:
        """
        Return the character representing a collectable: 'C'
        """
        return COLLECTABLE


class Blocker(Entity):
    """
    A subclass of Entity representing a Blocker within the game. A blocker cannot be destroyed or collected by the player.
    """
    def display(self) -> str:
        """
        Return the character representing a blocker: 'B'
        """
        return BLOCKER


class Grid(object):
    """
    The Grid class is used to represent the 2D grid of entities. The top left position of the grid is indicated by (0, 0).
    """
    def __init__(self, size: int) -> None:
        """
        A grid is constructed with a size representing the number of rows (equal to the number of columns) in the grid. Entities should be stored in a dictionary. 
        Initially a grid does not contain any entities.
        """
        self._size = size
        self._position_dictionary = {}

    def get_size(self) -> int:
        """
        Return the size of the grid.
        """
        return self._size

    def add_entity(self, position: Position, entity: Entity) -> None:
        """
        Add a given entity into the grid at a specified position. This entity is only added if the position is valid.
        If an entity already exists at the specified position, this method will replace the current entity at the specified position.
        """
        if entity.display() == Player().display():
            self._position_dictionary[position] = entity
        if self.in_bounds(position):
            self._position_dictionary[position] = entity

    def get_entities(self) -> Dict[Position, Entity]:
        """
        Return the dictionary containing grid entities.
        Updating the returned dictionary should have no side-effects.
        """
        return self._position_dictionary

    def get_entity(self, position: Position) -> Optional[Entity]:
        """
        Return a entity from the grid at a specfic position or None if the position does not have a mapped entity.
        """
        return self._position_dictionary.get(position,None)

    def remove_entity(self, position: Position) -> None:
        """
        Remove an entity from the grid at a specified position.
        """
        del self._position_dictionary[position]

    def serialise(self) -> Dict[Tuple[int, int], str]:
        """
        Convert dictionary of Position and Entities into a simplified, serialised dictionary mapping tuples to characters, and return this serialised mapping.
        Tuples are represented by the x and y coordinates of a Positions and Entities are represented by their `display()` character.
        """
        dict_serial = {}
        position_X_Y = tuple()
        for key in self.get_entities():
            position_X_Y = (key.get_x(),key.get_y())
            dict_serial[position_X_Y] = self.get_entities().get(key).display()

        return dict_serial

    def in_bounds(self, position: Position) -> bool:
        """
        Return a boolean based on whether the position is valid in terms of the dimensions of the grid. Return True iff:
        x >= 0 and x < grid size
        y >= 1 and y < grid size
        """
        return (self._size > position.get_x() >= 0) and (self._size > position.get_y() >= 1) 

    def __repr__(self) -> str:
        """
        Return a representation of this Grid.
        """
        return 'Grid({})'.format(self.get_size())


class Game(object):
    """
    The Game handles the logic for controlling the actions of the entities within the grid.
    """
    def __init__(self, size: int) -> None:
        """
        A game is constructed with a size representing the dimensions of the playing grid. A game should be constructed with at least the following variable:
        Flag representing whether the game is won or lost
        """
        self._grid      = Grid(size)
        self._collected = 0
        self._destroyed = 0
        self._shots     = 0
        self._lost      = 0

    def get_grid(self) -> Grid:
        """
        Return the instance of the grid held by the game.
        """
        return self._grid

    def get_player_position(self) -> Position:
        """
        Return the position of the player in the grid (top row, centre column). This position should be constant.
        """
        return Position(self.get_grid().get_size() // 2, 0)


    def get_num_collected(self) -> int:
        """
        Return the total of Collectables acquired.
        """
        return self._collected

    def get_num_destroyed(self) -> int:
        """
        Return the total of Destroyables removed with a shot.
        """
        return self._destroyed

    def get_total_shots(self) -> int:
        """
        Return the total of shots taken.
        """
        return self._shots

    def rotate_grid(self, direction: str) -> None:
        """
        Rotate the positions of the entities within the grid depending on the direction they are being rotated. 
        Valid directions are specified by the constants found in the a3_support le. Entity positions rotate as seen in Figure 2.
        Left rotation moves all entities by an oset of (-1, 0)
        Right rotation moves all entities by an oset of (1, 0)
        """
        dict_rotated = {}
        left_offset  = ROTATIONS[0]
        right_offset = ROTATIONS[1]
        dict_key     = list(self.get_grid().get_entities().keys())

        if direction == LEFT:
            for key in self.get_grid().get_entities():
                if self.get_grid().get_entities().get(key).display() == Player().display():
                    dict_rotated[key] = self.get_grid().get_entities().get(key)
                    continue
                if key.get_x() == 0:
                    dict_rotated[Position(self.get_grid().get_size() - 1, key.get_y())] = self.get_grid().get_entities().get(key)
                dict_rotated[key.add(Position(left_offset[0], left_offset[1]))] = self.get_grid().get_entities().get(key)
        if direction == RIGHT:
            for key in self.get_grid().get_entities():
                if self.get_grid().get_entities().get(key).display() == Player().display():
                    dict_rotated[key] = self.get_grid().get_entities().get(key)
                    continue
                if key.get_x() == self.get_grid().get_size() - 1:
                    dict_rotated[Position(0, key.get_y())] = self.get_grid().get_entities().get(key)
                dict_rotated[key.add(Position(right_offset[0], right_offset[1]))] = self.get_grid().get_entities().get(key)

        for key in dict_key:
            self.get_grid().remove_entity(key)

        for key in dict_rotated:
            self.get_grid().add_entity(key, dict_rotated.get(key))

    def _create_entity(self, display: str) -> Entity:
        """
        Uses a display character to create an Entity. Raises a NotImplementedError if the character parsed into as the display is not an existing Entity.
        """
        if display == COLLECTABLE:
            return Collectable()
        elif display == DESTROYABLE:
            return Destroyable()
        elif display == BLOCKER:
            return Blocker()

        raise NotImplementedError


    def generate_entities(self) -> None:
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # bomb = False
        # if not blocker:
        #     bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # if bomb:
        #     total_count += 1
        #     entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def step(self) -> None:
        """
        This method moves all entities on the board by an offset of (0, -1). 
        Once entities have been moved, new entities should be added to the grid (using generate_entities). 
        Entities should not be re-added to the grid if they have moved out of bounds.
        """
        step_offset = Position(MOVE[0],MOVE[1])
        
        for y in range(1, self.get_grid().get_size()):
            for x in range(0, self.get_grid().get_size()):
                if y == 1 and self.get_grid().get_entities().__contains__(Position(x, y)):
                    if self.get_grid().get_entities().get(Position(x, y)).display() == DESTROYABLE:
                        self._lost = 1
                if self.get_grid().get_entities().__contains__(Position(x, y).subtract(step_offset)):
                    self.get_grid().get_entities()[Position(x, y)] = self.get_grid().get_entities().get(Position(x, y).subtract(step_offset), None)
                elif self.get_grid().get_entities().__contains__(Position(x, y)):
                    self.get_grid().remove_entity(Position(x, y))

        self.generate_entities()


    def fire(self, shot_type: str) -> None:
        """
        Handles the firing/collecting actions of a player towards an entity within the grid. 
        A shot is fired from the players position and iteratively moves down the grid.
        shot_type refers to whether a collect or destroy shot has been fired (refer to Entity descriptions for how different entities react to being hit by different types). 
        Valid shot_type constants can be found in the a3_support file.
        """
        fire_offset = Position(FIRE[0], FIRE[1])
        target      = self.get_player_position().add(fire_offset)

        self._shots += 1

        while self.get_grid().in_bounds(target):
            if target in self.get_grid().get_entities():
                if shot_type == DESTROY:
                    if self.get_grid().get_entity(target).display() == DESTROYABLE:
                        self.get_grid().remove_entity(target)
                        self._destroyed += 1
                if shot_type == COLLECT:
                    if self.get_grid().get_entity(target).display() == COLLECTABLE:
                        self.get_grid().remove_entity(target)
                        self._collected += 1
                break

            target = target.add(fire_offset)

    def has_won(self) -> bool:
        """
        Return True if the player has won the game.
        """
        return self.get_num_collected() >= COLLECTION_TARGET

    def has_lost(self) -> bool:
        """
        Returns True if the game is lost (a Destroyable has reached the top row).
        """
        return self._lost == 1

class AbstractField(tk.Canvas):
    """
    AbstractField is an abstract view class which inherits from tk.Canvas and provides base functionality for other view classes. 
    An AbstractField can be thought of as a grid with a set number of rows and columns, which supports creation of text at specific positions based on row and column. 
    The number of rows may differ from the number of columns, and the cells may be non-square. You must define the constructor for the AbstractField class as:
    """
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        The parameters rows and cols are the number of rows and columns in the grid, width and height are the width and height of the height of the grid.
        (and hence the width and height of the tk.Canvas,measured in pixels) 
        and **kwargs signies that any additional named arguments supported by tk.Canvas should also be supported by AbstractField.
        """
        super().__init__(master, **kwargs)
        self._master    = master
        self._rows      = rows
        self._cols      = cols
        self._width     = width
        self._height    = height
        self._kwargs    = kwargs

        self._pixel_row = int(self._width // self._rows)
        self._pixel_col = int(self._height // self._cols)

    def get_bbox(self, position):
        """
        Returns the bounding box for the position; 
        this is a tuple containing information about the pixel positions of the edges of the shape, in the form (x_min, y_min, x_max, y_max).
        """
        row, col = position
        x_min = row * self._pixel_row
        x_max = (row + 1) * self._pixel_row
        y_min = col * self._pixel_col
        y_max = (col + 1) * self._pixel_col

        return (x_min, y_min, x_max, y_max)

    def pixel_to_position(self, pixel):
        """
        Converts the (x, y) pixel position (in graphics units) to a (row, column) position.
        """
        x, y = pixel
        return (x // self._pixel_row, y // self._pixel_col)


    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the given (row, column) position.
        """
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        return ((x_min + x_max) // 2, (y_min + y_max) // 2)

    def annotate_position(self, position, text):
        """
        Annotates the center of the cell at the given (row, column) position with the provided text.
        """
        x_center, y_center = self.get_position_center(position)
        label = tk.Label(self._master, text = text, bg='green', font=('Arial', 12), width=2, height=2)
        label.place(X = x_center, Y = y_center)

class GameField(AbstractField):
    """
    GameField is a visual representation of the game grid which inherits from AbstractField. 
    Entities are drawn on the map using coloured rectangles at different (row, column) positions. 
    You must annotate the rectangles of all entities with their display() characters (as per Figure 1). 
    You must use the create_rectangle and create_text methods from tk.Canvas to achieve this. 
    The colours representing each entity are found in a3_support. The FIELD_COLOUR constant indicates the background colour of the view.
    """
    def __init__(self, master, size, width, height, **kwargs):
        """
        The size parameter is the number of rows (= number of columns) in the grid, 
        width and height are the width and height of the grid (in pixels) 
        and **kwargs signifies that any additional named arguments supported by tk.Canvas should also be supported by GameField.
        """
        super().__init__(master, size, size, width, height, **kwargs)
        self._master    = master
        self._size      = size
        self._width     = width
        self._height    = height

        self._size_row = int(self._width // self._size)
        self._size_col = int(self._height // self._size)

        self._cvs = tk.Canvas(self._master, width = self._width, height = self._height, bg = FIELD_COLOUR)
        self._cvs.pack(anchor = NW)

    def draw_grid(self, entities: Dict[Position, Entity]):
        """
        Draws the entities (found in the Grid's entity dictionary) in the game grid at their given position 
        using a coloured rectangle with superimposed text identifying the entity (this includes the Player entity).
        """
        self.draw_player_area()

        for key in entities:
            x_min, y_min, x_max, y_max = self.get_bbox((key.get_x(),key.get_y()))
            text_center = self.get_position_center((key.get_x(),key.get_y()))
            self._cvs.photo = list()
            position_list = []
            for color in COLOURS:
                if entities.get(key).display() == color:
                    self._cvs.create_rectangle(x_min, y_min, x_max, y_max, fill = COLOURS.get(color))
                    self._cvs.create_text(text_center[0], text_center[1], text = entities.get(key).display())
                    one = Image.open('images\{}'.format(IMAGES.get(color)))
                    one = one.resize((self._size_row, self._size_col), Image.ANTIALIAS)
                    one = ImageTk.PhotoImage(one) 
                    self._cvs.photo.append(one)  # to prevent the image garbage collected.
                    position_list.append(text_center)
            for i in range(0, len(self._cvs.photo)):
                self._cvs.create_image((position_list[i][0], position_list[i][1]), image =  self._cvs.photo[i])
        self._cvs.pack(side = "left")
    
    def clear(self):
        """
        clear the grid
        """
        self._cvs.delete(ALL)

    
    def draw_player_area(self):
        """
        Draws the grey area a player is placed on. This colour is found in a3_support file as the PLAYER_AREA constant.
        """
        self._cvs.create_rectangle(0, 0, self._width, self._size_col, fill = PLAYER_AREA)
    
class ScoreBar(AbstractField):
    """
    ScoreBar is a visual representation of shot statistics from the player which inherits from AbstractField.
    For Task 1, this bar displays the number of collectables acquired and the number of destroyables shot as seen in Figure 1. 
    The ScoreBar's statistics values must update in real time. You must define the constructor for the ScoreBar class as:
    """
    def __init__(self, master, rows, game: Game, **kwargs):
        """
        rows is the number of rows contained in the ScoreBar canvas. 
        This should match the size of the grid. By default, columns should be set to 2. 
        Relevant support file constants should be used for window sizing and **kwargs signifies that any additional named arguments supported by tk.Canvas should also be
        supported by ScoreBar. Finally, the background colour of the ScoreBar can be found in a3_support as SCORE_COLOUR.
        """
        super().__init__(master, rows, rows, SCORE_WIDTH, MAP_HEIGHT, **kwargs)
        self._master    = master
        self._rows      = rows
        self._kwargs    = kwargs
        self._game      = game

        self._cvs = tk.Canvas(self._master, width = SCORE_WIDTH, height = MAP_HEIGHT, bg = SCORE_COLOUR)
        self._cvs.pack(anchor = NE)

    def draw_scorebar(self):
        self._cvs.create_text((SCORE_WIDTH //2), (MAP_HEIGHT // self._rows) // 2,text = "Score", font = TITLE_FONT , fill = 'white')
        self._cvs.create_text((SCORE_WIDTH //3), MAP_HEIGHT // self._rows + ((MAP_HEIGHT // self._rows) // 2),text = "Collected:", font = ('Arial', 12) , fill = 'white')
        self._cvs.create_text((SCORE_WIDTH*2 //3), MAP_HEIGHT // self._rows + ((MAP_HEIGHT // self._rows) // 2),text = "{}".format(self.num_collected_destroyed()[0]), font = ('Arial', 12) , fill = 'white')
        self._cvs.create_text((SCORE_WIDTH //3), (MAP_HEIGHT // self._rows) * 2 + ((MAP_HEIGHT // self._rows) // 2),text = "Destroyed:", font = ('Arial', 12) , fill = 'white')
        self._cvs.create_text((SCORE_WIDTH*2 //3), (MAP_HEIGHT // self._rows) * 2 + ((MAP_HEIGHT // self._rows) // 2),text = "{}".format(self.num_collected_destroyed()[1]), font = ('Arial', 12) , fill = 'white')

    def clear(self):
        self._cvs.delete(ALL)

    def num_collected_destroyed(self):
        return (self._game.get_num_collected(), self._game.get_num_destroyed())

class State_scenario(AbstractField):
    """
    For total_shots, timer, pause button
    """
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, GRID_SIZE, GRID_SIZE, width, height, **kwargs)

        self._cvs = tk.Canvas(self._master, width = width, height = height)
        self._cvs.pack(side = tk.BOTTOM, fill = X)

    def draw_shots_stats(self, game: Game):
        """
        Show the total shots
        """
        self._cvs.create_text((SCORE_WIDTH //2), self._height // 6, text = "Total Shots", font = ('Arial', 12) )
        self._cvs.create_text((SCORE_WIDTH //2), self._height  // 3 + 10, text = "{}".format(game.get_total_shots()), font = ('Arial', 12) )

    def shots_stats_clear(self):
        """
        clear total shots scenario
        """
        self._cvs.delete(ALL)


class HackerController(object):
    """
    HackerController acts as the controller for the Hacker game. The constructor should be defined
    """
    def __init__(self, master, size):
        """
        The parameter master represents the master window and size represents the number of rows (= number of columns) in the game map. 
        Thismethod should draw the title label (see a3_support for font, colour and size details), initialise the Game model, 
        and instantiate and pack the GameField and ScoreBar. Finally, this method should initiate the game's `step'
        """
        self._master = master
        self._size   = size
        self._master.geometry('{}x{}'.format(MAP_WIDTH + SCORE_WIDTH,MAP_WIDTH + BAR_HEIGHT + 10))
        lbl = tk.Label(self._master, text = TITLE, bg = TITLE_BG, font = TITLE_FONT, fg = 'white')
        lbl.pack(side=tk.TOP, fill = X)

        self._game        = Game(self._size)
        self._shots        = State_scenario(self._master, SCORE_WIDTH, MAP_HEIGHT*2 // GRID_SIZE)
        self._gamefield   = GameField(self._master, self._size, MAP_WIDTH, MAP_WIDTH)
        self._scorebar    = ScoreBar(self._master, self._size, self._game)

        self._game.get_grid().add_entity(self._game.get_player_position(), Player())
        self._gamefield.draw_grid(self._game.get_grid().get_entities())
        self._scorebar.draw_scorebar()
        self._shots.draw_shots_stats(self._game)
        self._master.focus_set()
        self._master.bind("<Key>", self.handle_keypress)
        self._master.after(2000, self.step)
        
        
    def handle_keypress(self, event):
        """
        This method should be called when the user presses any key during the game. 
        It must handle error checking and event calling and execute methods to update both the model and the view accordingly.
        """
        if event.char.upper() in DIRECTIONS:
            self.handle_rotate(event.char.upper())
        elif event.keycode in (32,13):
            print(event.keycode)
            if event.keycode == 32:
                event_type = DESTROY
            elif event.keycode == 13:
                event_type = COLLECT
            self.handle_fire(event_type)
        else:
            print("Invalid input:",event.keycode)

    def draw(self):
        """
        Clears and redraws the view based on the current game state.
        """
        self._gamefield.clear()
        self._scorebar.clear()
        self._shots.shots_stats_clear()
        
        self._shots.draw_shots_stats(self._game)
        self._gamefield.draw_grid(self._game.get_grid().get_entities())
        self._scorebar.draw_scorebar()


    def handle_rotate(self, direction):
        """
        Handles rotation of the entities and redrawing the game. 
        It may be easiest for the handle_keypress method to call handle_rotate with the relevant arguments.
        """
        self._game.rotate_grid(direction)
        self.draw()
        

    def handle_fire(self, shot_type):
        """
        Handles the firing of the specified shot type and redrawing of the game. 
        It may be easiest for the handle_keypress method to call handle_fire with the relevant arguments.
        """
        self._game.fire(shot_type)
        self.draw()

    def step(self):
        """
        The step method is called every 2 seconds. This method triggers the step method for the game and updates the view accordingly. 
        Note: The .after method for tkinter widgets may be useful when trying to get this method to run every 2 seconds.
        """
        self._game.step()
        self.draw()
        if self._game.has_won():
            tk.messagebox.showinfo("Game Over", "You win!")
        if self._game.has_lost():
            tk.messagebox.showinfo("Game Over", "You lost!")

        self._master.after(2000, self.step)

class AdvancedHackerController(HackerController):

    def __init__(self, master, size):
        super().__init__(master, size)
        self._game_saved = Game

        """File Menu"""
        menubar = tk.Menu(self._master)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="New game", command = self.start_new_game)
        filemenu.add_command(label="Save game", command = self.same_game)
        filemenu.add_command(label="Load game", command = self.load_game)
        filemenu.add_command(label="Quit", command = self.quit_game)
        menubar.add_cascade(label="File Menu", menu=filemenu)
        self._master.config(menu=menubar)

        self._cvs = tk.Canvas(self._master, width = SCORE_WIDTH, height = MAP_HEIGHT*2 // GRID_SIZE, bg = SCORE_COLOUR)
        self._cvs.pack(side = tk.BOTTOM, fill = X)


    def start_new_game(self):
        """
        Start a new Hacker game
        """
        position_list = list(self._game.get_grid().get_entities().keys())
        for key in position_list:
            self._game.get_grid().remove_entity(key)
        self._game.get_grid().add_entity(self._game.get_player_position(), Player())
        self.draw()
        
    def same_game(self):
        """
        Prompt the user for the location to save their le (using an appropriate method of your choosing) 
        and save all necessary information to replicate the current state of the game.
        """
        self._game_saved = self._game
        print(self._game_saved)
        print(self._game_saved.get_num_destroyed())

    def load_game(self):
        """
        Prompt the user for the location of the le to load a game from and load the game described in thatfile.
        """
        self._game = self._game_saved
        print(self._game)
        print(self._game_saved.get_num_destroyed())
        self.draw()

    def quit_game(self):
        """
        Prompt the player via a messagebox to ask whether they are sure they would like to quit. 
        If no, do nothing. If yes, quit the game (window should close and program should terminate).
        """
        quit_btn = tk.messagebox.askyesno("Quit", "do you want to quit the game?")
        if quit_btn:
            self._master.destroy()

def start_game(root, TASK=TASK):
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app


def main():
    root = tk.Tk()
    root.title(TITLE)
    app = start_game(root)
    root.mainloop()


if __name__ == '__main__':
    main()
