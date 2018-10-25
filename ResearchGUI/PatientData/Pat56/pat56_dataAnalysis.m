%% import data
patientnumber = {'7'};
mvcpf_filename = strcat('Patient', patientnumber, '_MVC_PF.txt');
mvcdf_filename = strcat('Patient', patientnumber , '_MVC_DF.txt');
volreflex_filename = strcat('PatNo', patientnumber', '_VR_AnklePosNeutral_DFPF_0-25Hz.txt');

mvcpfdata = load(mvcpf_filename{1});
mvcdfdata = load(mvcdf_filename{1});
vrdata = load(volreflex_filename{1});

%process filename
mvcdffilenamearray = removeextension(mvcdf_filename);
mvcpffilenamearray = removeextension(mvcpf_filename);

volreflexfilenamearray = removeextension(volreflex_filename);
mvcdffilenamearray = split(mvcdffilenamearray, '_');
mvcpffilenamearray = split(mvcpffilenamearray, '_');
volreflexfilenamearray = split(volreflexfilenamearray, '_');

flexion = volreflexfilenamearray{4};

% initialize constants
serial2NmBipolar = 125/2048*4.448*.15;
serial2NmUnipolar = 0;
percentmvc = 0.20;
%%
% Define ref and meas channels
refchan = 2;
measchan = 1;

% Get all pf and df mvc data measurement
mvcpfmeas = mvcpfdata(:,measchan);
mvcdfmeas = mvcdfdata(:,measchan);

% rest1         0 - 5s
% mvc1          5 - 10s 
% rest2         10 - 25s
% mvc2          25 - 30s
% rest3         30 - 45s
% mvc3          45 - 50s

%split into sections --- Plantarflexion
mvcpf3 = mvcpfmeas(end-5000: end);
restpf3 = mvcpfmeas(end-20000: end - 5000);
mvcpf2 = mvcpfmeas(end - 25000: end - 20000);
restpf2 = mvcpfmeas(end - 40000: end - 25000);
mvcpf1 = mvcpfmeas(end - 45000: end - 40000);
restpf1 = mvcpfmeas(1: end - 45000);


% cut off ends of data
indexes2cut = 700;
mvcpf3  =  mvcpf3(indexs2cut: end-indexs2cut);
mvcpf2  =  mvcpf2(indexs2cut: end-indexs2cut);
mvcpf1  =  mvcpf1(indexs2cut: end-indexs2cut);
restpf3 = restpf3(indexs2cut: end-indexs2cut);
restpf2 = restpf2(indexs2cut: end-indexs2cut);
restpf1 = restpf1(indexs2cut: end-indexs2cut);

zero3 = mean(restpf3);
zero2 = mean(restpf2);
zero1 = mean(restpf1);
mvcpf3val = min(mvcpf3) - zero3;
mvcpf2val = min(mvcpf2) - zero2;
mvcpf1val = min(mvcpf1) - zero1;


%split into sections --- Dorsiflexion
mvcdf3 = mvcdfmeas(end-5000: end);
restdf3 = mvcdfmeas(end-20000: end - 5000);
mvcdf2 = mvcdfmeas(end - 25000: end - 20000);
restdf2 = mvcdfmeas(end - 40000: end - 25000);
mvcdf1 = mvcdfmeas(end - 45000: end - 40000);
restdf1 = mvcdfmeas(1: end - 45000);

% cut off ends of data
mvcdf3  =  mvcdf3(indexs2cut: end-indexs2cut);
mvcdf2  =  mvcdf2(indexs2cut: end-indexs2cut);
mvcdf1  =  mvcdf1(indexs2cut: end-indexs2cut);
restdf3 = restdf3(indexs2cut: end-indexs2cut);
restdf2 = restdf2(indexs2cut: end-indexs2cut);
restdf1 = restdf1(indexs2cut: end-indexs2cut);

zero3 = mean(restdf3);
zero2 = mean(restdf2);
zero1 = mean(restdf1);
mvcdf3val = max(mvcdf3) - zero3;
mvcdf2val = max(mvcdf2) - zero2;
mvcdf1val = max(mvcdf1) - zero1;

% mvc values
mvcpfval = min([mvcpf3val, mvcpf2val, mvcpf1val])*serial2NmBipolar;
mvcdfval = max([mvcdf3val, mvcdf2val, mvcdf1val])*serial2NmBipolar;
mvcdfpfval = mean([abs(mvcpfval), abs(mvcdfval)]);

%% Voluntary Reflex Analysis
[rows,cols] = size(vrdata);
vrtrialdata = vrdata(rows-60000:rows, 1:cols);
vrrestdata = vrdata(1:rows-60000, 1:cols);

% calculate zero
vrrestmeas = vrrestdata(:,measchan);
vrzero = mean(vrrestmeas);

% get trial data
vrtrialref = vrtrialdata(:,refchan);
vrtrialmeas = (vrtrialdata(:, measchan) - vrzero)*serial2NmBipolar;


if (strcmp(flexion,'DFPF'))
    % PRBS signal so "filter" it
    vrtrialreffiltered = zeros(size(vrtrialref));
    for i = 1:length(vrtrialref)
        if vrtrialref(i) < 2048
            vrtrialreffiltered(i) = -percentmvc*mvcdfpfval;
        else
            vrtrialreffiltered(i) = percentmvc*mvcdfpfval;
        end
    end
elseif (strcmp(flexion,'PF'))
    vrtrialreffiltered = percentmvc*mvcpfval - vrtrialref*(percentmvc*mvcpfval)/4095;
elseif (strcmp(flexion,'DF'))
    vrtrialreffiltered = vrtrialref*(percentmvc*mvcdfval)/4095;
end


t = [0:length(vrtrialmeas)-1]*0.001;

figure(1)
hold on
plot(t, vrtrialmeas);
plot(t, vrtrialreffiltered);
title('PRBS - Dorsiflexion-Plantarflexion Tsw = 750ms');
xlabel('Time (s)');
ylabel('Torque (Nm)');
hold off

%% Plot standard deviation 
vrrestmeas = vrrestdata(:, measchan);
stdvec = zeros(size(vrrestmeas));
for i = 1:length(vrrestmeas)
    stdvec(i) = std(vrrestmeas(i:end));
end

plot(stdvec)
