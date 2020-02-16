function [d,t] = lab1_code1(np,nd)
    if (nargin < 1), np = 1e7; nd = 10;
    A = randn(np,nd); B = randn(np,nd); end
    d = zeros(np,1);
    tic;
    for i = 1:np
        for j = 1:nd
            d(i) = d(i) + (B(i,j)-A(i,j)).^2;
        end
        d(i) = sqrt(d(i));
    end
    toc;