function res = ParseFilename(fname, varargin)
    % This function takes in filenames for the voluntary reflex project
    % with the formats
    %   Patient1_MVC_DF.txt
    %   PatNo1_VR_AnklePosNeutral_DF_1-00Hz_Trial1.txt
    % An optional addition argument is a file path
    
    res = struct; % create result struct

    % Determine if its an MVC or Voluntary Reflex (VR) file
    ismvc = ~isempty(strfind(fname, 'MVC'));
    isvr = ~isempty(strfind(fname, 'VR'));

    if ismvc
        res = ParseMvcFilename(fname); 
    elseif isvr
        res = ParseVrFilename(fname);
    end

    % add path if its given
    if nargin == 2 
        res.path = varargin{1};
    end
end