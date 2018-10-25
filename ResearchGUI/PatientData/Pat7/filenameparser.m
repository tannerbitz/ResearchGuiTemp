function r = filenameparser(fname)
    fname = removeextension(fname);
    fnameparts = split(fname, '_');
    r = fnameparts;
    temp = struct;
    
    temp.patno = getPatNumber(fnameparts{1});
    temp.filetype = fnameparts{2};
    if strcmp(temp.filetype, 'MVC')
        whatever = 0;
        
    elseif strcmp(temp.filetype,'VR')
        temp.anklepos = fnameparts{3};
        temp.flexion = fnameparts{4};
        
            
    end
end