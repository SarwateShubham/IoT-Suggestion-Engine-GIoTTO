%% Documentation
% This code is used to suggest rules to the user on the basis of his 
% interaction with his environment.
% The code takes the files stored in Sensor_data folder and pre-processes it,
% later it applies information gain to extract the sensor that is the most
% crucial in predicting the state of the actuator. Next it uses gaussian 
% classification to classify the data into the two classes and find the 
% prediction boundary.


%% Storing data on the workbench

fnam = dir('..\Sensor_data\*.csv');
numfids = length(fnam);
values=zeros(101,numfids);
names={'time'};

%% Pre-processing
for K = 1:(numfids)
  [time,in,value]=(importfile(strcat('..\Sensor_data\',fnam(K).name)));
  fnam(K).name;
  time=unique(time,'stable'); 
  norm_time = (time - min(time)) / ( max(time) - min(time) );
  values(:,K)=interp1(norm_time,value(1:length(time)),0:0.01:1,'previous');
  names{K+1}=fnam(K).name;
end

%% Final Data Concat
Data=values(:,:);
X=Data(:,1:(size(Data,2)-1));
Y=Data(:,size(Data,2));

%% Information Gain & Feature Selection
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


%% Gaussian Classification 


pos=[];
neg=[];
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
try
   val=num2str((mean_pos+mean_neg)/2);
catch ME
    disp(ME.identifier)
    if (strcmp('MATLAB:UndefinedFunction',ME.identifier))
        disp('Please check if the state of the actuator is changing');
    
    end
end

%Uncomment the below code if the value of the classification is not
%accurate.

% for i=mean_neg:(mean_pos-mean_neg)/100:mean_pos
%     if gauss(i,mean_neg,var_neg)<gauss(i,mean_pos,var_pos)
%         val=num2str(i);
%     end
% end

figure
plot(-10000:10000,gauss([-10000:10000],mean_pos,var_pos));
hold on
plot(-10000:10000,gauss([-10000:10000],mean_neg,var_neg),'r');

commandStr = char(strcat('python ./change_flow.py ',{' '},Location_Sen,...
    {' '},{Name_Sen},{' '},Region_Sen,{' '},uuid_Sen,{' '},val,{' '},...
    Location_Act,{' '},Name_Act,{' '},Region_Act,{' '},type,{' '},identity));

[status, commandOut] = system(commandStr);
exit
