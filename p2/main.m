% (a) Fix T = 2, r = 0.05, ? = 0.25, 
% and vary the strike K ? [60,180] with step size 2. 
% Plot the graph ?strike vs price? for both sets of options.

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

figure('Name', 'strike vs put price')
plot(puts, K)

K = 120;
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

figure('Name', 'maturity vs put price')
plot(puts, T)

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

figure('Name', 'volatility vs put price')
plot(puts, sigma)

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

figure('Name', 'interest rate vs put price')
plot(puts, r)

