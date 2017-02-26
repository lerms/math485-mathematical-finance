import numpy as np
from abc import ABC, abstractmethod


class InterestRate:
    def __init__(self, rate, short_term=False):
        """
        :param rate: a given yearly or short-term interest rate
        :param short_term: set this to True if using a short-term interest rate
         yearly interest rate is the interest rate for a full year
         short-term interest rate is the rate between periods
        """
        self.rate = rate
        self.short_term = short_term

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class BinomialModel(ABC):
    """
    Abstract class for any Binomial Model.
    All classes that inherit from BinomialModel must implement
    stock_tree(), payoff(), derivative_tree(), and price() methods.
    """

    def __init__(self, s0, K, T, u, d, r, n_periods, option):
        """
        :param s0: initial stock price
        :param K: strike price
        :param T: duration
        :param u: up-factor
        :param d: down-factor
        :param r: interest rate, must be an InterestRate object
        :param n_periods: height of the binomial tree
        :param option: 'put' or 'call'
        """
        self.s0 = s0
        self.K = K
        self.T = T
        self.u = u
        self.d = d
        self.r = r
        self.n = n_periods
        self.option = option
        self.compute_dt()
        self.compute_probabilities()

    def compute_dt(self):
        """
        First checks if the given interest rate is short_term. If that's the case,
        ∆T is 1 and there is no need to compute it.

        :return: delta T (∆T)
        """
        if self.r.short_term:
            self.dt = 1
        else:
            self.dt = self.T / self.n

    def compute_probabilities(self):
        self.p = (np.exp(self.r.rate * self.dt) - self.d) / (self.u - self.d)
        self.q = 1 - self.p


    @abstractmethod
    def stock_tree(self):
        """
        Computes the binomial tree of up and down stock prices.
        Use the returned tree as parameter for derivative_tree function.

        :return np array with shape (self.n + 1, self.n + 1) containing stock prices
        """
        pass

    @abstractmethod
    def payoff(self, st):
        """
        The payoff at terminal time T.

        :param st: price of stock at terminal node T
        :return: payoff at terminal node T
        """
        pass

    @abstractmethod
    def derivative_tree(self, stock_tree):
        """
        using stock_tree, computes the option price
        :param stock_tree:
        :return: np array with shape (self.n + 1, self.n + 1) containing derivative prices
        """
        pass

    @abstractmethod
    def price(self):
        """
        Using the stock_tree and derivative_tree functions,
        finds the optimal price of the option at time 0.
        :return: optimal option price at time 0
        """
        pass

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class EuropeanVanillaModel(BinomialModel):

    def stock_tree(self):
        stock_tree = np.zeros((self.n + 1, self.n + 1))
        stock_tree[0, 0] = self.s0
        for i in range(1, self.n + 1):
            stock_tree[i, 0] = stock_tree[i - 1, 0] * self.u
            for j in range(1, i + 1):
                stock_tree[i, j] = stock_tree[i - 1, j - 1] * self.d
        return stock_tree

    def payoff(self, st):
        if self.option == 'put':
            return max(self.K - st, 0)
        if self.option == 'call':
            return max(st - self.K, 0)
        raise Exception('option must be put or call, you entered:', self.option)

    def derivative_tree(self, stock_tree):
        d_tree = np.zeros((self.n + 1, self.n + 1))
        for i in range(self.n + 1):
            d_tree[self.n, i] = self.payoff(stock_tree[self.n, i])

        exp = np.exp(-1 * self.r.rate * self.dt)
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1):
                d_tree[i, j] = exp * (self.p * d_tree[i + 1, j] + self.q * d_tree[i + 1, j + 1])
        return d_tree

    def price(self):
        s_tree = self.stock_tree()
        d_tree = self.derivative_tree(s_tree)
        return d_tree[0, 0]


class AmericanModel(EuropeanVanillaModel):
    """
    Same as EuropeanVanillaModel, but need to account for early execution at each node
    when computing derivative_tree.
    """

    def derivative_tree(self, stock_tree):
        """
        American options can be executed early. At each node,
        the price of the derivative is max(vn, payoff(Sn)).
        :param stock_tree:
        :return: optimal value at t=0
        """
        d_tree = np.zeros((self.n + 1, self.n + 1))
        for i in range(self.n + 1):
            d_tree[self.n, i] = self.payoff(stock_tree[self.n, i])

        exp = np.exp(-1 * self.r.rate * self.dt)
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1):
                vn = exp * (self.p * d_tree[i + 1, j] + self.q * d_tree[i + 1, j + 1])
                early_execution = self.payoff(stock_tree[i, j])
                d_tree[i, j] = max(vn, early_execution)
        return d_tree

