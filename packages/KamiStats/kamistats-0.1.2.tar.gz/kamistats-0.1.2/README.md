# KamiStats

KamiStats is a Python module designed to provide implementations of various statistical distributions, including but not limited to Binomial, Hypergeometric, and Poisson distributions. This library allows users to create instances of these distributions, calculate their probability mass functions (PMF), cumulative distribution functions (CDF), and other statistical properties such as mean, variance, and standard deviation.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Binomial Distribution](#binomial-distribution)
  - [Hypergeometric Distribution](#hypergeometric-distribution)
  - [Poisson Distribution](#poisson-distribution)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

Instructions on how to install the necessary packages and set up the environment.

```sh
# Clone the repository
git clone https://github.com/kishimita/KamiStats.git

# Navigate to the project directory
cd KamiStats

# Install the required dependencies
pip install -r requirements.txt
```
## Usage
Below are 3 examples of how to use the distributions of this module to calculate the probability mass function, cumulative probability function, mean, varience and standard deviation. For the rest of the distributions the code is self explanatory and has similar implementation as the ones in the example below. 

### Binomial Distribution
The BinomialDist class represents a binomial distribution.

Example
```python 
from KamiStats import distributions as dist

# Create a Binomial distribution instance
binom_dist = dist.BinomialDist(n=10, p=0.5, q=0.5, k=5)

# Calculate the probability mass function
print(binom_dist.pmf())

# Calculate the cumulative distribution function
print(binom_dist.cdf())

# Get the mean
print(binom_dist.mean)

# Get the variance
print(binom_dist.variance)

# Get the standard deviation
print(binom_dist.std_dev)
```

### Hypergeometric Distribution
The HypergeometricDist class represents a hypergeometric distribution.

Example
```python
from KamiStats import distributions as dist 

# Create a Hypergeometric distribution instance
hypergeom_dist = dist.HypergeometricDist(N=20, n=10, K=5, k=3)

# Calculate the probability mass function
print(hypergeom_dist.pmf())

# Calculate the cumulative distribution function
print(hypergeom_dist.cdf())

# Get the mean
print(hypergeom_dist.mean)

# Get the variance
print(hypergeom_dist.variance)

# Get the standard deviation
print(hypergeom_dist.std_dev)
```

### Poisson Distribution
The PoissonDist class represents a Poisson distribution.

Example
```python
from KamiStats import distributions as dist 

# Create a Poisson distribution instance
poisson_dist = dist.PoissonDist(λ=4, k=2)

# Calculate the probability mass function
print(poisson_dist.pmf())

# Calculate the cumulative distribution function
print(poisson_dist.cdf())

# Get the mean
print(poisson_dist.mean)

# Get the variance
print(poisson_dist.variance)

# Get the standard deviation
print(poisson_dist.std_dev)
```
## Not for Use!
Any file in the test_scripts, and tests. This was used for unittest and due to files and folder struectures the code does not work.

## Dependencies
List of dependencies required for the project are listed here and in the ***requirements.txt*** file.

        Package Version
        ------- -------
        mpmath  1.3.0
        numpy   2.0.1
        pip     24.2
        scipy   1.14.0
        sympy   1.13.2

## License
Copyright 2024 Kishimita
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
(the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.