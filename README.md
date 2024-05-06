# Hidden Markov Models (HMM)

## Introduction
Modeling with a Hidden Markov Model (HMM) will be learned in this assignment, and the Viterbi and the Baum-Welch algorithms will be implemented. HMMs find applications in various fields such as speech and image processing, bioinformatics, and finance.

## Climate Pattern Modeling
El Niño–Southern Oscillation (ENSO), an irregular periodic variation in winds and sea surface temperatures over the tropical eastern Pacific Ocean, affecting the climate of much of the tropics and subtropics, will be focused on. Observations regarding whether it is an El Niño year based on present rainfall in the tropical Pacific can be made. However, understanding past climate variation requires inference from tree ring widths.

Two hidden states representing El Niño and La Niña will be considered, with observed quantities being rainfall estimates from tree ring width data. For simplicity, the observations can be modeled by Gaussian distributions.

For further details, reference can be made to [this link](https://waterprogramming.wordpress.com/2018/07/03/fitting-hidden-markov-models-part-i-background-and-methods/).

## Dataset
Two files will be provided:
- **data.txt**: Contains T rows, each indicating the rainfall for a specific year.
- **parameters.txt**: Contains the number of states n, transition matrix P, means of Gaussian distributions, and standard deviations.

## Input
- **data.txt**: Contains T rows each with a rainfall value for a particular year.
- **parameters.txt**: Contains the number of states n (2 in this case), transition matrix P, means of Gaussian distributions, and standard deviations.

## Output
- **Estimated states file**: A file will be generated containing T rows, each with the estimated state for a particular year.
- **Learned parameters file**: A file will be generated containing the parameters learned using the Baum-Welch algorithm, with the same format as parameters.txt, including the stationary distribution in the last line.
- **Estimated states using learned parameters file**: A file will be generated containing T rows, each with the estimated state for a particular year.

## Viterbi Algorithm Implementation
Given the parameters of the HMM and rainfall estimates, the Viterbi algorithm will be implemented to estimate the most likely hidden state sequence for the past T years.

## Baum-Welch Implementation
The Baum-Welch algorithm will be implemented to estimate the parameters of the HMM and the most likely hidden state sequence for the past T years using the estimated parameters.

The Baum–Welch algorithm, a special case of the Expectation-Maximization (EM) algorithm used to find the unknown parameters of a hidden Markov model (HMM), will be utilized.

## Outputs
The estimated hidden state sequence and parameter values will be outputted to files. Additionally, the solution results will be compared with the sci-kit hmmlearn.
