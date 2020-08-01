# Simulation-MarkovChains
Simulating Monte Carlo Markov Chains in Python using the theme of an epidemic spreading within a fixed population.

The following variables are used through the Python scripts:
* `M` - the size of the population
* `I` - the number of infected people
* `S` - the number of susceptible people
* `k` - the state number in the Markov Chain
* `C_lk` and `B_lk` - binomial random variables to calculate the number of people infected or recovered at state `k`
* `p` - probability of recovery
* `q_k` - probability of becoming infected
* `beta` - variable used within `q_k`, to be determined

Each of the Python scripts is related to a particular question.


Each of the R-scripts in the folder `R` represents a different model layout and can run under flexible settings of level of interaction information per triplet by changing the contents of the `ecov` vector.

The folder `Workspaces` contains a total of 252 separate workspaces, each containing a list of results from 1000 simulations. A breakdown of the workspaces is done as follows:
* 7 model layouts
* For each model layout, 12 threshold levels (False, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, True)
* For each threshold level, 3 cases: full synergy, full redundancy or full zero-interaction.
    + 7 * 12 * 3 = 252 unique scenarios

The folder `Visualization` uses combined results from those 252 workspaces to create a bigger, single workspace per visualization topic. It mainly contains scripts to reproduce the visualizations shown for the main results in the dissertation, along with extra, rejected visualization approaches.
