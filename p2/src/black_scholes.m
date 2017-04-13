% Alexander Lerma
% Math 485

function [ call, put ] = black_scholes(st, ttm, k, r, sigma)
% compute option price using black_scholes model
    dp = compute_d(st, ttm, k, r, sigma, 1);
    dm = compute_d(st, ttm, k, r, sigma, -1);
    expon = k * exp(-r * ttm);
    call = st * cdf(dp) - expon * cdf(dm);
    ft = st - expon;
    put = call - ft;
end

function [d] = compute_d (s, ttm, k, r, sigma, factor)
% compute d plus (factor = 1) or d minus (factor = -1)
    computed = (r + factor * (sigma ^ 2) / 2) * ttm;
    d = (log(s / k) + computed) / (sigma * sqrt(ttm));
end

function [ result ] = cdf(d)
% cumulative distribution function
    f = @(x) exp(-x.^2 / 2);
    result = (1 / sqrt(2 * pi)) * integral(f,-Inf, d);
end

