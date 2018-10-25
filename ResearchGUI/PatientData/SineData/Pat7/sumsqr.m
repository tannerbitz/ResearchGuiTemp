function SE  = sumsqr(m)
    SE = 0;
    for i = 1:length(m)
        SE = SE + m(i)^2;
    end
end