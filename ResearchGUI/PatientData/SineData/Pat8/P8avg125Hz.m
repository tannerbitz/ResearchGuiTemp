clear;
clc;

p7mvcdf = load('Patient8_MVC_DF.txt');
p7df25 = load('PatNo8_VR_AnklePosNeutral_DF_1-25Hz.txt');

p7df_m = p7df25(:,1);
p7df_ref = p7df25(:,2);

serial2lbs_bipolar = 125/2048;
lbs2NmAt15cm = 4.448*.15;

n = 450;
for i = 1:80
    
    df(:,i) = p7df_m(n:800+n);
    n = n + 800;
 
    
end

dfm = mean(df,2);

SDdfm = std(dfm);
SDdfmP = dfm + SDdfm;
SDdfmM = dfm - SDdfm;

mvcdf1 = max(p7mvcdf(5500:9500));
mvcdf2 = max(p7mvcdf(25500:29500));
mvcdf3 = max(p7mvcdf(45500:49500));

mvcdfSerial = max([mvcdf1, mvcdf2, mvcdf3]);
mvcdf_Nm = abs(mvcdfSerial)*serial2lbs_bipolar*lbs2NmAt15cm;

refsig = p7df_ref(451:1251);
refsigser2Nm = mvcdf_Nm/4096*0.2;

ref = refsig*refsigser2Nm;
SDref = std(ref);
refp = ref + SDref;
refm = ref - SDref;

hold on;
title('1.25 Hz Dorsiflexion');
plot(dfm*serial2lbs_bipolar*lbs2NmAt15cm+7.25);
plot(ref);
%plot(SDdfmP*serial2lbs_bipolar*lbs2NmAt15cm+7.25);
%plot(SDdfmM*serial2lbs_bipolar*lbs2NmAt15cm+7.25);
plot(refp);
plot(refm);
xlim([0 800]);
legend('Measured','Reference','+1 STD','-1 STD');

