function[t] = lab1a(np,nd);
% checks if the number of arguments is less than 1. if so, gives the
% missing arguments values.
if (nargin < 1), np = 1e3; nd = 2; end
% random a and b vector initialization
A = randn(np,nd); B = randn(np,nd);
% the output vector that has the euclidean distance
C = zeros(np,1);

tic;
for i = 1:np
    for j = 1:nd
        C(i) = C(i) + (B(i,j)-A(i,j)).^2;
    end
    C(i) = sqrt(C(i));
end
toc;