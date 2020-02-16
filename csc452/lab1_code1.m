np = 1e6; nd = 2;
A = randn(np,nd); B = randn(np,nd);
d = randn(np,1);
for i = 1:np
    d(i) = (B(i,1)-A(i,1)).^2 + (B(i,2)-A(i,2)).^2;
    d(i) = sqrt(d(i));
end