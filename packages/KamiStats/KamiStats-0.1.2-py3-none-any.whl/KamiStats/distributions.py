import math
import sympy as sp
import scipy.stats as sc
from statistics import mean, variance

class BinomialDist:
    "Binomial distribution of a random variable"
    # https://en.wikipedia.org/wiki/Binomial_distribution

    __slots__ = {'_n': "n independent experiments", 
                 '_p': "probability of success in each experiment",
                 '_q': "probability of failure in each experiment",
                 '_k': "number of successes in n trials"}
    
    def __init__(self, n: int, p: float, q: float, k: int)-> None:
        """Initializes Binomial Distribution where n is equal to the number of trials and p is the probability of success in each trial 
        and q is the probability of failure in each trial."""
        if n < 0 or k <= 0:
            raise ValueError("n must be greater than 0 and k must be greater than or equal to 0")
        elif p < 0 or p > 1 or q < 0 or q > 1:
            raise ValueError("p must be between 0 and 1 and q must be between 0 and 1")
        elif (round(1-p, 4) != round(q, 4)):
            raise ValueError("p and q must be complements of each other")
        elif(q == None or p == None):
            q = 1 - p
            p = 1 - q
        elif type(n) == bool or type(p) == bool or type(q) == bool or type(k) == bool:
            raise ValueError("n, p, q, and k must be integers or floats")
        
        self._n = int(n)
        self._p = float(p)
        self._q = float(q)
        self._k = int(k)

    @classmethod
    def from_samples(cls, data, p: float, k : int) -> "BinomialDist":
        "Make a binomial distribution instance from sample data."
        if(len(data) <= 0 and k < 0):
            raise ValueError("sample data must contain at least one value and k must be greater than or equal to 0")
        if any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than 0")
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1")
        n = len(data)
        q = 1-p
        return cls(n, p, q, k)
    
    def pmf(self: "BinomialDist") -> float:
        """We write X ~ B(n, p). The probability of getting exactly k successes in n independent Bernoulli trials (with the same rate p) 
        is given by the probability mass function: P(X = k) = C(n, k) * p^k * q^(n-k) where C(n, k) = n! / (k! * (n-k)!) is the binomial coefficient."""
        return math.comb(self._n, self._k) * (self._p ** self._k) * (self._q ** (self._n - self._k))

    def cdf(self: "BinomialDist") -> float:
        """The cumulative distribution function is the probability of getting k or fewer successes in n independent Bernoulli trials (with the same rate p). 
        It is given by the formula: P(X ≤ k) = ∑(i=0, k) C(n, i) * p^i * q^(n-i)"""
        cumulative_prob = 0
        for i in range(self._k + 1):
            self._k = i
            cumulative_prob += self.pmf()
        return cumulative_prob
    
    @property
    def mean(self: "BinomialDist") -> float:
        return self._n * self._p
    
    @property
    def variance(self: "BinomialDist") -> float:
        return self._n * self._p * self._q
    
    @property
    def std_dev(self: "BinomialDist") -> float:
        return math.sqrt(self.variance)
    
    def __repr__(self: "BinomialDist") -> str:
        return f"{type(self).__name__} with values: (n={self._n}, p={self._p}, q={self._q}, k={self._k})"
    
class HypergeometricDist:
    "Hypergeometric distribution of a random variable"
    # https://en.wikipedia.org/wiki/Hypergeometric_distribution

    __slots__ = {'_N': "total number of objects in the in population", 
                 '_K': "number of success states in the sample",
                 '_n': "total number of trials selected(sample size)",
                 '_k': "number of successes observed(of specified feauture) in n trials"}
    
    def __init__(self, N, n, K, k) -> None:
        """Describes the probability of k successes (random draws for which the object drawn has a specified feature) in n draws, without 
        replacement, from a finite population of size N that contains exactly objects with that feature, wherein each draw is either 
        a success or a failure."""
        if N < 0 or n < 0 or K <= 0:
            raise ValueError("N, n, and K must be greater than or equal to 0")
        elif n > N:
            raise ValueError("n must be less than or equal to ")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif K <= 0:
            raise ValueError("K must be greater than 0")
        
        self._N = int(N)
        self._K = int(K)
        self._n = int(n)
        self._k = int(k)

    @classmethod
    def from_samples(cls, data, n, K, k) -> "HypergeometricDist":
        "Make a hypergeometric distribution instance from sample data."
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and k must be greater than or equal to 0")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or euqal to 0")
        N = len(data)
        return cls(N, n, K, k)
    
    def pmf(self: "HypergeometricDist") -> float:
        """We write X ~ H(N, n, r). The probability of getting exactly k successes in n trials (without replacement) is given by the probability mass function: 
        P(X = k) = C(r, k) * C(N-r, n-k) / C(N, n) where C(n, k) = n! / (k! * (n-k)!) is the binomial coefficient."""
        return (math.comb(self._K, self._k) * math.comb(self._N - self._K, self._n - self._k)) / math.comb(self._N, self._n)

    def cdf(self: "HypergeometricDist") -> float:
        """The cumulative distribution function is the probability of getting k or fewer successes in n trials (without replacement). 
        It is given by the formula: P(X ≤ k) = ∑(i=0, k) C(r, i) * C(N-r, n-i) / C(N, n)"""
        cumalative_prob = 0
        for i in range(self._k + 1):
            cumalative_prob += self.pmf()
            self._k-= 1 
        return cumalative_prob
    
    @property
    def mean(self: "HypergeometricDist") -> float:
        """The mean of the hypergeometric distribution is given by the formula: E(X) = n * (K / N)"""
        return self._n * (self._K / self._N)
    
    @property
    def variance(self: "HypergeometricDist") -> float:
        """The variance of the hypergeometric distribution is given by the formula: Var(X) = n * (K / N) * [(N - K) / N] * [(N - n) / (N - 1)]"""
        return self._n * (self._K / self._N) * ((self._N - self._K) / self._N) * ((self._N - self._n) / (self._N - 1))
    
    @property
    def std_dev(self: "HypergeometricDist") -> float:
        """The standard deviation of the hypergeometric distribution is given by the formula: σ = sqrt(Var(X))"""
        return math.sqrt(self.variance)
    
    def __repr__(self: "HypergeometricDist") -> str:
        return f"{type(self).__name__} with values: (N={self._N}, n={self._n}, K={self._K}, k={self._k})"

class PoissonDist:
    "Poisson distribution of a random variable"
    # https://en.wikipedia.org/wiki/Poisson_distribution

    __slots__ = {'_λ': "average rate of success", 
                 '_k': "number of successes in a fixed interval of time or space"}
    
    def __init__(self, λ, k) -> None:
        """Describes the probability of k successes in a fixed interval of time or space, given that the average rate of success is λ."""
        if λ < 0 or k < 0:
            raise ValueError("λ and k must be greater than or equal to 0")
        if type(λ) == bool or type(k) == bool:
            raise ValueError("λ and k must be integers or floats")
        
        self._λ = float(λ)
        self._k = int(k)

    @classmethod
    def from_samples(cls, data, k) -> "PoissonDist":
        "Make a poisson distribution instance from sample data."
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and k must be greater than or equal to 0")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or euqal to 0")
        elif type(k) == bool:
            raise ValueError("k must be an integer or float")
        λ = mean(data)
        return cls(λ, k)
    
    def pmf(self: "PoissonDist") -> float:
        """We write X ~ P(λ). The probability of getting exactly k successes in a fixed interval of time or space is given by the probability mass function: 
        P(X = k) = (λ^k * e^(-λ)) / k!"""
        return (self._λ ** self._k) * math.exp(-self._λ) / math.factorial(self._k)

    def cdf(self: "PoissonDist") -> float:
        """The cumulative distribution function is the probability of getting k or fewer successes in a fixed interval of time or space. 
        It is given by the formula: P(X ≤ k) = ∑(i=0, k) (λ^i * e^(-λ)) / i!"""
        cumalative_prob = 0
        for i in range(self._k+1):
            cumalative_prob += self.pmf()
            self._k-= 1 
        return cumalative_prob
    
    @property 
    def mean(self: "PoissonDist") -> float:
        """The mean of the poisson distribution is given by the formula: E(X) = λ"""
        return self._λ
    
    @property
    def variance(self: "PoissonDist") -> float:
        """The variance of the poisson distribution is given by the formula: Var(X) = λ"""
        return self._λ
    
    @property
    def std_dev(self: "PoissonDist") -> float:
        """The standard deviation of the poisson distribution is given by the formula: σ = sqrt(λ)"""
        return math.sqrt(self._λ)
    
    def __repr__(self: "PoissonDist") -> str:
        return f"{type(self).__name__} with values: (λ={self._λ}, k={self._k})"
    
class GeometricDist:
    "Discrete Geometric distribution of a random variable"
    # https://en.wikipedia.org/wiki/Geometric_distribution

    __slots__ = {'_p': "probability of success in each trial", 
                 '_q': "probability of failure in each trial",
                 '_k': "number of trials until the first success"}
    
    def __init__(self, p, q, k) -> None:
        """
        ## Description
        Make an instance of a Discrete Geometric Distribution, where the geometric distribution describes
        the number of trials it takes to achieve the first success in a sequence of independent Bernoulli trials.
        
        ## Parameters
        - p: float
            probability of success in each trial
        - q: float
            probability of failure in each trial
        - k: int
            number of trials until the first success
        
        ## Returns
        None, it creates an instance of the Geometric Distribution class.
        """
        if p < 0 or p > 1 or q < 0 or q > 1:
            raise ValueError("p must be between 0 and 1 and q must be between 0 and 1")
        elif(q == None or p == None):
            q = 1 - p
            p = 1 - q
        elif (round(1-p, 4) != round(q, 4)):
            raise ValueError("p and q must be complements of each other")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif type(p) == bool or type(q) == bool or type(k) == bool:
            raise ValueError("p, q, and k must be integers or floats")
        
        self._p = float(p)
        self._q = float(q)
        self._k = int(k)

    @classmethod
    def from_samples(cls, data, k) -> "GeometricDist":
        """
        ## Description
        Make a discrete geometric distribution instance from sample data.
        
        ## Parameters
        - data: list
            sample data
        - k: int
            number of trials until the first success
        
        ## Returns
        None, it creates an instance of the Geometric Distribution class.
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and k must be greater than or equal to 0")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or euqal to 0")
        p = mean(data)
        q = 1 - p
        return cls(p, q, k)
    
    def pmf(self: "GeometricDist") -> float:
        """
        ## Descriptions
        We write X ~ G(p). describes when the first success in an infinite sequence of independent and identically 
        distributed Bernoulli trials occurs. The probability mass function is given P(X = k) = q^(k-1) * p
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting exactly k failures before the first success in a sequence of Bernoulli trials.
        """
        return (self._q ** (self._k - 1)) * self._p

    def cdf(self: "GeometricDist") -> float:
        """
        ## Description
        The cumulative distribution function is the probability of getting success with k or fewer tirals.
        P(X ≤ k) = 1 - (q)^(floor(x)) for x>=1, for x<1, P(X ≤ k) = 0  .
        ## Parameters
        None

        ## Returns
        float, the probability of getting k or fewer failures before the first success in a sequence of Bernoulli trials.
        """
        if self._k >= 1:
            cumulative_prob = 1 - self._q**(math.floor(self._k))
        else:  
            cumulative_prob = 0
        return cumulative_prob

    @property
    def mean(self: "GeometricDist") -> float:
        """
        ## Description
        The mean of the geometric distribution is given by the formula: E(X) = 1 / p
        
        ## Parameters
        None

        ## Returns
        float, the mean of the geometric distribution.
        """
        return 1 / self._p
    
    @property
    def variance(self: "GeometricDist") -> float:
        """
        ## Description
        The variance of the geometric distribution is given by the formula: Var(X) = q / p^2
        
        ## Parameters
        None

        ## Returns
        float, the variance of the geometric distribution.
        """
        return (self._q) / (self._p ** 2)
    
    @property
    def std_dev(self: "GeometricDist") -> float:
        """
        ## Description
        The standard deviation of the geometric distribution is given by the formula: σ = sqrt(q / p^2)
        
        ## Parameters
        None

        ## Returns
        float, the standard deviation of the geometric distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "GeometricDist") -> str:
        """
        ## Description
        The string representation of the Geometric Distribution class.

        ## Parameters
        None

        ## Returns
        str, the string representation of the Geometric Distribution class.
        """
        return f"{type(self).__name__} with values: (p={self._p}, q={self._q}, k={self._k})"
    
class UniformDist:
    "Uniform distribution of a random variable"
    # https://en.wikipedia.org/wiki/Discrete_uniform_distribution
    
    __slots__ = {'_a': "minimum value", 
                 '_b': "maximum value",
                 '_x': "random variable",
                 "_n": "number of equally likely outcomes"}
    
    def __init__(self, a, b, x) -> None:
        """
        ##  Description
        Discrete uniform distribution is a probability distribution that describes the likelihood of outcomes when each outcome in a 
        finite set is equally likely. Make an instance of a Uniform Distribution, where the uniform distribution describes the probability 
        of a random variable taking on a value within a given range.
        
        ##  Parameters
        - a: float
            minimum value
        - b: float
            maximum value
        - x: float
            random variable
        
        ##  Returns
        None, it creates an instance of the Uniform Distribution class.
        """
        if a < 0 or b < 0 or x < 0:
            raise ValueError("a, b, and x must be greater than or equal to 0")
        elif a > b:
            raise ValueError("a must be less than or equal to b")
        elif x < a or x > b:
            raise ValueError("x must be greater than or equal to a and less than or equal to b")
        elif type(a) == bool or type(b) == bool or type(x) == bool:
            raise ValueError("a, b, and x must be integers or floats")
        
        self._a = float(a)
        self._b = float(b)
        self._x = float(x)
        self._n = int(b - a)

    @classmethod
    def from_samples(cls, data, x) -> "UniformDist":
        "Make a uniform distribution instance from sample data."
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x < 0:
            raise ValueError("x must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or euqal to 0")
        a = min(data)
        b = max(data)
        return cls(a, b, x)
    
    def pmf(self: "UniformDist") -> float:
        """We write X ~ U(a, b). The probability mass function(a.k.a probability density function) of a uniform distribution is given by the formula: 
        f(x) = 1 / (n)"""
        return 1 / (self._n)

    def cdf(self: "UniformDist") -> float:
        """The cumulative distribution function is the probability of getting a value less than or equal to x in a uniform distribution.
        f(x) = (floor[x] - a + 1) / n"""
        return (math.floor(self._x) - self._a + 1) / (self._n)
    
    @property
    def mean(self: "UniformDist") -> float:
        """The mean of the uniform distribution is given by the formula E(X) = (a + b) / 2"""
        return (self._a + self._b) / 2
    
    @property
    def variance(self: "UniformDist") -> float:
        """The variance of the uniform distribution is given by the formula Var(X) = (((n+1)^2) - 1) / 12"""
        return (((self._n + 1) ** 2) - 1) / 12
    
    @property
    def std_dev(self: "UniformDist") -> float:
        """The standard deviation of the uniform distribution is given by the formula σ = sqrt((n^2 - 1) / 12)"""
        return math.sqrt(self.variance)
    
    def __repr__(self: "UniformDist") -> str:
        return f"{type(self).__name__} with values: (a={self._a}, b={self._b}, x={self._x})"
    
class ExponentialDist:
    "Exponential distribution of a random variable"
    # https://en.wikipedia.org/wiki/Exponential_distribution
    
    __slots__ = {'_λ': "rate of success", 
                 '_x': "random variable"}
    
    def __init__(self, λ, x) -> None:
        """
        ## Description
        The exponential distribution in R Language is the probability distribution of the time between events in a Poisson point 
        process, i.e., a process in which events occur continuously and independently at a constant average rate.
        Describes the probability of a random variable taking on a value within a given range, given that the rate of success is λ.
        
        ## Parameters
        - λ: float
            rate of success
        - x: float
            random variable
        
        ## Returns
        None, it creates an instance of the Exponential Distribution class.
        """
        if λ < 0 or x < 0:
            raise ValueError("λ and x must be greater than or equal to 0")
        elif type(λ) == bool or type(x) == bool: 
            raise ValueError("λ and x must be integers or floats")
        self._λ = float(λ)
        self._x = float(x)
    
    @classmethod
    def from_samples(cls, data, x) -> "ExponentialDist":
        """
        ## Description
        Make an exponential distribution instance from sample data.

        ## Parameters
        - data: list
            sample data
        
        ## Returns
        None, it creates an instance of the Exponential Distribution class.
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x < 0:
            raise ValueError("x must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or equal to 0")
        λ = 1 / mean(data)
        return cls(λ, x)
    
    def pdf(self: "ExponentialDist") -> float:
        """
        ## Description
        We write X ~ Exp(λ). The probability of getting a value less than or equal to x in an exponential distribution is given by the
        formula: f(x) = λ * e^(-λ * x)

        ## Parameters
        None

        ## Returns
        float, the probability of getting a value less than or equal to x in an exponential distribution.
        """
        return self._λ * math.exp(-self._λ * self._x)
    
    def cdf(self: "ExponentialDist") -> float:
        """
        ## Desciprtion
        The cumulative distribution function is the probability of getting a value less than or equal to x in an exponential distribution.
        F(x) = 1 - e^(-λ * x)

        ## Parameters
        None

        ## Returns
        float, the probability of getting a value less than or equal to x in an exponential distribution.
        """
        return 1 - math.exp(-self._λ * self._x)
    
    @property
    def mean(self: "ExponentialDist") -> float:
        """
        ## Description
        The mean of the exponential distribution is given by the formula E(X) = 1 / λ
        
        ## Parameters
        None

        ## Returns
        float, the mean of the exponential distribution.
        """
        return 1 / self._λ
    
    @property
    def variance(self: "ExponentialDist") -> float:
        """
        ## Description
        The variance of the exponential distribution is given by the formula Var(X) = 1 / λ^2
        
        ## Parameters
        None

        ## Returns
        float, the variance of the exponential distribution.
        """
        return 1 / (self._λ ** 2)
    
    @property
    def std_dev(self: "ExponentialDist") -> float:
        """
        ## Description
        The standard deviation of the exponential distribution is given by the formula σ = sqrt(1 / λ^2)
        
        ## Parameters
        None

        ## Returns
        float, the standard deviation of the exponential distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "ExponentialDist") -> str:
        """
        ## Description
        Create a string representation of the Exponential Distribution class.

        ## Parameters
        None

        ## Returns
        str, the string representation of the Exponential Distribution class.
        """
        return f"{type(self).__name__} with values: (λ={self._λ}, x={self._x})"

class NegativeBinomialDist:
    "Negative Binomial distribution of a random variable"
    # https://en.wikipedia.org/wiki/Negative_binomial_distribution

    __slots__ = {'_r': "number of successes", 
                 '_p': "probability of success in each trial",
                 '_q': "probability of failure in each trial",
                 '_k': "number of trials until the rth success"}
    
    def __init__(self, r, p, q, k) -> None:
        """
        ## Description
        The negative binomial distribution describes the number of trials(failures) it takes to achieve the rth success in a sequence 
        of independent Bernoulli trials. Make an instance of a Negative Binomial Distribution, where the negative binomial distribution 
        describes the probability of a random variable taking on a value within a given range.
        
        ## Parameters
        - r: int
            number of successes
        - p: float
            probability of success in each trial
        - q: float
            probability of failure in each trial
        - k: int
            number of trials until the rth success
        
        ## Returns
        None, it creates an instance of the Negative Binomial Distribution class.
        """
        if r < 0 or p < 0 or p > 1 or q < 0 or q > 1 or k < 0:
            raise ValueError("r, p, q, and k must be greater than or equal to 0")
        elif(q == None or p == None):
            q = 1 - p
            p = 1 - q
        elif (round(1-p, 2) != round(q, 2)):
            raise ValueError("p and q must be complements of each other")
        elif isinstance(r, bool) or isinstance(p, bool) or isinstance(q, bool) or isinstance(k, bool):
            raise ValueError("r, p, q, and k must be integers or floats")
        
        self._r = int(r)
        self._p = float(p)
        self._q = float(q)
        self._k = int(k)

    @classmethod
    def from_samples(cls, data, r, k) -> "NegativeBinomialDist":
        """
        ## Description
        Make a negative binomial distribution instance from sample data.

        ## Parameters
        - data: list
            sample data
        - r: int
            number of successes
        - k: int
            number of trials until the rth success
        
        ## Returns
        None, it creates an instance of the Negative Binomial Distribution class
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and k must be greater than or equal to 0")
        elif k < 0:
            raise ValueError("k must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or euqal to 0")
        p = mean(data)
        q = 1 - p
        return cls(r, p, q, k)
    
    def pmf(self: "NegativeBinomialDist") -> float:
        """
        ## Description
        We write X ~ NB(r, p). The probability of getting exactly k failures before the rth success in a sequence 
        of Bernoulli trials is given by the probability mass function: P(X = k) = C(k + r - 1, r) * p^r * q^k
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting exactly k failures before the rth success in a sequence of Bernoulli trials.
        """
        return math.comb(self._k + self._r - 1, self._k) * (self._p ** self._r) * (self._q ** self._k)
    
    def cdf(self: "NegativeBinomialDist") -> float:
        """
        ## Description
        The cumulative distribution function is the probability of getting k or fewer failures before the rth success 
        in a sequence of Bernoulli trials. X~NB(r, p). It is given by the formula: P(X ≤ k) = Ip(r, k+1)
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting k or fewer failures before the rth success in a sequence of Bernoulli trials.
        """
        cumulative_prob = 0
        for i in range(self._k+1):
            self._k = i
            cumulative_prob += self.pmf()
        return cumulative_prob
    
    @property
    def mean(self: "NegativeBinomialDist") -> float:
        """
        ## Description
        The mean of the negative binomial distribution is given by the formula E(X) = (r * q)/ p
        
        ## Parameters
        None

        ## Returns
        float, the mean of the negative binomial distribution.
        """
        return (self._r * self._q) / self._p
    
    @property
    def variance(self: "NegativeBinomialDist") -> float:
        """
        ## Desciprtion
        The variance of the negative binomial distribution is given by the formula Var(X) = r * q / p^2
        
        ## Parameters
        None

        ## Returns
        float, the variance of the negative binomial distribution.
        """
        return (self._r * self._q )/ (self._p ** 2)
    
    @property
    def std_dev(self: "NegativeBinomialDist") -> float:
        """
        ## Description
        The standard deviation of the negative binomial distribution is given by the formula σ = sqrt(r * q / p^2)
        
        ## Parameters
        None   

        ## Returns
        float, the standard deviation of the negative binomial distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "NegativeBinomialDist") -> str:
        """
        ## Description
        The string representation of the Negative Binomial Distribution class.

        ## Parameters
        None

        ## Returns
        str, the string representation of the Negative Binomial Distribution class.
        """
        
        return f"{type(self).__name__} with values: (r={self._r}, p={self._p}, q={self._q}, k={self._k})"
    
class StudentDist:
    "Student's t-distribution of a random variable"
    # https://en.wikipedia.org/wiki/Student%27s_t-distribution

    __slots__ = {'_ν': "degrees of freedom", 
                 '_x': "random variable"}
    
    def __init__(self, ν, x) -> None:
        """
        ## Description
        The Student's t-distribution is a continuous probability distribution that is used to estimate the mean of a normally distributed population 
        when the sample size is small and the population standard deviation is unknown. Make an instance of a Student's 
        t-distribution, where the Student's t-distribution describes the probability of a random variable taking on a 
        value within a given range.
        
        ## Parameters
        - ν: float
            degrees of freedom
        - x: float
            random variable
        
        ## Returns
        None, it creates an instance of the Student's t-distribution class.
        """
        if ν < 0 or x < 0:
            raise ValueError("ν and x must be greater than or equal to 0")
        if isinstance(ν, bool) or isinstance(x, bool):
            raise ValueError("ν and x must be integers or floats")
        self._ν = float(ν)
        self._x = float(x)
    
    @classmethod
    def from_samples(cls, data, x) -> "StudentDist":
        """
        ## Description
        Make a student's t-distribution instance from sample data.
        
        ## Parameters
        - data: list
            sample data
        - x: float
            random variable
        
        ## Returns
        None, it creates an instance of the Student's t-distribution class.
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x < 0:
            raise ValueError("x must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or equal to 0")
        ν = len(data) - 1
        return cls(ν, x)
    
    def pdf(self: "StudentDist") -> float:
        """
        ## Description
        We write X ~ t(ν). The probability of getting a value less than or equal to x in a student's t-distribution is given by the formula: 
        f(x) = Γ((ν + 1) / 2) / (sqrt(πν) * Γ(ν / 2)) * (1 + x^2 / ν)^(-(ν + 1) / 2)
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting a value less than or equal to x in a student's t-distribution.
        """
        return (sp.gamma((self._ν + 1) / 2) / (math.sqrt(math.pi * self._ν) * sp.gamma(self._ν / 2))) * (1 + (self._x ** 2) / self._ν) ** (-(self._ν + 1) / 2)
    
    def cdf(self: "StudentDist") -> float:
        """
        ## Description
        The cumulative distribution function is the probability of getting a value less than or equal to x in a student's 
        t-distribution. F(x) = 1 - 0.5 * [I_{x(t}(ν / 2, 1 / 2)]
        
        ## Parameters
        None
        
        ## Returns 
        float, the probability of getting a value less than or equal to x in a student's t-distribution.
        """
        return sc.t.cdf(self._x, self._ν)
    
    @property
    def mean(self: "StudentDist") -> float:
        """
        ## Description
        The mean of the student's t-distribution is given by the formula E(X) = 0
        
        ## Parameters
        None

        ## Returns
        float, the mean of the student's t-distribution.
        """
        if self._ν > 1:
            return 0
        elif self._ν <= 1:
            return math.nan
    
    @property
    def variance(self: "StudentDist") -> float:
        """
        ## Description
        The variance of the student's t-distribution is given by the formula Var(X) = ν / (ν - 2)
        
        ## Parameters
        None

        ## Returns
        float, the variance of the student's t-distribution.
        """
        if self._ν > 2:
            return self._ν / (self._ν - 2)
        elif self._ν < 2 and self._ν > 1:
            return math.inf
        else:
            return math.nan

    
    @property
    def std_dev(self: "StudentDist") -> float:
        """
        ## Description
        The standard deviation of the student's t-distribution is given by the formula σ = sqrt(ν / (ν - 2))
        
        ## Parameters
        None

        ## Returns
        float, the standard deviation of the student's t-distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "StudentDist") -> str:
        """
        ## Description
        The string representation of the Student's t-distribution class.

        ## Parameters
        None

        ## Returns
        str, the string representation of the Student's t-distribution class.
        """
        return f"{type(self).__name__} with values: (ν={self._ν}, x={self._x})"
    
class FDist:
    "Fisher-Snedechor's or F-distribution of a random variable"
    # https://en.wikipedia.org/wiki/F-distribution

    __slots__ = {'_ν1': "degrees of freedom of the numerator", 
                 '_ν2': "degrees of freedom of the denominator",
                 '_x': "random variable"}
    
    def __init__(self, ν1, ν2, x) -> None:
        """
        ## Description
        The F-distribution with d1 and d2 degrees of freedom is the distribution of the ratio of two independent chi-squared random variables, each divided by its degrees of freedom. The F-distribution is a probability distribution that is used in the analysis of variance tests. Make an instance of an F-distribution, where 
        the F-distribution describes the probability of a random variable taking on a value within a given range.
        
        ## Parameters
        - ν1: float
            degrees of freedom of the numerator
        - ν2: float
            degrees of freedom of the denominator
        - x: float
            random variable
        
        ## Returns
        None, it creates an instance of the F-distribution class.
        """
        if ν1 < 0 or ν2 < 0 or x < 0:
            raise ValueError("ν1, ν2, and x must be greater than or equal to 0")
        elif isinstance(ν1, bool) or isinstance(ν2, bool) or isinstance(x, bool):
            raise ValueError("ν1, ν2, and x must be integers or floats")
        self._ν1 = float(ν1)
        self._ν2 = float(ν2)
        self._x = float(x)
    
    @classmethod
    def from_samples(cls, data, x) -> "FDist":
        """
        ## Description
        Make an F-distribution instance from sample data.

        ## Parameters
        - data: list
            sample data
        - x: float
            random variable
        
        ## Returns
        None, it creates an instance of the F-distribution class.
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x < 0:
            raise ValueError("x must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or equal to 0")
        elif isinstance(data, bool) or isinstance(x, bool):
            raise ValueError("sample data and x must be integers or floats")
        ν1 = len(data) - 1
        ν2 = len(data) - 1
        return cls(ν1, ν2, x)
    
    def pdf(self: "FDist") -> float:
        """
        ## Description
        We write X ~ F(ν1, ν2). The probability of getting a value less than or equal to x in an F-distribution is given by the formula: f(x) = sqrt(((ν1 * x)^ν1 * (v2^v2)) / (ν1 * x + v2) ^(v1 + v2)) / (x * B(ν1 / 2, ν2 / 2))
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting a value less than or equal to x in an F-distribution.
        """
        return math.sqrt(((self._ν1 * self._x) ** self._ν1 * (self._ν2 ** self._ν2)) / 
                         ((self._ν1 * self._x + self._ν2) ** (self._ν1 + self._ν2))) / (self._x * sp.beta(self._ν1 / 2, self._ν2 / 2))

    def cdf(self: "FDist") -> float:
        """
        ## Description
        The cumulative distribution function is the probability of getting a value less than or equal to x in an F-distribution. F(x) = I_{(v1 * x) / (v1 * x + v2)}(ν1 / 2, ν2 / 2). Use scipys cdf function to calculate the cumulative distribution function.
        
        ## Parameters
        None

        ## Returns
        float, the probability of getting a value less than or equal to x in an F-distribution.
        """
        return sc.f.cdf(self._x, self._ν1, self._ν2)
    @property
    def mean(self: "FDist") -> float:
        """
        ## Descritpion
        The mean of the F-distribution is given by the formula E(X) = ν2 / (ν2 - 2)
        
        ## Parameters
        None

        ## Returns
        float, the mean of the F-distribution.
        """
        if self._ν2 > 2:
            return self._ν2 / (self._ν2 - 2)
        else:
            return math.nan
        
    @property
    def variance(self: "FDist") -> float:
        """
        ## Description
        The variance of the F-distribution is given by the formula Var(X) = (2ν2^2 * (ν1 + ν2 - 2)) / (ν1 * (ν2 - 2)^2 * (ν2 - 4))
        
        ## Parameters   
        None

        ## Returns
        float, the variance of the F-distribution.
        """
        if self._ν2 > 4:
            return ((2 * (self._ν2 ** 2)) * (self._ν1 + self._ν2 - 2)) / (self._ν1 * ((self._ν2 - 2) ** 2) * (self._ν2 - 4))
        elif self._ν2 < 4 and self._ν2 > 2:
            return math.inf
        else:
            return math.nan
    
    @property
    def std_dev(self: "FDist") -> float:
        """
        ## Description
        The standard deviation of the F-distribution is given by the formula σ = sqrt((2ν2^2 * (ν1 + ν2 - 2)) / (ν1 * (ν2 - 2)^2 * (ν2 - 4))
        
        ## Parameters
        None

        ## Returns
        float, the standard deviation of the F-distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "FDist") -> str:
        """
        ## Description
        The string representation of the F-distribution class.

        ## Parameters
        None

        ## Returns
        str, the string representation of the F-distribution class.
        """
        
        return f"{type(self).__name__} with values: (ν1={self._ν1}, ν2={self._ν2}, x={self._x})"

class GammaDist:
    "Gamma distribution of a random variable"
    # https://en.wikipedia.org/wiki/Gamma_distribution

    __slots__ = {'_α': "shape parameter", 
                 '_β': "rate parameter",
                 '_x': "random variable"}
    
    def __init__(self, α, β, x) -> None:
        """
        ## Description of the Gamma Distribution
        The gamma distribution is a two-parameter family of continuous probability distributions. The exponential distribution, 
        Erlang distribution, and chi-squared distribution are special cases of the gamma distribution. Make an instance of a 
        Gamma Distribution, where the gamma distribution describes the probability of a random variable taking on a value within
        a given range.
        
        ## Parameters
        - α: float
            The shape parameter.
        - β: float
            The rate parameter.
        - x: float
            The random variable.
        
        ## Returns
        - None, it initializes the Gamma Distribution instance.
        
        """
        if α <= 0 or β <= 0 or x <= 0:
            raise ValueError("α, β, and x must be greater than 0")
        elif isinstance(α, bool) or isinstance(β, bool) or isinstance(x, bool):
            raise ValueError("α, β, and x must be integers or floats")
        self._α = float(α)
        self._β = float(β)
        self._x = float(x)
    
    @classmethod
    def from_samples(cls, data, x) -> "GammaDist":
        "Make a gamma distribution instance from sample data."
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x <= 0:
            raise ValueError("x must be greater than 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or equal to 0")
        elif isinstance(data, bool) or isinstance(x, bool):
            raise ValueError("sample data and x must be integers or floats")
        α = mean(data) ** 2 / variance(data)
        β = variance(data) / mean(data)
        return cls(α, β, x)
    
    def pdf(self: "GammaDist") -> float:
        """We write X ~ Γ(α, β). The probability of getting a value less than or equal to x in a gamma distribution is given by the formula: 
        f(x) = (β^α * x^(α - 1) * e^(-β * x)) / Γ(α)"""
        return (((self._β ** self._α) * (self._x ** (self._α - 1)) * math.exp(-self._β * self._x))) / (sp.gamma(self._α))
    
    def cdf(self: "GammaDist") -> float:
        """The cumulative distribution function is the probability of getting a value less than or equal to x in a gamma distribution.
        F(x) = (1 / Γ(α)) * γ(α, β * x)
        Using scipys cdf function to calculate the cumulative distribution function.
        """
        return sc.gamma.cdf(self._x, self._α, scale=1/self._β)
    
    @property
    def mean(self: "GammaDist") -> float:
        """The mean of the gamma distribution is given by the formula E(X) = α / β"""
        return self._α / self._β
    
    @property
    def variance(self: "GammaDist") -> float:
        """The variance of the gamma distribution is given by the formula Var(X) = α / β^2"""
        return self._α / (self._β ** 2)
    
    @property
    def std_dev(self: "GammaDist") -> float:
        """The standard deviation of the gamma distribution is given by the formula σ = sqrt(α / β^2)"""
        return math.sqrt(self.variance)
    
    def __repr__(self: "GammaDist") -> str:
        return f"{type(self).__name__} with values: (α={self._α}, β={self._β}, x={self._x})"
    
class ChiSquaredDist:
    "Chi-squared distribution of a random variable"
    # https://en.wikipedia.org/wiki/Chi-squared_distribution

    __slots__ = {'_df': "degrees of freedom", 
                 '_x': "random variable"}
    
    def __init__(self, df, x) -> None:
        """
        ## Description of the Chi-Squared Distribution
        The chi-squared distribution is a special case of the gamma distribution. It describes the sum of the squares of 
        df independent standard normal random variables. Make an instance of a Chi-squared Distribution, where the chi-squared 
        distribution describes the probability of a random variable taking on a value within a given range.
        
        ## Parameters
        - df: float
            The degrees of freedom.
        - x: float
            The random variable.

        ## Returns
        - None, it initializes the Chi-squared Distribution instance.
        """
        if df < 0 or x < 0:
            raise ValueError("df and x must be greater than or equal to 0")
        elif type(df) == bool or type(x) == bool:
            raise ValueError("df and x cannot be boolean values") 
        self._df = float(df)
        self._x = float(x)
    
    @classmethod
    def from_samples(cls, data, x) -> "ChiSquaredDist":
        """
        ## Description 
        Initialize an instance of the Chi Square Distribution class from data.
        
        ## Parameters
        - data: List[float]
        - x: float

        ## Returns
        - ChiSquaredDist: An instance of the ChiSquaredDist class.
        """
        if(len(data) <= 0):
            raise ValueError("sample data must contain at least one value and x must be greater than or equal to 0")
        elif x < 0:
            raise ValueError("x must be greater than or equal to 0")
        elif any(x < 0 for x in data):
            raise ValueError("sample data must contain values greater than or equal to 0")
        df = len(data)
        return cls(df, x)
    
    def pmf(self: "ChiSquaredDist") -> float:
        """
        ## Description
        We write X ~ χ^2(ν). The probability of getting the exact x in a chi-squared distribution is 
        given by the formula: f(x) = (1 / (2^(df / 2) * Γ(df / 2))) * x^(df / 2 - 1) * e^(-x / 2)
        
        ## Parameters
        - None

        ## Returns
        - float: The probability of getting the exact x in a chi-squared distribution.
        """
        return (1 / (2 ** (self._df / 2) * sp.gamma(self._df / 2))) * self._x ** (self._df / 2 - 1) * math.exp(-self._x / 2)
    
    def cdf(self: "ChiSquaredDist") -> float:
        """
        ## Description
        The cumulative distribution function is the probability of getting a value less than or equal to x in a chi-squared 
        distribution. F(x) = (1 / Γ(df / 2)) * df(df / 2, x / 2)
        
        ## Parameters
        - None

        ## Returns
        - float: The probability of getting a value less than or equal to x in a chi-squared distribution.
        """
        return (1 / sp.gamma(self._df / 2)) * sp.lowergamma(self._df / 2, self._x / 2)
    
    @property
    def mean(self: "ChiSquaredDist") -> float:
        """
        ## Description
        The mean of the chi-squared distribution is given by the formula E(X) = df
        
        ## Paramaters
        - None

        ## Returns
        - float: The mean of the chi-squared distribution.
        """
        return self._df
    
    @property
    def variance(self: "ChiSquaredDist") -> float:
        """
        ## Description
        The variance of the chi-squared distribution is given by the formula Var(X) = 2df
        
        ## Parameters
        - None
        
        ## Returns
        - float: The variance of the chi-squared distribution.
        """
        return 2 * self._df
    
    @property
    def std_dev(self: "ChiSquaredDist") -> float:
        """
        ## Description
        The standard deviation of the chi-squared distribution is given by the formula σ = sqrt(2df)
        
        ## Parameters
        - None

        ## Returns
        - float: The standard deviation of the chi-squared distribution.
        """
        return math.sqrt(self.variance)
    
    def __repr__(self: "ChiSquaredDist") -> str:
        """
        ## Description
        A string representation of the ChiSquaredDist class.
        
        ## Parameters
        - None

        ## Returns
        - str: A string representation of the ChiSquaredDist
        """
        return f"{type(self).__name__} with values: (df={self._df}, x={self._x})"
    
def main():
    print("""Main function to test the classes""")
    return None

if __name__ == "__main__":
    main()
