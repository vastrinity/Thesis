function [Predictor, Records] = Train_Network(Training_Dataset, Target_Dataset)

Learning_Algorithm = 'trainlm';
Network_Architecture = [10 10 10];

setdemorandstream(491218382)

The_Network = fitnet(Network_Architecture, Learning_Algorithm);

The_Network.divideFcn = 'dividerand';
The_Network.divideMode = 'sample';
The_Network.divideParam.trainRatio = 70/100;
The_Network.divideParam.testRatio = 15/100;
The_Network.divideParam.valRatio = 15/100;

The_Network.performFcn = 'mse';
The_Network.plotFcns = {'plotperform', 'plottrainstate', 'ploterrhist', 'plotregression'};

[Predictor, Records] = train(The_Network, Training_Dataset', Target_Dataset');

end