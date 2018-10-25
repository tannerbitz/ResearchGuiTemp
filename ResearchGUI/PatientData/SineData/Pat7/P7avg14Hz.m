clear;
clc;
close all;

p7mvcdf = load('Patient7_MVC_DF.txt');
p7df25 = load('PatNo7_VR_AnklePosNeutral_DF_0-25Hz.txt');

p7df_m = p7df25(:,1);
p7df_ref = p7df25(:,2);

serial2lbs_bipolar = 125/2048;
lbs2NmAt15cm = 4.448*.15;

n = 9704;
for i = 1:14
    
    df(:,i) = p7df_m(n:4000+n);
    n = n + 4000;
    
 
    
end

for i = 1:4001
    
SDdfRow(i) = std(df(i,:));
Mean_df(i) = mean(df(i,:));

end

lbound = Mean_df - SDdfRow;
lbound2 = Mean_df - 2*SDdfRow;
ubound = Mean_df + SDdfRow;
ubound2 = Mean_df + 2*SDdfRow;

for i = 1:14
    SE(i) = sumsqr(df(:,i)-Mean_df');
    vcnt = 0;
    vcnt2 = 0;
    for j = 1:length(df(:,i))
        if (df(j, i) < lbound(j) || df(j,i) > ubound(j))
            vcnt = vcnt + 1;
        end
        if (df(j, i) < lbound2(j) || df(j,i) > ubound2(j))
            vcnt2 = vcnt2 + 1;
        end
    end
    v1(i) = vcnt;
    v2(i) = vcnt2;
end


for i = 1:14
    figure(i);
    hold on;
    plot(lbound2, 'm','HandleVisibility', 'off');
    plot(ubound2, 'm');
    plot(lbound, 'r');
    plot(Mean_df, 'b');
    plot(ubound, 'r','HandleVisibility', 'off');
    plot(df(:, i), 'g');
    xlabel('Time(ms)');
    ylabel('Resolution Point');
    meas_str = sprintf('Measured - SE: %1.2f  -  V1: %i -  V2: %i', SE(i)/mean(SE), v1(i), v2(i));
    legend('2 STD', '1 STD','Avg', meas_str);
    hold off
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

refsig = p7df_ref(9705:9507+4001);
refsigser2Nm = mvcdf_Nm/4096*0.2;

ref = refsig*refsigser2Nm;
SDref = std(ref);
refp = ref + SDref;
refm = ref - SDref;
% 
% hold on;
% title('1/4 Hz Dorsiflexion');
% xlabel('Time (ms)');
% ylabel('Nm');
% 
% plot(dfm*serial2lbs_bipolar*lbs2NmAt15cm+8.25);
% plot(ref);
% %plot(refp);
% %plot(refm);
% xlim([0 4000]);
% legend('Measured','Reference','+1 STD','-1 STD');





