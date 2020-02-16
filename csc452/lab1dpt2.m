function [t] = lab1dpt2(np,nd,nl)
if (nargin < 1); np = 1e5; nd = 2; nl = 2; end

hp = gcp('nocreate');
if isempty(hp), hp = parpool(nl); end

tic;
spmd
    nppl = floor(np/nl); % points per lab
    nplo = np - nl*nppl; % no of points left over
    
    if (labindex == 1)
        nptl = nppl + nplo; % points for this lab
    else
        nptl = nppl;
    end
    
    A = randn(nptl,nd); B = randn(nptl,nd);   
    d = zeros(nptl,1);


   
    for i = 1:np/nptl
        for j = 1:nd
            d(i) = d(i) + (B(i,j)-A(i,j)).^2;
        end
        d(i) = sqrt(d(i));
    end
    
    da = gcat(d,1,1);
    
end

t = toc;
d1 = da{1};
delete(hp);
