from model.binomial import EuropeanVanillaModel


def main():
    s0 = float(input('enter initial stock price s0: '))
    K = float(input('enter strike price K: '))
    T = float(input('enter time T: '))
    dt = float(input('enter delta-t ∆T: '))
    u = float(input('enter up factor u: '))
    d = float(input('enter down factor d: '))
    r = float(input('enter interest rate r: '))
    n = int(input('the number of steps n: '))

    option = str(input('put or call? (put/call)')).lower()
    while option not in ['put', 'call']:
        print('invalid, please enter put or call')
        option = str(input('put or call? (put/call)'))

    european = EuropeanVanillaModel(s0, K, T, dt, u, d, r, n, option)
    print('stock tree: \n', european.s_tree.T)
    print('option tree: \n', european.o_tree.T)
    print('optimal price is: ', european.price())


if __name__ == '__main__':
    main()