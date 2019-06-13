"""Test for my functions.

Note: Keep this file in the same directory as its in now, or the test functions will not be able to find the 
        image files and modules that are located in the my_module directory. 
"""


from my_module.classes import Plot, SeedPanel
import pygame

##
##


def test_Plot():
    pygame.init()
    plot = Plot(200, 200, pygame.display.set_mode( (600,800) ))
    
    #Testing the plant() and remove_plant() functions
    plot.plant('wheat')
    assert plot.has_plant == True
    assert plot.plant_type == 'wheat'
    
    plot.remove_plot()
    assert plot.has_plant == False
    assert plot.plant_type == None
    
    plot.plant('some other plant')
    assert plot.has_plant == False
    
    #Testing contains() and overlap() functions
    assert plot.contains(160, 160) == True
    assert plot.contains(10, 10) == False
    assert plot.overlap(250, 150) == True
    assert plot.overlap(1250, 1150) == False
        
    pygame.display.quit()
    pygame.quit()
    

def test_SeedPanel():
    pygame.init()
    panel = SeedPanel(pygame.display.set_mode( (600,800) ))
    
    #Testing the select() function
    panel.select(50, 50)    
    assert panel.selected == 'tree'
    
    panel.select(50, 300) 
    assert panel.selected == 'shovel'
    
    panel.select(500, 300)
    assert panel.selected == 'shovel'
    
    #Testing the overlap() function
    assert panel.overlap(200, 200, 500, 500) == True
    assert panel.overlap(200, 200, 10, 10) == False

    pygame.display.quit()
    pygame.quit()
