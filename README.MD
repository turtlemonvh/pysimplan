# PySimPlan

Currently just a script for running a Monte Carlo analysis of a project plan, using a variation on [the three-point estimation method](http://en.wikipedia.org/wiki/Three-point_estimation).

# How it works

To use this script, first determine a set of scenarios that can occur for each task within a project.  "Most likely", "worst case", and "best case" are popular choices.  Next, you must assign each of these a probability of occuring.
Then you must define you set of tasks.  For every task, you define the amount of time that task will take under each scenario.
This data is used to generate simulations of possible outcomes of the project.

# Input file

The input file takes the following form:

    == Probabilities
    80 10 10

    == Likely, Worst, Best
    a	8	16	2
    b	16	64	8
    c	32	128	16
    d	8	16	4
    e	8	16	2
    f	128	512	32
    g	4	8	2


Under the first `==`, probabilities for each project scenario are listed in units of precentage.  For now it's on you to make sure these add to 100.
    
In this example, we use 3 scenarios for estmation, as shown by the 3 probability categories.  You can use as many or as few scenarios as you want (though less than 2 is pretty useless) as long as the number of probabilty categories equals the number of categories per project task. 

The list of project tasks starts after the second `==`.  The first column of each task row is the name of the task.  The following columns correspond to the time estimated to complete the task in each scenario.

# Basic usage

To run, you must provide the script with an input file and call it with python.

    python estimate_schedule.py example_input.txt

You can also generate histograms simulation outcomes if you have matplotlib and numpy installed.

    python estimate_schedule.py example_input.txt plot.png
    
The image file created looks like the following.  The y-axis is the count, and the x-axis is the time to completion for all the tasks in your project, in whatever units you used in the input file.

![example histogram](https://raw.github.com/turtlemonvh/pysimplan/master/example_out.png "Example Histogram")

# Customizing

You can change the constants in the top of the script to tailor the simulation to your needs.

# License

Coming soon...