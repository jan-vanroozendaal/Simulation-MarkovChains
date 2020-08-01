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
* `beta` - variable used within `q_k`, to be determined. Its true distribution is unknown, but we start from the assumption of a prior Uniform(0,1) distribution.

The Python scripts tagged with `Q1` and `Q2` form the baseline code of the Markov Chain simulation.

The Python script tagged with `Q6` deals with investigating posterior distributions of `beta` for each state transition. Here, we assume that the Markov chain starts with the following sequence of number of infected people: `1 - 4 - 7 - 6 - 16 - 14`.

The Python scripts tagged with `Q7` deal with importance sampling; the ones tagged with `Q8` deal with applying MCMC using different proposal distributions for `beta`: (a) a beta-distribution; (b) a truncated Normal distribution with limited range [0,1]; and (c) a triangular distribution with limited range [0,1].
