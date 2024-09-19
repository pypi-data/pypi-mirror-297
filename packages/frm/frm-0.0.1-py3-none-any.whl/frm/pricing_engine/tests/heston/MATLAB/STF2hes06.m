% STF2hes06 Plots showing the influence of the correlation on the shape of 
% the smile in the Heston model 
% Written by Rafal Weron (21.05.2004)
% Ported to Matlab by Agnieszka Janek (07.07.2010)
% Revised by Rafal Weron (28.07.2010)

standalone = 0; % set to 0 to make plots as seen in STF2

% Marketvols July 1, 2004
marketvols1w  = [0.106 0.1015 0.1005 0.1025 0.107];
marketvols1m  = [0.1065 0.1012 0.0995 0.1012 0.1065];
marketvols3m  = [0.111 0.1048 0.102 0.1038 0.109];
marketvols6m  = [0.1132 0.1065 0.103 0.1045 0.1092];
marketvols1y  = [0.11525 0.10825 0.1045 0.10575 0.11075];
marketvols2y  = [0.1155 0.10825 0.1045 0.10575 0.1105];

% Forward deltas
delta = [0.1 0.25 0.5 0.75 0.9];

% Interest rates July 1, 2004
rd  = [0.02055 0.02055 0.02095 0.02165 0.02365 0.0291];
rf  = [0.01305 0.01325 0.01565 0.01845 0.02315 0.0315];
tau = [7/365 1/12 3/12 6/12 1 2];

% Spot EUR/USD on July 1, 2004
spot = 1.215; 
% Call option flag
cp = 1;

tic

% 1W smile ----------------------------------------------------------
marketvols = marketvols1w;
% Calculate spot delta
delta1w = exp(-rf(1)*tau(1))*delta;
[v01w,vv1w,kappa1w,theta1w,rho1w,IV1w,SSE1w] = HestonVanillaFitSmile(delta1w,marketvols,spot,rd(1),rf(1),tau(1),cp);

disp('=== 1W calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v01w,vv1w,kappa1w,theta1w,rho1w, 2*kappa1w*theta1w - vv1w^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV1w,SSE1w]*100)

figure(1)
subplot(2,2,1)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV1w*100,'rs--',  'LineWidth',1);
if standalone, title('1W market and Heston volatilities'); end
legend('1W smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% 1M smile ----------------------------------------------------------
marketvols = marketvols1m;
% Calculate spot delta
delta1m = exp(-rf(2)*tau(2))*delta;
[v01m,vv1m,kappa1m,theta1m,rho1m,IV1m,SSE1m] = HestonVanillaFitSmile(delta1m,marketvols,spot,rd(2),rf(2),tau(2),cp);

disp('=== 1M calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v01m,vv1m,kappa1m,theta1m,rho1m, 2*kappa1m*theta1m - vv1m^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV1m,SSE1m]*100)

subplot(2,2,2)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV1m*100,'rs--',  'LineWidth',1);
if standalone, title('1M market and Heston volatilities'); end
legend('1M smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% 3M smile ----------------------------------------------------------
marketvols = marketvols3m;
% Calculate spot delta
delta3m = exp(-rf(3)*tau(3))*delta;
[v03m,vv3m,kappa3m,theta3m,rho3m,IV3m,SSE3m] = HestonVanillaFitSmile(delta3m,marketvols,spot,rd(3),rf(3),tau(3),cp);

disp('=== 3M calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v03m,vv3m,kappa3m,theta3m,rho3m, 2*kappa3m*theta3m - vv3m^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV3m,SSE3m]*100)

subplot(2,2,3)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV3m*100,'rs--',  'LineWidth',1);
if standalone, title('3M market and Heston volatilities'); end
legend('3M smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% 6M smile ----------------------------------------------------------
marketvols = marketvols6m;
% Calculate spot delta
delta6m = exp(-rf(4)*tau(4))*delta;
[v06m,vv6m,kappa6m,theta6m,rho6m,IV6m,SSE6m] = HestonVanillaFitSmile(delta6m,marketvols,spot,rd(4),rf(4),tau(4),cp);

disp('=== 6M calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v06m,vv6m,kappa6m,theta6m,rho6m, 2*kappa6m*theta6m - vv6m^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV6m,SSE6m]*100)

subplot(2,2,4)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV6m*100,'rs--',  'LineWidth',1);
if standalone, title('6M market and Heston volatilities'); end
legend('6M smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% 1Y smile ----------------------------------------------------------
marketvols = marketvols1y;
% Calculate spot delta
delta1y = exp(-rf(5)*tau(5))*delta;
[v01y,vv1y,kappa1y,theta1y,rho1y,IV1y,SSE1y] = HestonVanillaFitSmile(delta1y,marketvols,spot,rd(5),rf(5),tau(5),cp);

disp('=== 1Y calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v01y,vv1y,kappa1y,theta1y,rho1y, 2*kappa1y*theta1y - vv1y^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV1y,SSE1y]*100)

figure(2)
subplot(2,2,1)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV1y*100,'rs--',  'LineWidth',1);
if standalone, title('1Y market and Heston volatilities'); end
legend('1Y smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% 2Y smile ----------------------------------------------------------
marketvols = marketvols2y;
% Calculate spot delta
delta2y = exp(-rf(6)*tau(6))*delta;
[v02y,vv2y,kappa2y,theta2y,rho2y,IV2y,SSE2y] = HestonVanillaFitSmile(delta2y,marketvols,spot,rd(6),rf(6),tau(6),cp);

disp('=== 2Y calibration results ===')
disp('v0, vv, kappa, theta, rho')
disp([v02y,vv2y,kappa2y,theta2y,rho2y, 2*kappa2y*theta2y - vv2y^2])
disp('[IV (10, 25, ATM, 75, 90), SSE] * 100%')
disp([IV2y,SSE2y]*100)

subplot(2,2,2)
plot(delta*100,marketvols*100,'ko-',  'LineWidth',1);
hold on
plot (delta*100,IV2y*100,'rs--',  'LineWidth',1);
if standalone, title('2Y market and Heston volatilities'); end
legend('2Y smile','Heston fit','Location','North')
xlabel ('Delta [%]');
ylabel ('Implied volatility [%]');
set(gca,'XTick', [10 25 50 75 90]);
hold off

% vol of vol and correlation term structure -----------------------
VV = [vv1w vv1m vv3m vv6m vv1y vv2y];
RHO = [rho1w rho1m rho3m rho6m rho1y rho2y];
tau = [7/365 1/12 3/12 6/12 1 2];

subplot(2,2,3)
plot(tau,VV,'ko-',  'LineWidth',1.2);
if standalone, title('Vol of vol term structure'); end
xlabel ('Tau [year]');
ylabel ('Vol of vol (\sigma)');
set(gca,'XTick', 0:0.5:2);
hold off

subplot(2,2,4)
plot (tau,RHO,'rs--',  'LineWidth',1);
if standalone, title('Correlation term structure'); end
xlabel ('Tau [year]');
ylabel ('Correlation (\rho)');
set(gca,'XTick', 0:0.5:2);
hold off

toc

