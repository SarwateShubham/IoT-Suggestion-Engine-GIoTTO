%% Storing data on the workbench

fnam = dir('/home/shubham/Desktop/MATLAB_BD/*.csv');
numfids = length(fnam);
values=zeros(101,numfids);
names={'time'};

%%Pre-processing
for K = 1:(numfids)
  [time,in,value]=(importfile(strcat('/home/shubham/Desktop/MATLAB_BD/',fnam(K).name)));
  fnam(K).name;
  time=unique(time,'stable'); 
  norm_time = (time - min(time)) / ( max(time) - min(time) );
  values(:,K)=interp1(norm_time,value(1:length(time)),0:0.01:1,'previous');
  names{K+1}=fnam(K).name;
end

%% Extract GPS DATA
% fnam = dir('C:\Users\lullichoti\Desktop\GPS\*.csv');
% numfids = length(fnam);
% values_g=zeros(10001,numfids);
% 
% % for K = v1:(numfids)
% %   [time_n,var]=(importfile(strcat('C:\Users\lullichoti\Desktop\GPS\',fnam(K).name))); 
% %   time_N=unique(time_n,'stable'); 
% %   norm_time = (time_N - min(time)) / ( max(time) - min(time) );
% %   values_g(:,K)=interp1(norm_time,var(1:length(time_N)),0:0.0001:1,'nearest');
% %   names{K+1}=fnam(K).name;
% % end


%% Final Data Concat
Data=values(:,:);
%% Experiment 1
X=Data(:,1:(size(Data,2)-1));
Y=Data(:,size(Data,2));


% % mdl = fscnca(X,Y,'Solver','sgd','Verbose',1);
%mdl = fscnca(X,Y);
%figure() 
%plot(mdl.FeatureWeights,'ro')
%grid on
%xlabel('Feature index')
% ylabel('Feature weight')
%find(mdl.FeatureWeights==max(mdl.FeatureWeights))
%Sensor=(fnam(find(mdl.FeatureWeights==max(mdl.FeatureWeights))-1).name);
%ma=max(mdl.FeatureWeights);
[ma, gain] = infogain(X,Y);
Sensor=(fnam(ma).name);
Comloca=strfind(Sensor,',');
Name_Sen=Sensor(1:Comloca(1)-1);
Location_Sen=Sensor(Comloca(1)+1:Comloca(2)-1);
uuid_Sen=Sensor(Comloca(2)+1:Comloca(3)-1);
Region_Sen=Sensor(Comloca(3)+1:size(Sensor,2)-4);

Actuator=fnam(size(fnam)).name;
Comloca=strfind(Actuator,',');
Name_Act=Actuator(1:Comloca(1)-1);
Location_Act=Actuator(Comloca(1)+1:Comloca(2)-1);
uuid_Act=Actuator(Comloca(2)+1:Comloca(3)-1);
Region_Act=Actuator(Comloca(3)+1:size(Actuator,2)-4);
identity='all';
type='lifx';


%% Experiment 2


pos=[];
neg=[];
%histogram(values(:,2));
gauss = inline('(1/(sqrt(2*pi)*s))*exp(-(x-m).*(x-m)/(2*s*s))', 'x','m','s');

for i=1:1:size(Y)
    if(Y(i)>0)
        pos=[pos,X(i,ma)];
        mean_pos=mean(pos);
        var_pos=var(pos);
    else
        neg=[neg,X(i,ma)];
        mean_neg=mean(neg);
        var_neg=var(neg);
    end
end
val=num2str((mean_pos+mean_neg)/2);
for i=mean_neg:(mean_pos-mean_neg)/100:mean_pos
    if gauss(i,mean_neg,var_neg)<gauss(i,mean_pos,var_pos)
        %val=num2str(i);
    end
end

figure
plot(-10000:10000,gauss([-10000:10000],mean_pos,var_pos));
hold on
plot(-10000:10000,gauss([-10000:10000],mean_neg,var_neg),'r');

commandStr = char(strcat('python /home/shubham/Desktop/change_flow.py ',{' '},Location_Sen,...
    {' '},{Name_Sen},{' '},Region_Sen,{' '},uuid_Sen,{' '},val,{' '},Location_Act,{' '},...
    Name_Act,{' '},Region_Act,{' '},type,{' '},identity));

[status, commandOut] = system(commandStr);
%exit
