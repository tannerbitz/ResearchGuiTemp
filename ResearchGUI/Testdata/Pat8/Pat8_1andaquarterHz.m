%% Patient 8 -- 1.25 Hz, initial data loading

clear;
clc;

P8mvcDF = load('Patient8_MVC_DF.txt'); % Loading Pat 8 MVC DF data
P8mvcPF = load('Patient8_MVC_PF.txt'); % Loading Pat 8 MVC PF data

P8one25DF = load('PatNo8_VR_AnklePosNeutral_DF_1-25Hz.txt'); % patient-hz-DF or PF
P8one25PF = load('PatNo8_VR_AnklePosNeutral_PF_1-25Hz.txt');
P8one25DFPF = load('PatNo8_VR_AnklePosNeutral_DFPF_1-25Hz.txt');

%% Calling reference and measured vectors

mvcDF_measured = P8mvcDF(:,1); % calling DF MVC data for Pat8
mvcPF_measured = P8mvcPF(:,1); % calling PF MVC data for Pat8

P8one25DF_m = P8one25DF(:,1); % column 1 is measured
P8one25DF_ref = P8one25DF(:,2); % column 2 is reference
P8one25PF_m = P8one25PF(:,1);
P8one25PF_ref = P8one25PF(:,2);
P8one25DFPF_m = P8one25DFPF(:,1);
P8one25DFPF_ref = P8one25DFPF(:,2);

%% Determining zero level

zerolvlone25DF = min(P8one25DF_m(1:4500));
P8one25DF_m = P8one25DF_m - zerolvlone25DF;

zerolvlone25PF = min(P8one25PF_m(1:4500));
P8one25PF_m = P8one25PF_m - zerolvlone25PF;

zerolvlone25DFPF = min(P8one25DFPF_m(1:4500));
P8one25DFPF_m = P8one25DFPF_m - zerolvlone25DFPF;

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
title('1.25 Hertz DF');
hold on;
plot(P8one25DF_ref*refsigserial2NmDF);
plot(P8one25DF_m*serial2lbs_bipolar*lbs2NmAt15cm);
hold off;

figure(2)
title('1.25 Hertz PF');
hold on;
plot(P8one25PF_ref*refsigserial2NmPF);
plot(P8one25PF_m*serial2lbs_bipolar*lbs2NmAt15cm+3); % plus 3 fudge factor??
hold off;





