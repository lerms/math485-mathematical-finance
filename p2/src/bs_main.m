% Alexander Lerma
% Math 485

% 1. Write a code (preferable in Matlab) that will compute the price of a
% call option, and a put option, in the Black-Scholes-Merton setup. Attach
% a printed version of the code at the end of the report. Using these code,
% take fixed S0 = 120, and compute the prices for calls and puts as
% follows.

% (a) Fix T = 2, r = 0.05, ? = 0.25, and vary the strike K ? [60,180] with
% step size 2. Plot the graph ?strike vs price? for both sets of options.

s0 = 120;
T = 2;
r = 0.05;
sigma = 0.25;
K = 60:2:180;
calls = NaN([1 length(K)]);
puts = NaN([1 length(K)]);
i = 1;
for k = K
    [calls(i), puts(i)] = black_scholes(s0, T, k, r, sigma);
    i = i + 1;
end

figure('Name', 'strike vs call price')
plot(calls, K)
title('strike vs call price');
xlabel('call price');
ylabel('strike price');


figure('Name', 'strike vs put price')
plot(puts, K)
title('strike vs put price');
xlabel('put price');
ylabel('strike price');

% (b) Fix K = 120, r = 0.05, ? = 0.25, and vary the maturity T ? [0.25, 4]
% with step size 1/12. Plot the graph ?maturity vs price? for both sets of
% options.

K = 120;
r = 0.05;
sigma = 0.25;
T = 0.25:1/12:4;
calls = NaN([1 length(T)]);
puts = NaN([1 length(T)]);
i = 1;
for t = T
    [calls(i), puts(i)] = black_scholes(s0, t, K, r, sigma);
    i = i + 1;
end

figure('Name', 'maturity vs call price')
plot(calls, T)
title('maturity vs call price');
xlabel('call price');
ylabel('maturity');

figure('Name', 'maturity vs put price')
plot(puts, T)
title('maturity vs put price');
xlabel('put price');
ylabel('maturity');

% (c) Fix K = 120, T = 2, r = 0.05, and vary the volatility ? ? [0.01, 0.5]
% with step size 0.01. Plot the graph ?volatility vs price? for both sets
% of options.

K = 120;
r = 0.05;
T = 2;
sigma = 0.01:0.01:0.5;
calls = NaN([1 length(sigma)]);
puts = NaN([1 length(sigma)]);
i = 1;
for sgma = sigma
    [calls(i), puts(i)] = black_scholes(s0, T, K, r, sgma);
    i = i + 1;
end

figure('Name', 'volatility vs call price')
plot(calls, sigma)
title('volatility vs call price');
xlabel('call price');
ylabel('maturity');

figure('Name', 'volatility vs put price')
plot(puts, sigma)
title('volatility vs put price');
xlabel('put price');
ylabel('maturity');


% (d) Fix K = 120, T = 2, ? = 0.25, and vary the interest rate r ? [0.01,
% 0.1] with step size 0.005. Plot the graph ?interest rate vs price? for
% both sets of options.

K = 120;
T = 2;
sigma = 0.25;
r = 0.01: 0.005: 0.1;
calls = NaN([1 length(r)]);
puts = NaN([1 length(r)]);
i = 1;
for rate = r
    [calls(i), puts(i)] = black_scholes(s0, T, K, rate, sigma);
    i = i + 1;
end

figure('Name', 'interest rate vs call price')
plot(calls, r)
title('interest rate vs call price');
xlabel('call price');
ylabel('iterest rate');


figure('Name', 'interest rate vs put price')
plot(puts, r)
title('interest rate vs put price');
xlabel('put price');
ylabel('iterest rate');

