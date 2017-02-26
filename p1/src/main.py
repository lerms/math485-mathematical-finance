from model.binomial import InterestRate, EuropeanVanillaModel


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