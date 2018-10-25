%% Patient 7 -- 1/4 Hz, initial data loading

clear;
clc;

P7mvcDF = load('Patient7_MVC_DF.txt'); % Loading Pat7 MVC DF data
P7mvcPF = load('Patient7_MVC_PF.txt'); % Loading Pat 7 MVC PF data

P7quarterDF = load('PatNo7_VR_AnklePosNeutral_DF_0-25Hz.txt'); % patient-hz-DF or PF
P7quarterPF = load('PatNo7_VR_AnklePosNeutral_PF_0-25Hz.txt');
P7quarterDFPF = load('PatNo7_VR_AnklePosNeutral_DFPF_0-25Hz.txt');

%% Calling reference and measured vectors

mvcDF_measured = P7mvcDF(:,1); % calling DF MVC data for Pat7
mvcPF_measured = P7mvcPF(:,1); % calling PF MVC data for Pat8

P7quarterDF_m = P7quarterDF(:,1); % column 1 is measured
P7quarterDF_ref = P7quarterDF(:,2); % column 2 is reference
P7quarterPF_m = P7quarterPF(:,1);
P7quarterPF_ref = P7quarterPF(:,2);
P7quarterDFPF_m = P7quarterDFPF(:,1);
P7quarterDFPF_ref = P7quarterDFPF(:,2);

%% Determining zero level

zerolvlquartDF = min(P7quarterDF_m(1:4500));
P7quarterDF_m = P7quarterDF_m - zerolvlquartDF;

zerolvlquartPF = min(P7quarterPF_m(1:4500));
P7quarterPF_m = P7quarterPF_m - zerolvlquartPF;

zerolvlquartDFPF = min(P7quarterDFPF_m(1:4500));
P7quarterDFPF_m = P7quarterDFPF_m - zerolvlquartDFPF;

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

mvcDFPF_serial = (mvcDF_serial+abs(mvcPF_serial))/2;
mvcDFPF_Nm = abs(mvcDFPF_serial)*serial2lbs_bipolar*lbs2NmAt15cm;

refsigserial2NmDF = mvcDF_Nm/4096*0.2;
refsigserial2NmPF = mvcPF_Nm/4096*0.2;
refsigserial2NmDFPF = mvcDFPF_Nm/2048*0.2;

clear figures;
figure(1)
title('1/4 Hertz DF');
hold on;
plot(P7quarterDF_ref*refsigserial2NmDF);
plot(P7quarterDF_m*serial2lbs_bipolar*lbs2NmAt15cm);
hold off;

figure(2)
title('1/4 Hertz PF');
hold on;
plot(P7quarterPF_ref*refsigserial2NmPF);
plot(P7quarterPF_m*serial2lbs_bipolar*lbs2NmAt15cm+4); % plus 4 fudge factor??
hold off;

figure(3);
title('1/4 Hz DFPF');
hold on;
plot(P7quarterDFPF_ref*refsigserial2NmDFPF);
plot(P7quarterDFPF_m*serial2lbs_bipolar*lbs2NmAt15cm+4);
hold off;




