function [t] = lab1f(np,nd)
if (nargin < 1); np = 1e5; nd = 2; nw=1; end
hp = gcp('nocreate');
if isempty(hp), hp=parpool(nw); end
aA = randn(np,nd); aB = randn(np,nd);
dA = distributed(aA); dB = distributed(aB);
d = zeros(np,1);
tic;
dc = sqrt(sum((dA-dB).^2,2));
c = gather(dc);
t = toc;

delete(hp);