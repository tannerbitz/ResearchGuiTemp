%% Patient 8 -- 2 Hz, initial data loading

clear;
clc;

P8mvcDF = load('Patient8_MVC_DF.txt'); % Loading Pat 8 MVC DF data
P8mvcPF = load('Patient8_MVC_PF.txt'); % Loading Pat 8 MVC PF data

P8twoDF = load('PatNo8_VR_AnklePosNeutral_DF_2-0Hz.txt'); % patient-hz-DF or PF
P8twoPF = load('PatNo8_VR_AnklePosNeutral_PF_2-0Hz.txt');
P8twoDFPF = load('PatNo8_VR_AnklePosNeutral_DFPF_2-0Hz.txt');

%% Calling reference and measured vectors

mvcDF_measured = P8mvcDF(:,1); % calling DF MVC data for Pat8
mvcPF_measured = P8mvcPF(:,1); % calling PF MVC data for Pat8

P8twoDF_m = P8twoDF(:,1); % column 1 is measured
P8twoDF_ref = P8twoDF(:,2); % column 2 is reference
P8twoPF_m = P8twoPF(:,1);
P8twoPF_ref = P8twoPF(:,2);
P8twoDFPF_m = P8twoDFPF(:,1);
P8twoDFPF_ref = P8twoDFPF(:,2);

%% Determining zero level

zerolvltwoDF = min(P8twoDF_m(1:4500));
P8twoDF_m = P8twoDF_m - zerolvltwoDF;

zerolvltwoPF = min(P8twoPF_m(1:4500));
P8twoPF_m = P8twoPF_m - zerolvltwoPF;

zerolvltwoDFPF = min(P8twoDFPF_m(1:4500));
P8twoDFPF_m = P8twoDFPF_m - zerolvltwoDFPF;

%% Zero level DF

zerolevel1DF = round(mean(mvcDF_measured(1:4500)));
mvcDF1 = max(mvcDF_measured(5500:9500)) - zerolevel1DF;
zerolevel2DF = round(mean(mvcDF_measured(10500:24500)));
mvcDF2 = max(mvcDF_measured(25500:29500)) - zerolevel2DF;
zerolevel3DF = round(mean(mvcDF_measured(30500:44500)));
mvcDF3 = max(mvcDF_measured(45550:end)) - zerolevel3DF;

%% Zero level PF

zerolevel1PF = round(mean(mvcPF_measured(1:4500)));
mvcPF1 = min(mvcPF_measured(5500:9500)) - zerolevel1PF;
zerolevel2PF = round(mean(mvcPF_measured(10500:24500)));
mvcPF2 = min(mvcPF_measured(25500:29500)) - zerolevel2PF;
zerolevel3PF = round(mean(mvcPF_measured(30500:44500)));
mvcPF3 = min(mvcPF_measured(45550:end)) - zerolevel3PF;

%% Zero level DFPF


%% Plotting

serial2lbs_bipolar = 125/2048;
lbs2NmAt15cm = 4.448*.15;

mvcDF_serial = max([mvcDF1, mvcDF2, mvcDF3]);
mvcDF_Nm = abs(mvcDF_serial)*serial2lbs_bipolar*lbs2NmAt15cm;

mvcPF_serial = min([mvcPF1, mvcPF2, mvcPF3]);
mvcPF_Nm = abs(mvcPF_serial)*serial2lbs_bipolar*lbs2NmAt15cm;

DFPFmax = max(P8twoDFPF(:,2));
DFPFmin = min(P8twoDFPF(:,2));
DFPFzero = (DFPFmax+DFPFmin)/2;

refsigserial2NmDF = mvcDF_Nm/4096*0.2;
refsigserial2NmPF = mvcPF_Nm/4096*0.2;
refsigserial2NmDFPF =0.002;

clear figures;
figure(1)
title('2 Hertz DF');
hold on;
plot(P8twoDF_ref*refsigserial2NmDF);
plot(P8twoDF_m*serial2lbs_bipolar*lbs2NmAt15cm);
hold off;

figure(2)
title('2 Hertz PF');
hold on;
plot(P8twoPF_ref*refsigserial2NmPF);
plot(P8twoPF_m*serial2lbs_bipolar*lbs2NmAt15cm+2); % plus 2 fudge factor??
hold off;

figure(3);
title('2 Hz DFPF');
hold on;
plot(P8twoDFPF_ref*refsigserial2NmDFPF);
plot(P8twoDFPF_m*serial2lbs_bipolar*lbs2NmAt15cm+4);
hold off;




