clear all

load('D:\FluxData\Sherman_Barn\SB_2018200_to_2019230_L3')

plottime=datetime(datevec(data.Mdate));
CH4=data.wm;
CO2=data.wc;


CO2_gf=data.wc_ANN;
CH4_gf=data.wm_ANN;

figure;subplot(2,1,1)
plot(plottime,CO2_gf);hold on
plot(plottime,CO2);
yline(0,'--');ylim([-25,30])
legend('ANN Gap filled','Original','Location','Best')
title('CO_2 flux')
ylabel('CO_2 flux (umol m^{-2} s^{-1})')


subplot(2,1,2)
plot(plottime,CH4_gf);hold on
plot(plottime,CH4);
yline(0,'--');ylim([-100,500])
legend('ANN Gap filled','Original','Location','Best')
title('CH_4 flux')
ylabel('CH_4 flux (nmol m^{-2} s^{-1})')

% From Aug 1st to July 31st

start=datenum(2018,08,1,0,0,0);
last=datenum(2019,08,1,0,0,0);
ix=data.Mdate>=start & data.Mdate<last;

CH4a=CH4_gf(ix);
CO2a=CO2_gf(ix);

CH4_sum=nansum(CH4a)*1800;% nmol m2 Year
CO2_sum=nansum(CO2a)*1800;% umol m2 Year

CO2_g=CO2_sum*12/(10^6);%& g m-2 year
CH4_g=CH4_sum*12/(10^9);%& g m-2 year

CH4_g_SWP=CH4_g*16/12*45




