To answer the three questions and prepare the report, you need to run "python log_analysis.py" (using python 3).
Each question is handled using a separate function. Before you run the code, first create a view using the following command:

create view status_days as select status, date_part('day', time) as day from log

