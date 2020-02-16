np = 1e7; nd = 10; n1 = 8;
tic;
spmd
    A = randn(np/nl,nd); B = randn(np/nl,nd);
    d = zeros(np/n1,1);
    for i = 1:np/8
        for j = 1:nd
            d(i) = d(i) + (B(i,j)-A(i,j)).^2;
        end
        d(i) = sqrt(d(i));
    end
    da = gcat(d,1,1);
end
t = toc;
d1 = da{1};