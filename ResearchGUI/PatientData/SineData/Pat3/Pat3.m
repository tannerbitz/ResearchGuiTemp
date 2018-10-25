x = load('PatNo3_VR_AnklePosNeutral_DF_Freq0-25Hz_Trial1.txt');
mvcdfdata = load('Patient3_MVC_DF.txt');
mvcpfdata = load('Patient3_MVC_PF.txt');

mvcdf_measured = mvcdfdata(:,1);
mvcpf_measured = mvcpfdata(:,1);
vr_pf_measured = x(:,1);
vr_pf_ref = x(:,2);
zerolevel_vr = min(vr_pf_measured(1:4500));
vr_pf_measured = vr_pf_measured - zerolevel_vr;


%% MVC PF
zerolevel1 = round(mean(mvcpf_measured(1:4500)));
mvcpf1 = min(mvcpf_measured(5500:9500)) - zerolevel1;
zerolevel2 = round(mean(mvcpf_measured(10500:24500)));
mvcpf2 = min(mvcpf_measured(25500:29500)) - zerolevel2;
zerolevel3 = round(mean(mvcpf_measured(30500:44500)));
mvcpf3 = min(mvcpf_measured(45550:end)) - zerolevel3;


serial2lbs_bipolar = 125/2048;
lbs2NmAt15cm = 4.448*.15;

mvcpf_serial = min([mvcpf1, mvcpf2, mvcpf3])
mvcpf_Nm = abs(mvcpf_serial)*serial2lbs_bipolar*lbs2NmAt15cm

refsignalserial2Nm = mvcpf_Nm/4096*0.2;



clear figures
figure(1)
hold on
plot(vr_pf_ref*refsignalserial2Nm);
plot(vr_pf_measured*serial2lbs_bipolar*lbs2NmAt15cm);
hold off


%%



figure(1)
plot(mvcdf_measured)
figure(2)
plot(mvcpf_measured)


