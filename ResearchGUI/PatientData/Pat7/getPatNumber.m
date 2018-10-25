function patno = getPatNumber(patNoStr)
    i = length(patNoStr);
    
    [num, status] = str2num(patNoStr(i));
    while (status == 1 && i > 0)
        tempStr = patNoStr(i:end);
        i = i - 1;
        [num, status] = str2num(patNoStr(i));
    end
    patno = str2num(tempStr);
end