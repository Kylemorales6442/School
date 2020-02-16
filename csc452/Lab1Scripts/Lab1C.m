% LONI runtime script
for k = 1:10
    [~,t(k)] = LabScript2(1e7,10,k);
disp(t(k));
end