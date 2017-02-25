import numpy as np
from abc import ABC, abstractmethod


class InterestRate:
    def __init__(self, rate, short_term=False):
        self.rate = rate
        self.short_term = short_term

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class BinomialModel(ABC):
    def __init__(self, s0, K, T, u, d, r, n_periods, option='put'):
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
        if self.r.short_term:
            self.dt = 1
        else:
            self.dt = self.T / self.n

    def compute_probabilities(self):
        self.p = (np.exp(self.r.rate * self.dt) - self.d) / (self.u - self.d)
        self.q = 1 - self.p

    def stock_tree(self):
        stock_tree = np.zeros((self.n + 1, self.n + 1))
        stock_tree[0, 0] = self.s0
        for i in range(1, self.n + 1):
            stock_tree[i, 0] = stock_tree[i - 1, 0] * self.u
            for j in range(1, i + 1):
                stock_tree[i, j] = stock_tree[i - 1, j - 1] * self.d
        return stock_tree

    @abstractmethod
    def payoff(self, st):
        pass

    @abstractmethod
    def derivative_tree(self, stock_tree):
        pass

    @abstractmethod
    def price(self):
        pass

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class EuropeanVanillaModel(BinomialModel):
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


def main():
    s0 = float(input('enter initial stock price s0: '))
    K = float(input('enter strike price K: '))
    T = float(input('enter time T: '))
    u = float(input('enter up factor u: '))
    d = float(input('enter down factor d: '))
    r = float(input('enter interest rate r: '))

    choice = str(input('is the interest rate short term? (y/n)')).lower()
    while choice not in ['y', 'n']:
        print('invalid, please enter y or n')
        choice = str(input('is the interest rate short term? (y/n)')).lower()

    flag = True if choice == 'n' else False

    i_rate = InterestRate(r, short_term=flag)
    n = int(input('the number of periods n: '))
    option = str(input('put or call? (put/call)')).lower()
    while option not in ['put', 'call']:
        print('invalid, please enter put or call')
        option = str(input('put or call? (put/call)'))

    european = EuropeanVanillaModel(s0, K, T, u, d, i_rate, n, option=option)
    print('optimal price is: ', european.price())

if __name__ == '__main__':
    main()

r = InterestRate(0.12, short_term=False)
european_call = EuropeanVanillaModel(20, 21, .5, 1.1, .9, r, n_periods=2, option='call')
european_call.price()

r = InterestRate(0.04, short_term=True)
european_put = EuropeanVanillaModel(80, 100, 2, 1.2, .8, r, 2, option='put')
european_put.price()