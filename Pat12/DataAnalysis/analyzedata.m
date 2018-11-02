function res = analyzedata()
    close all;
    clear all;
    clc;
    
    % Choose MVC MAT Files. We will get the PF and DF MVC Values which were
    % calculated and saved in this mat file.
    [mvcfile, mvcpath] = uigetfile('.mat', ...
                                    'Choose MVC MAT Files', ...
                                    'MultiSelect', 'on');
    load(fullfile(mvcpath, mvcfile), 'DF', 'PF');
    mvcpf = PF;
    mvcdf = DF;
    
    
    refchannel = 2;
    measchannel = 1;

    % Choose Trial File
    [trialfile, trialpath] = uigetfile('.txt', ...
                                    'Choose MVC Files', ...
                                    'MultiSelect', 'off');
                              
    trialstruct = ParseFilename(trialfile, trialpath);
    data = load(fullfile(trialpath, trialfile));
    refdata = data(:,refchannel);
    measdata = data(:, measchannel);
    zerolevel = mean(measdata(1:5000));
    measdata = measdata - zerolevel;
    
    % Take last cycle of refdata and find where it is zero (or at least
    % minimum).  This spot will be assumed to be 3/4 of a period ahead of
    % the start/stop of each trial period.  
    reflastperiod = refdata(end-ceil(trialstruct.samplesperperiod):end);
    periodmin = min(reflastperiod);
    minindices = find(reflastperiod==periodmin);
%     minindices = find(minindices > minindices(end) - trialstruct.samplesperperiod/2);
    minind = round(mean(minindices));
    minind = length(measdata) - (length(reflastperiod) - minind);
    
    zeroind = minind - 3/4*round(trialstruct.samplesperperiod);

    
    % Gather data into cycles
    numcycles = 20;
    cycles = zeros(numcycles, floor(trialstruct.samplesperperiod));
    startind = zeroind;
    for i = 1:numcycles
        actualind = zeroind - trialstruct.samplesperperiod*i;
        startind = startind - floor(trialstruct.samplesperperiod);
        stopind = startind + floor(trialstruct.samplesperperiod) - 1;
        inddiff = actualind - startind;
        if inddiff < -1
            startind = startind -1;
            stopind = stopind -1;
        end
        cycles(numcycles+1-i, :) = measdata(startind:stopind);
        refcycles(numcycles+1-i, :) = refdata(startind:stopind);
    end
    
    % Find mean and std deviation of cycles
    nomcycle = zeros(1, floor(trialstruct.samplesperperiod));
    stdcycle = zeros(1, floor(trialstruct.samplesperperiod));
    
    for i = 1:floor(trialstruct.samplesperperiod)
        nomcycle(i) = mean(cycles(:, i));
        stdcycle(i) = std(cycles(:, i));
    end
    lowerbound = nomcycle - 3*stdcycle;
    upperbound = nomcycle + 3*stdcycle;
    
    % Only keep data if all data points are within 3 std deviations of
    % mean
    k = 1;
    cycleslost = [];
    for j = 1:numcycles
        keepcycle = true;
        for i = 1:floor(trialstruct.samplesperperiod)
            if cycles(j, i) >= upperbound(i) || cycles(j, i) <= lowerbound(i)
                keepcycle = false;
                cycleslost(end + 1) = j;
                break
            end
        end
        if keepcycle
            validcycles(k, :) = cycles(j, :);
            validrefcycles(k, :) = refcycles(j, :);
            k = k + 1;
        end
    end
    
    % recalculate nominal measured and reference cycles
    for i = 1:floor(trialstruct.samplesperperiod)
        nommeascycle(i) = mean(validcycles(:, i));
        nomrefcycle(i) = mean(validrefcycles(:,i));
    end
    
    % Normalize to MVC
    res2lbs = 250/4096;
    lbs2newtons =  4.44822;
    armlength = 0.15; % meters
    percentmvc = 0.3;
    
    if strcmp(trialstruct.flexion, 'DF')
        minrefval = 0;
        maxrefval = percentmvc*mvcdf;
        refsigspan = maxrefval - minrefval;
        nomrefcycle_nm = minrefval + nomrefcycle/4096*refsigspan;
    elseif strcmp(trialstruct.flexion, 'PF')
        minrefval = -percentmvc*mvcpf;
        maxrefval = 0;
        refsigspan = maxrefval - minrefval;
        nomrefcycle_nm = minrefval + nomrefcycle/4096*refsigspan;
    end
    
    nommeascycle_nm = nommeascycle*res2lbs*lbs2newtons*armlength;

    res = [nomrefcycle_nm; nommeascycle_nm];
    
    %     [M, I] = max(nommeascycle_nm);
%        
%     
%     close all
%     figure(1)
%     plot(nomrefcycle_nm);
%     hold on
%     plot(nommeascycle_nm);
%     legend('ref', 'meas')
%     plot(I, M, 'r*')
%     hold off

end