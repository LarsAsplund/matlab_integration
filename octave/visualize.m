% Parse arguments
arg_list = argv;
output_path = arg_list{1};
plot_title = arg_list{2};
num_of_data_sets = arg_list{3};

% Configure figure
fig = figure('Name', 'Testbench Progress');
title(plot_title)
xlabel("x")
ylabel("y")
xlim([0 100])
ylim([0 100])
hold on

% Wait on data set files and plot
data = [];
for s = 1:str2num(num_of_data_sets)
  file_name = fullfile(output_path, strcat("data_set_", int2str(s), ".csv"));
  while not(exist(file_name, 'file'))
    pause(0.1)
  end
  data_set = csvread(file_name);
  data = [data, data_set];
  x = 0 : length(data) - 1;
  plot(x, data)
end

% Verify that the data set is monotonically increasing
if sum(data(1:length(data)-1) >= data(2:length(data))) == 0
  f = fopen(fullfile(output_path, "pass"), "w");
else
  f = fopen(fullfile(output_path, "fail"), "w");
  disp("ERROR: Output is not monotonically increasing!")
end
fclose(f);

% Quit when figure is closed
pause(1)
waitfor(fig);
