"""
This module contains the classes for Plot and SeedPanel

"""

import pygame


#Constants
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
grass_green = [51, 181, 90]
blue = [0, 0, 255]
soil_color = [131, 102, 58]
panel_color = [209, 158, 82]
button_color = [165, 121, 54]
selected_color = [249, 235, 112]

#Importing images from the images folder
shovel_image = pygame.image.load('images/shovel.png')
rake_image = pygame.image.load('images/rake.png')
scythe_image = pygame.image.load('images/scythe.png')
squiggly_image = pygame.image.load('images/squiggly_line.png')
wheat_image = pygame.image.load('images/wheat.png')
baby_wheat_image = pygame.image.load('images/baby_wheat.png')
wheat_icon_image = pygame.image.load('images/wheat_icon.png')
sapling_image = pygame.image.load('images/sapling.png')
baby_sapling_image = pygame.image.load('images/baby_sapling.png')
sapling_icon_image = pygame.image.load('images/sapling_icon.png')


class Plot():
    """
    This class is for the plots. 
    They require the functionality to appear and disappear, and hold plants.
    
    """
    
    #Plot attributes
    plot_height = 100
    plot_width = 100
    has_plant = False
    can_harvest = False
    plant_type = None
    time_planted = 0
    age = 0
    
    #Keeps track of whether the plot is still visible on the screen
    plotted = True
        
    
    def __init__(self, plot_x, plot_y, screen):
        
        #Adjusting the x and y position of the plot to create a plot at the 
        #  center of themouse click
        self.plot_x = plot_x - (self.plot_width / 2)
        self.plot_y = plot_y - (self.plot_height / 2)
        
        #Save the pygame screen for use within the class instances
        self.screen = screen
        
        #Create the rectangle for the plot
        self.plot_rect = pygame.Rect(self.plot_x, self.plot_y, self.plot_height, self.plot_width)
        
    def draw_plot(self):
        """Draws the plot on the pygame screen. 
           Also draws the plant if the plot is currently holding a plant.
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        """
        
        if self.plotted: #self.plotted serves as a switch for whether the plot is drawn or not
            
            #Draws the plot on the screen and the squiggly lines to indicate it being plowed
            pygame.draw.rect(self.screen, soil_color, self.plot_rect)
            self.screen.blit(squiggly_image, (self.plot_x, self.plot_y - 35))
            self.screen.blit(squiggly_image, (self.plot_x, self.plot_y + 40))
            
            if self.plant_type == 'wheat':
                
                #Draws the wheat on the plot
                if self.age < 1:
                    #Draws the young wheat
                    self.screen.blit(baby_wheat_image, (self.plot_x - 10, self.plot_y - 40))
                    self.can_harvest = False
                    
                else: 
                    #Draws the mature wheat
                    self.screen.blit(wheat_image, (self.plot_x - 10, self.plot_y - 10))
                    self.can_harvest = True
                    
            elif self.plant_type == 'tree':
                
                #Draws the tree on the plot
                if self.age < 2:
                    #Draws the young tree
                    self.screen.blit(baby_sapling_image, (self.plot_x + 28, self.plot_y + 20))
                    self.can_harvest = False
                    self.screen.blit(squiggly_image, (self.plot_x + 5, self.plot_y - 20))
                    self.screen.blit(squiggly_image, (self.plot_x + 5, self.plot_y + 20))
                    
                else:
                    #Draws the mature tree
                    self.screen.blit(sapling_image, (self.plot_x - 22, self.plot_y - 22))
                    self.can_harvest = True
                
            else:           
                #if nothing is planted, draw the remaining squiggly lines
                self.screen.blit(squiggly_image, (self.plot_x + 5, self.plot_y - 20))
                self.screen.blit(squiggly_image, (self.plot_x, self.plot_y))
                self.screen.blit(squiggly_image, (self.plot_x + 5, self.plot_y + 20))
            
            self.grow() #grows the plant by updating the age
    
    
    def plant(self, plant_type):
        """Assigns a plant (wheat or tree) to this plot
           Starts the timer to keep track of the growth of the plant
        
        Parameters
        ----------
        plant_type: string
            The string to be assigned to self.plant_type
        
        
        Returns
        -------
        None
        
        """
        
        if self.plotted: #Controlled by the switch
            
            if self.has_plant == False:
                
                if plant_type == 'wheat' or plant_type == 'tree':
                    #Update the corresponding variables
                    self.plant_type = plant_type    
                    self.has_plant = True
                    self.time_planted = pygame.time.get_ticks()
                    
    def grow(self):
        """Updates self.age to indicate plant growth
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        """
        if self.plotted: #Controlled by switch
            #Every 10000 milliseconds is one unit of age
            self.age = (pygame.time.get_ticks() - self.time_planted) // 10000 
        
            
    
    def overlap(self, xpos, ypos):
        """Checks if the a new plot of position xpos and ypos will overlap with this plot
        
        Parameters
        ----------
        xpos : integer
            the x position of the new plot
            
        ypos : integer 
            the y position of the new plot
            
            
        Returns
        -------
        boolean
            True - if new plot overlaps with this plot
            False - otherwise
        
        """
        
        if self.plotted == False: #Controlled by the switch
            return False
        
        elif xpos > self.plot_x - (self.plot_width/2) - 5 and xpos < self.plot_x + \
             (3*self.plot_width/2) + 5 and ypos > self.plot_y - (self.plot_height/2) - 5 and \
             ypos < self.plot_y + (3*self.plot_height/2) + 5: 
                return True
            
        else:
            #If the new plot does not overlap
            return False
        
    def contains(self, xpos, ypos):
        """Checks if the x and y positions provided as contained within this plot
        
        Parameters
        ----------
        xpos : integer  
            the x position 
        
        ypos : integer
            the y position
            
            
        Returns
        -------
        boolean
            True - if (xPos, yPos) is contained in the plot
            False - otherwise
        
        """
        if self.plotted == False:
            return False
        elif xpos > self.plot_x and xpos < self.plot_x + self.plot_width:
            if ypos > self.plot_y and ypos < self.plot_y + self.plot_height:
                return True
        else:
            return False
        
    def harvest(self):
        """Harvests the plant by updating the plot status so that its now empty.
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        earnings : int
            the money that the player gets from harvesting the plant
        
        """
        
        earnings = 0
        
        if self.has_plant and self.can_harvest:
            
            if self.plant_type == 'tree':
                #If the plant harvested was a tree
                earnings = 3
                
            else:
                #If the plant harvested was wheat
                earnings = 1
            
            #Update the plot by removing the plant
            self.remove_plot()
            
        return earnings
        

        
    def remove_plot(self):
        """Updates the plot by removing the plant if it's not empty, or the plot
           itself if the plot is empty.
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        """
        
        if self.has_plant: 
            #Updates the variables to show that the plot is empty
            self.plant_type = None
            self.has_plant = False
            self.age = 0
            self.time_planted = 0
            self.can_harvest = False
            
        else:
            #Once the plot itself is removed, the switch turns off and the plot is disabled
            self.plotted = False 
        


class SeedPanel():
    """
    This class is for the game panel on the left side of the game screen. 
    They require the functionality to allow for interaction and selection.
    
    """   
    
    #Class attributes 
    selected = None
    height = 500
    width = 100
    button1_color = button_color
    button2_color = button_color
    button3_color = button_color
    button4_color = button_color
    button5_color = button_color
    money = 0
    
    
    def __init__(self, screen):
        
        #Saves the pygame display screen to be used in the class later
        self.screen = screen
        
        #Creates the rectangles for the game panel
        self.panel_rect = pygame.Rect(0, 0, self.width, self.height)
        self.button1 = pygame.Rect(10, 10, 80, 80)
        self.button2 = pygame.Rect(10, 100, 80, 80)
        self.button3 = pygame.Rect(10, 190, 80, 80)
        self.button4 = pygame.Rect(10, 280, 80, 80)
        self.button5 = pygame.Rect(10, 370, 80, 80)
        
    def select(self, xpos, ypos):
        """If the provided x and y positions (for the mouse click) is within
           one of the buttons, update the panel to reflect the button press by
           updating the button colors and the variable self.selected
        
        Parameters
        ----------
        xpos : integer
            the x position (of the mouse)
         
        ypos : integer
            the y position (of the mouse)
           
           
        Returns
        -------
        None
        
        """        
        
        if self.button1.collidepoint(xpos, ypos):
            self.button1_color = selected_color
            self.button2_color = button_color
            self.button3_color = button_color
            self.button4_color = button_color
            self.button5_color = button_color
            self.selected = "tree"
            
        elif self.button2.collidepoint(xpos, ypos):
            self.button1_color = button_color
            self.button2_color = selected_color
            self.button3_color = button_color
            self.button4_color = button_color
            self.button5_color = button_color
            self.selected = "wheat"
            
        elif self.button3.collidepoint(xpos, ypos):
            self.button1_color = button_color
            self.button2_color = button_color
            self.button3_color = selected_color
            self.button4_color = button_color
            self.button5_color = button_color
            self.selected = "rake"
            
        elif self.button4.collidepoint(xpos, ypos):
            self.button1_color = button_color
            self.button2_color = button_color
            self.button3_color = button_color
            self.button4_color = selected_color
            self.button5_color = button_color
            self.selected = "shovel"
            
        elif self.button5.collidepoint(xpos, ypos):
            self.button1_color = button_color
            self.button2_color = button_color
            self.button3_color = button_color
            self.button4_color = button_color
            self.button5_color = selected_color
            self.selected = "harvest"
            
            
    def add_money(self, money):
        """Updates the self.money variable by adding the parameter value to it
        
        Parameters
        ----------
        money : integer
            the money to be added
            
        Returns
        -------
        None
        
        """
        
        self.money += money
        
    def overlap(self, xpos, ypos, plot_width, plot_height):
        """Checks if the a new plot of position xpos and ypos will overlap 
           with the game panel
        
        Parameters
        ----------
        xpos : integer
            the x position of the new plot
            
        ypos : integer
            the y position of the new plot
            
            
        Returns
        -------
        boolean
            True - if new plot overlaps with this panel
            False - otherwise
        
        """
        
        if xpos < self.width + (plot_width/2) + 5 : 
            if ypos < self.height + (plot_height/2) + 5:
                return True
        else:
            return False
    
    def draw_panel(self):
        """Draws the game panel with all its updates from interactions
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        """
        pygame.draw.rect(self.screen, panel_color, self.panel_rect)
        pygame.draw.rect(self.screen, self.button1_color, self.button1)
        pygame.draw.rect(self.screen, self.button2_color, self.button2)
        pygame.draw.rect(self.screen, self.button3_color, self.button3)
        pygame.draw.rect(self.screen, self.button4_color, self.button4)
        pygame.draw.rect(self.screen, self.button5_color, self.button5)
        self.screen.blit(shovel_image, (15, 285))
        self.screen.blit(rake_image, (15, 195))
        self.screen.blit(scythe_image, (15, 375))
        self.screen.blit(wheat_icon_image, (10, 100))
        self.screen.blit(sapling_icon_image, (12, 7))
        
    def update_panel(self):
        """Updates the game panel with all its updates from interactions
        
        Parameters
        ----------
        None
        
        
        Returns
        -------
        None
        
        """       
        self.draw_panel()
        