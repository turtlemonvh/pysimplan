"""
Python script to analyze probability of project completion time

Timothy Van Heest
07-26-2013
"""

import sys
import os
import re
import random

NUM_SCENARIOS = 1000 # Number of scenarios to find
NBINS = 25 # Number of bins to use for histogram
#PROB_MULT = 0.001 # Uncomment this line to provide an explicit acceptance probability

def mc_scenarios(est, prob):
  """Accept a list of estimate and a list of probabilities and calculate
  a set of scenarios """
  
  # Check dimensions
  if len(est[0]) != len(prob):
    print "ERROR: Dimension mismatch between probabilities and estimates"
    print "ERROR: > You have %s estimates per item and %s probabilities" % (len(est[0]), len(prob))
    print "ERROR: > These values must be equal for this script to work."
    sys.exit()
  
  # Calculate a reasonable default acceptance probability
  PROB_MULT = (PROB_MULT if 'PROB_MULT' in locals() else
                reduce(lambda x,y: x*0.2, range(len(est)), 1))
  
  # Run the simulation
  scenarios = []
  nscenarios = 0
  niter = 0
  while(nscenarios <= NUM_SCENARIOS):
    niter += 1
    
    # Generate choice
    choices = [random.randrange(0,3) for i in est]
    
    # Get total time and total prob for this choice
    if calc_choice_prob(choices, prob) > random.random()*PROB_MULT:
      scenarios.append(calc_choice_time(choices, est))
      nscenarios += 1
  
  return (niter, scenarios)

def calc_choice_prob(choice, prob):
  """ Given a choice and a array of probabilities, return the probability for that choice """
  return reduce(lambda x,c: x*prob[c]/100.0, choice, 1.0)

def calc_choice_time(choice, est):
  """Given a choice and list of estimates, return the estimated time for that choice """
  return sum(est[i][c] for i, c in enumerate(choice))
  
def plot_histogram(values, file_name):
  """Create a histogram plot using NBINS bins for the data """
  import numpy as np
  import matplotlib.pyplot as plt
  
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.hist(values, NBINS)
  plt.savefig(file_name)

if __name__ == "__main__":
  """Main script """
  try:
    file_name = sys.argv[1]
  except IndexError:
    print "ERROR: You must specify the name of the input file."
    sys.exit()
  
  plot_file_name = None
  if len(sys.argv) > 2:
    plot_file_name = sys.argv[2]
  
  # Read file
  settings = ""
  with open(os.path.abspath(file_name), 'r') as f:
    # Split line on commas, spaces, or tabs
    settings = [tuple(re.split(",| |\t", line.strip())) for line in f]
  
  # 0 is not started, 1 is started, 2 is done
  reading_prob = 0
  reading_est = 0
  prob = []
  ests = []
  
  for l in settings:
    if l[0] == "\n":
      # skip blank lines
      continue
    if reading_prob == 1:
      # Read in probability, skipping blanks
      prob = [int(i) for i in l if i]
      reading_prob = 2
      continue
    if reading_est == 1:
      # Read in estimates, skipping blanks
      ests.append([int(i) for i in l[1:] if i])
      continue
    if l[0] == "==":
      if reading_prob:
        reading_est = 1
      else:
        reading_prob = 1

   # Run Monte Carlo
  (niter, scenarios) = mc_scenarios(ests, prob)
  
  if plot_file_name:
    plot_histogram(scenarios, plot_file_name)

  # Calculate and display stats
  s_min = min(scenarios)
  s_max = max(scenarios)
  s_range = s_max - s_min
  s_l = len(scenarios)
  s_sum = sum(scenarios)
  s_mean = s_sum/float(s_l)
  s_stddev = sum(abs(s - s_mean) for s in scenarios)/float(s_l)
  
  # Print out contents
  print "N ATTEMPTS: %s" % niter
  print "N SELECTED: %s" % s_l
  print "ACCEPTANCE RATE: %4.2f%%" % (s_l/float(niter) * 100)
  print '<<-- should be 20-80% -->>'
  print "MEAN: %s" % s_mean
  print "MIN: %s" % s_min
  print "MAX: %s" % s_max
  print "RANGE: %s" % s_range
  print "STD DEV: %s" % s_stddev

    

    