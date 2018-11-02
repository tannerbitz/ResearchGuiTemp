function res = ParseMvcFilename(fname)
    % This function takes in filenames for the voluntary reflex project
    % with the formats
    %   Patient1_MVC_DF.txt
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
    res.patno = str2num(fnamestruct{1}(8:end));
    res.filetype = fnamestruct{2};
    res.flexion = fnamestruct{3};
    
end