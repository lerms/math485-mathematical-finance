import numpy as np
from abc import ABC, abstractmethod


class BinomialModel(ABC):
    """
    Abstract class for any Binomial Model.
    All classes that inherit from BinomialModel must implement
    self.stock_tree(), self.payoff(), self.option_tree(), and self.price() methods.
    """

    def __init__(self, s0, K, T, dt, u, d, r, n, option):
        """
        :param s0: initial stock price
        :param K: strike price
        :param T: duration
        :param dt: delta-T (∆T)
        :param u: up-factor
        :param d: down-factor
        :param r: interest rate
        :param n: height of the binomial tree, number of steps
        :param option: 'put' or 'call'
        """
        self.s0 = s0
        self.K = K
        self.T = T
        self.dt = dt
        self.u = u
        self.d = d
        self.r = r
        self.n = n
        self.option = option
        self.compute_probabilities()
        self.stock_tree()
        self.option_tree()

    def compute_probabilities(self):
        self.p = (np.exp(self.r * self.dt) - self.d) / (self.u - self.d)
        self.q = 1 - self.p


    @abstractmethod
    def stock_tree(self):
        """
        Computes the binomial tree of up and down stock prices.
        Use the returned tree as parameter for option_tree function.

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
    def option_tree(self):
        """
        using self.stock_tree, computes the option price
        :param self.stock_tree:
        :return: np array with shape (self.n + 1, self.n + 1) containing derivative prices
        """
        pass

    @abstractmethod
    def price(self):
        """
        Using the computed self.stock_tree and option_tree,
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
        self.s_tree = np.empty((self.n + 1, self.n + 1))
        self.s_tree[:] = np.nan
        self.s_tree[0, 0] = self.s0
        for i in range(1, self.n + 1):
            self.s_tree[i, 0] = self.s_tree[i - 1, 0] * self.u
            for j in range(1, i + 1):
                self.s_tree[i, j] = self.s_tree[i - 1, j - 1] * self.d

    def payoff(self, st):
        if self.option == 'put':
            return max(self.K - st, 0)
        if self.option == 'call':
            return max(st - self.K, 0)
        raise Exception('option must be put or call, you entered:', self.option)

    def option_tree(self):
        self.o_tree = np.empty((self.n + 1, self.n + 1))
        self.o_tree[:] = np.nan
        for i in range(self.n + 1):
            self.o_tree[self.n, i] = self.payoff(self.s_tree[self.n, i])

        exp = np.exp(-1 * self.r * self.dt)
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1):
                self.o_tree[i, j] = exp * (self.p * self.o_tree[i + 1, j] + self.q * self.o_tree[i + 1, j + 1])

    def price(self):
        return self.o_tree[0,0]


class AmericanModel(EuropeanVanillaModel):
    """
    Same as EuropeanVanillaModel, but need to account for early execution at each node
    when computing option_tree.
    """

    def option_tree(self):
        """
        American options can be executed early. At each node,
        the price of the derivative is max(vn, payoff(Sn)).
        :param self.stock_tree:
        :return: optimal value at t=0
        """
        self.o_tree = np.empty((self.n + 1, self.n + 1))
        self.o_tree[:] = np.nan
        for i in range(self.n + 1):
            self.o_tree[self.n, i] = self.payoff(self.s_tree[self.n, i])

        exp = np.exp(-1 * self.r * self.dt)
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1):
                vn = exp * (self.p * self.o_tree[i + 1, j] + self.q * self.o_tree[i + 1, j + 1])
                early_execution = self.payoff(self.s_tree[i, j])
                self.o_tree[i, j] = max(vn, early_execution)
        return self.o_tree
