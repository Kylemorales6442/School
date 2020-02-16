function [t] = lab1a(np,nd,nw)
% Checks # of arguments in function, if less than one, initializes arguments
% to default value.
if (nargin < 1); np = 1e7; nd = 2; nw=2; end
% HP is a parallel pool, this line checks to see if there is a pool, and if
% there is a pool, don't create a new one.
hp = gcp('nocreate');
% This line is for if there is not a parallel pool. If there is not one, it
% creates one.
if isempty(hp), hp=parpool(nw); end
% Random vector initialization from last program.
A = randn(np,nd); B = randn(np,nd);
% Output initialization
C = zeros(np,1);

tic;
% Calculation of euclidean distance using parallel computing.
parfor i = 1:np
    for j = 1:nd
        C(i) = C(i) + (B(i,j)-A(i,j)).^2;
    end
    C(i) = sqrt(C(i));
end
t = toc;
% Deletion of the parallel pool.

delete(hp);