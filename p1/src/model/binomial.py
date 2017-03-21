import numpy as np
from abc import ABC, abstractmethod


class BinomialModel(ABC):
    """
    Abstract class for any Binomial Model.
    All classes that inherit from BinomialModel must implement its methods
    """

    def __init__(self, s0, K, T, dt, u, d, r, n_steps, option):
        """
        :param s0: initial stock price
        :param K: strike price
        :param T: duration
        :param dt: delta-T (∆T)
        :param u: up-factor
        :param d: down-factor
        :param r: interest rate
        :param n_steps: height of the binomial tree, number of steps
        :param option: 'put' or 'call'
        """
        self.s0 = s0
        self.K = K
        self.T = T
        self.dt = dt
        self.u = u
        self.d = d
        self.r = r
        self.n_steps = n_steps
        self.option = option
        self.s_tree = None
        self.o_tree = None
        self.build()

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def compute_probabilities(self):
        pass

    @abstractmethod
    def compute_stock_tree(self):
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
    def compute_option_tree(self):
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
    def build(self):
        self.compute_probabilities()
        self.compute_stock_tree()
        self.compute_option_tree()

    def compute_probabilities(self):
        self.p = (np.exp(self.r * self.dt) - self.d) / (self.u - self.d)
        self.q = 1 - self.p

    def compute_stock_tree(self):
        self.s_tree = np.empty((self.n_steps + 1, self.n_steps + 1))
        self.s_tree[:] = np.nan
        self.s_tree[0, 0] = self.s0
        for i in range(1, self.n_steps + 1):
            self.s_tree[i, 0] = self.s_tree[i - 1, 0] * self.u
            for j in range(1, i + 1):
                self.s_tree[i, j] = self.s_tree[i - 1, j - 1] * self.d

    def payoff(self, st):
        if self.option == 'put':
            return max(self.K - st, 0)
        if self.option == 'call':
            return max(st - self.K, 0)
        raise ValueError('option must be put or call, you entered:', self.option)

    def compute_option_tree(self):
        self.o_tree = np.empty((self.n_steps + 1, self.n_steps + 1))
        self.o_tree[:] = np.nan
        for i in range(self.n_steps + 1):
            self.o_tree[self.n_steps, i] = self.payoff(self.s_tree[self.n_steps, i])

        exp = np.exp(-1 * self.r * self.dt)
        for i in range(self.n_steps - 1, -1, -1):
            for j in range(i + 1):
                self.o_tree[i, j] = exp * (self.p * self.o_tree[i + 1, j] + self.q * self.o_tree[i + 1, j + 1])

    def price(self):
        return self.o_tree[0, 0]


class AmericanModel(EuropeanVanillaModel):
    """
    Same as EuropeanVanillaModel, but need to account for early execution at each node
    when computing option_tree.
    """

    def compute_option_tree(self):
        """
        American options can be executed early. At each node,
        the price of the derivative is max(vn, payoff(Sn)).
        """
        self.o_tree = np.empty((self.n_steps + 1, self.n_steps + 1))
        self.o_tree[:] = np.nan
        for i in range(self.n_steps + 1):
            self.o_tree[self.n_steps, i] = self.payoff(self.s_tree[self.n_steps, i])

        exp = np.exp(-1 * self.r * self.dt)
        for i in range(self.n_steps - 1, -1, -1):
            for j in range(i + 1):
                vn = exp * (self.p * self.o_tree[i + 1, j] + self.q * self.o_tree[i + 1, j + 1])
                early_execution = self.payoff(self.s_tree[i, j])
                self.o_tree[i, j] = max(vn, early_execution)


class HullWhiteModel(ABC):
    def __init__(self, K, T, dt, r, n_steps, option, n_training, stock_prices, s0=None):
        """
            :param K: strike price
            :param T: duration
            :param dt: delta-T (∆T)
            :param r: interest rate
            :param n_steps: height of the binomial tree, number of steps
            :param option: 'put' or 'call'
            :param n_training: number of training docs
            :param stock_prices: a DataFrame containing stock prices with computed ratios
        """
        self.s0 = s0
        self.K = K
        self.T = T
        self.dt = dt
        self.r = r
        self.n_steps = n_steps
        self.option = option
        self.n_training = n_training
        self.stock_prices = stock_prices
        self.binomial = None
        self.build()

    def compute_factors(self):
        self.mean = np.nanmean(self.stock_prices['Ratio'][:self.n_training])
        self.sigma = np.nanstd(self.stock_prices['Ratio'][:self.n_training])
        U = self.mean - 1
        self.u = 1 + (U * self.dt) + (self.sigma * np.sqrt(self.dt))
        self.d = 1 + (U * self.dt) - (self.sigma * np.sqrt(self.dt))

    def price(self):
        return self.binomial.price()

    @abstractmethod
    def build(self):
        pass


class HullWhiteEuropeanModel(HullWhiteModel):
    def build(self):
        if self.s0 is None:
            if self.n_training < len(self.stock_prices['Close']):
                self.s0 = self.stock_prices['Close'][self.n_training]
            else:
                raise IndexError('Could not assign s0 to first non training stock price')

        self.compute_factors()
        self.binomial = EuropeanVanillaModel(
            self.s0, self.K, self.T, self.dt, self.u, self.d, self.r, self.n_steps, self.option)


class HullWhiteAmericanModel(HullWhiteModel):
    def build(self):
        if self.s0 is None:
            if self.n_training < len(self.stock_prices['Close']):
                self.s0 = self.stock_prices['Close'][self.n_training]
            else:
                raise IndexError('Could not assign s0 to first non training stock price')
        self.compute_factors()
        self.binomial = AmericanModel(
            self.s0, self.K, self.T, self.dt, self.u, self.d, self.r, self.n_steps, self.option)
