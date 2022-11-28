function [Training, Target] = Load_Data(File_Name)

warning('off')
Training_Dataset = File_Name;
Training_Dataset_Options = detectImportOptions(Training_Dataset);

Training_Data = readtable(Training_Dataset, Training_Dataset_Options, "UseExcel", false);

Studytime = Training_Data.studytime;
Absences = Training_Data.absences;
Set1 = Training_Data.Set1;
Set2 = Training_Data.Set2;

Training = [Studytime Absences Set1 Set2];
Target = Training_Data.Grade;

end