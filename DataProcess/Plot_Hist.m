function [pos,neg]=Plot_Hist( Data ,col,pred_col)
pos=[];
neg=[];
histogram(Data(:,col));
gauss = inline('(1/(sqrt(2*pi)*s))*exp(-(x-m).*(x-m)/(2*s*s))', 'x','m','s');
for i=1:1:size(Data,1)
    if(Data(i,pred_col)==1)
        pos=[pos, Data(i,col)];   
    else
        neg=[neg,Data(i,col)];    
    end
end
mean_pos=mean(pos);
var_pos=var(pos);
mean_neg=mean(neg);
var_neg=var(neg);
x_min=0.9*min(Data(:,col));
x_max=1.1*max(Data(:,col));
figure
plot(x_min:x_max,gauss(x_min:x_max,mean_pos,sqrt(var_pos)));
hold on
plot(x_min:x_max,gauss(x_min:x_max,mean_neg,sqrt(var_neg)));
hold off

end

