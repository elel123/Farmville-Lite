from my_module.classes import Plot, SeedPanel
import pygame 

def farmville_lite():
    """
    This function puts together the entirety of my game. 
    It creates the game display and starts the game thread and kills it
      when the user decides to quit.
    There are no parameters needed aside from the imports.
    """
    
    #initializes some elements of pygame
    pygame.init() 
    pygame.font.init()

    #Sets up some constants to be used throughout the program
    screen_width = 800
    screen_height = 600
    grass_image = pygame.image.load('images/grass.jpg')

    #Sets up the game display and in-game clock
    gameDisplay = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("FarmVille Lite")
    clock = pygame.time.Clock()

    #Sets up the conditions for the game loop
    gameRunning = True
    plots = []
    panel = SeedPanel(gameDisplay)

    #This loop constantly runs to keep the game running 
    #  (until the player exits the window)
    while gameRunning:

        #Draws the background and game panel everytime the loop iterates
        gameDisplay.blit(grass_image, (0,0))
        panel.draw_panel()

        #This loop gets every event (mouse, keyboard, etc) that occurs in the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False

            #Adding functionality to the mouse_click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() #returns a tuple (x,y) 

                #Creating a plot, but first must check if possible overlap occurs
                collide = False
                for plot in plots: #Check if overlap with other plots
                    if plot.overlap(mouse_pos[0], mouse_pos[1]):
                        collide = True

                #Check if overlap with the panel
                if panel.overlap(mouse_pos[0], mouse_pos[1], 100, 100):
                    collide = True

                #Check if plot is out of the screen
                if mouse_pos[0] > screen_width - 50 or mouse_pos[0] < 50 or \
                   mouse_pos[1] > screen_height - 50 or mouse_pos[1] < 50:
                    collide = True


                #Checking if in-game buttons were clicked
                panel.select(mouse_pos[0], mouse_pos[1])

                #Checking selections made by the user from the panel 
                #  and performs the respective actions
                if panel.selected == "shovel": #removes plots
                    for plot in plots:
                        if plot.contains(mouse_pos[0], mouse_pos[1]):
                            #plot still exists but is permanently disabled
                            plot.remove_plot() 
                            
                elif panel.selected == "rake": #adds plots
                    if collide == False: #If no overlap occurs
                        plots.append( Plot(mouse_pos[0], mouse_pos[1], gameDisplay) )
                        
                elif panel.selected == "wheat":
                    for plot in plots: 
                        if plot.contains(mouse_pos[0], mouse_pos[1]):
                            plot.plant('wheat')
                            
                elif panel.selected == "tree":
                    for plot in plots:
                        if plot.contains(mouse_pos[0], mouse_pos[1]):
                            plot.plant('tree')
                            
                elif panel.selected == "harvest":
                    for plot in plots:
                        if plot.contains(mouse_pos[0], mouse_pos[1]):
                            panel.add_money( plot.harvest() )

        #Update the game panel for any changes made
        panel.update_panel()
        
        #Updates the score in the game
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        money_text = my_font.render("Coins: " + str(panel.money), False, (0, 0, 0))
        gameDisplay.blit(money_text, (4, 460))


        #Update and draw the plots on the screen 
        for plot in plots:
            plot.draw_plot()

        #Update the game
        clock.tick(60)
        pygame.display.flip()
        
    #When the player decides to quit, end all threads
    pygame.display.quit()
    pygame.font.quit()
    pygame.quit()