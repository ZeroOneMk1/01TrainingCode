import matplotlib.pyplot as plt
import numpy as np
""" FOR PLOTTING """

x = [0, 1, 2, 2.5, 3, 4]
y = [0, 1, 4, 6.25, 9, 16]
plt.plot(x, y, 'co')  # ro means red circles, so the data will be shown with red circles.
"""
    other colors include:
    b = blue
    g = green
    c = cyan
    m = magenta
    w = white (why would you want this?)
    y = yellow (this one is UGLY!)
"""
plt.axis([0, 6, 0, 20])
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 2))(np.unique(x)), 'g')  # if you want continuous lines you omit the o
"""
    np.unique(x) means it will plot for all unique x values. It looks like a line because it connects the dots,
    not because it calculates all the points in between. IT ALSO sorts the values. :D

    mp.poly1d is a one-dimensional polynomial, 
        here it has np.polyfit as its parameter. 
        polyfit fits param1 and param2 to a param3-degree polynomial and returns the FUNCTION.
        
        After it has the function that polyfit output, that function takes unique(x) as the input, 
        and outputs the outer plot's y-values.
"""
plt.show()  # renders the plot, but deletes previous data (see multiline comment below).\
"""
    as for show(), plotting plots all data and then removes it from the cache. If you only want to add to a plot,
    you have to re-enter the data like this:

        plt.plot(x, y, 'yo')
        plt.axis([0, 6, 0, 20])
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 2))(np.unique(x)), 'g')
        
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 'b')
        
        plt.show()
"""
