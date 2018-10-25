%% Patient 7 -- 1/2 Hz, initial data loading

clear;
clc;

P7mvcDF = load('Patient7_MVC_DF.txt'); % Loading Pat7 MVC DF data
P7mvcPF = load('Patient7_MVC_PF.txt'); % Loading Pat 7 MVC PF data

P7halfDF = load('PatNo7_VR_AnklePosNeutral_DF_0-50Hz.txt'); % patient-hz-DF or PF
P7halfPF = load('PatNo7_VR_AnklePosNeutral_PF_0-50Hz.txt');
P7halfDFPF = load('PatNo7_VR_AnklePosNeutral_DFPF_0-50Hz.txt');

%% Calling reference and measured vectors

mvcDF_measured = P7mvcDF(:,1); % calling DF MVC data for Pat7
mvcPF_measured = P7mvcPF(:,1); % calling PF MVC data for Pat8

P7halfDF_m = P7halfDF(:,1); % column 1 is measured
P7halfDF_ref = P7halfDF(:,2); % column 2 is reference
P7halfPF_m = P7halfPF(:,1);
P7halfPF_ref = P7halfPF(:,2);
P7halfDFPF_m = P7halfDFPF(:,1);
P7halfDFPF_ref = P7halfDFPF(:,2);

%% Determining zero level

zerolvlhalfDF = min(P7halfDF_m(1:4500));
P7halfDF_m = P7halfDF_m - zerolvlhalfDF;

zerolvlhalfPF = min(P7halfPF_m(1:4500));
P7halfPF_m = P7halfPF_m - zerolvlhalfPF;

zerolvlhalfDFPF = min(P7halfDFPF_m(1:4500));
P7halfDFPF_m = P7halfDFPF_m - zerolvlhalfDFPF;

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

refsigserial2NmDF = mvcDF_Nm/4096*0.2;
refsigserial2NmPF = mvcPF_Nm/4096*0.2;

clear figures;
figure(1)
title('1/2 Hertz DF');
hold on;
plot(P7halfDF_ref*refsigserial2NmDF);
plot(P7halfDF_m*serial2lbs_bipolar*lbs2NmAt15cm-1.25); % minus 1.25 fudge factor??
hold off;

figure(2)
title('1/2 Hertz PF');
hold on;
plot(P7halfPF_ref*refsigserial2NmPF);
plot(P7halfPF_m*serial2lbs_bipolar*lbs2NmAt15cm+4); % plus 4 fudge factor??
hold off;





