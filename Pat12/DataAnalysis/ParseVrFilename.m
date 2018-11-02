function res = ParseVrFilename(fname)
    % This function takes in filenames for the voluntary reflex project
    % with the formats
    %   PatNo1_VR_AnklePosNeutral_DF_1-00Hz_Trial1.txt
    % and returns a struct with file info
    
    res = struct; % create result struct
    res.filename = fname;
    
    % remove file extension
    extensionstartchar = '.';
    extensionstartind = strfind(fname, extensionstartchar);
    fnamefull = fname;
    fname = fname(1:extensionstartind-1);
    
    % split filename string parts
    fnamestruct = strsplit(fname, '_');
    res.patno = str2num(fnamestruct{1}(6:end));
    res.filetype = fnamestruct{2};
    res.flexion = fnamestruct{4};
    res.anklepos = fnamestruct{3}(9:end);
    
    % reference signal info
    if contains(fnamestruct{5}, 'Hz')
        res.refsigtype = 'sine';
        hzind = strfind(fnamestruct{5}, 'Hz');
        freqstr = fnamestruct{5}(1:hzind-1);
        freqstr = strrep(freqstr, '-', '.');
        res.refsigfreq = str2num(freqstr);
        res.samplesperperiod = 1000/res.refsigfreq;
    elseif contains(fnamestruct{5}, 'PRBS')
        res.sigtype = 'PRBS';
    elseif contains(fnamestruct{5}, 'Step')
        res.sigtype = 'Step';
    elseif contains(fnamestruct{5}, 'Other')
        res.sigtype = 'Other';
    end
    
    % trial info
    if length(fnamestruct) == 6
        res.trialno = str2num(fnamestruct{6}(6:end));
    else
        res.trialno = 0;
    end
    
end