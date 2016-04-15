currentdir=$(pwd|sed 's/ /\%20/g')
mapperlink="$currentdir/mapper.py"
reducerlink="$currentdir/reducer.py"

#make sure the abosukte path to the directory containing
#sales_data and mapper and reducer doesn't have any 'blank space in it'
hadoop fs -put sales_data
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_byStore.py -file sales_mapper_byStore.py -file sales_reducer_byStore.py -input sales_data -output salesout
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_byStore.py -file sales_mapper_byStore.py -file sales_reducer_byStore.py -input purchases.txt -output salesout2
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byCategory.py -reducer sales_reducer_byCategory.py -file sales_mapper_byCategory.py -file sales_reducer_byCategory.py -input purchases.txt -output sales_by_category
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_storeMax.py -file sales_mapper_byStore.py -file sales_reducer_storeMax.py -input purchases.txt -output sales_store_max
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_overallSales.py -file sales_mapper_byStore.py -file sales_reducer_overallSales.py -input purchases.txt -output sales_overall

hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper log_mapper.py -reducer log_reducer.py -file log_mapper.py -file log_reducer.py -input access_log -output log_hits

hadoop fs -put access_log
