%% Patient 7 -- 1 Hz, initial data loading

clear;
clc;

P7mvcDF = load('Patient7_MVC_DF.txt'); % Loading Pat7 MVC DF data
P7mvcPF = load('Patient7_MVC_PF.txt'); % Loading Pat 7 MVC PF data

P7oneDF = load('PatNo7_VR_AnklePosNeutral_DF_1-0Hz.txt'); % patient-hz-DF or PF
P7onePF = load('PatNo7_VR_AnklePosNeutral_PF_1-0Hz.txt');
P7oneDFPF = load('PatNo7_VR_AnklePosNeutral_DFPF_1-0Hz.txt');

%% Calling reference and measured vectors

mvcDF_measured = P7mvcDF(:,1); % calling DF MVC data for Pat7
mvcPF_measured = P7mvcPF(:,1); % calling PF MVC data for Pat8

P7oneDF_m = P7oneDF(:,1); % column 1 is measured
P7oneDF_ref = P7oneDF(:,2); % column 2 is reference
P7onePF_m = P7onePF(:,1);
P7onePF_ref = P7onePF(:,2);
P7oneDFPF_m = P7oneDFPF(:,1);
P7oneDFPF_ref = P7oneDFPF(:,2);

%% Determining zero level

zerolvloneDF = min(P7oneDF_m(1:4500));
P7oneDF_m = P7oneDF_m - zerolvloneDF;

zerolvlonePF = min(P7onePF_m(1:4500));
P7onePF_m = P7onePF_m - zerolvlonePF;

zerolvloneDFPF = min(P7oneDFPF_m(1:4500));
P7oneDFPF_m = P7oneDFPF_m - zerolvloneDFPF;

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
title('1 Hertz DF');
hold on;
plot(P7oneDF_ref*refsigserial2NmDF);
plot(P7oneDF_m*serial2lbs_bipolar*lbs2NmAt15cm-1); % minus 1 fudge factor
hold off;

figure(2)
title('1 Hertz PF');
hold on;
plot(P7onePF_ref*refsigserial2NmPF);
plot(P7onePF_m*serial2lbs_bipolar*lbs2NmAt15cm+4); % plus 4 fudge factor??
hold off;





