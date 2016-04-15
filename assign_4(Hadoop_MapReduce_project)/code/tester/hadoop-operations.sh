currentdir=$(pwd|sed 's/ /\%20/g')
mapperlink="$currentdir/mapper.py"
reducerlink="$currentdir/reducer.py"

#make sure the abosukte path to the directory containing
#sales_data and mapper and reducer doesn't have any 'blank space in it'
hadoop fs -put sales_data
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_byStore.py -file sales_mapper_byStore.py -file sales_reducer_byStore.py -input sales_data -output salesout
hadoop jar /usr/lib/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -mapper sales_mapper_byStore.py -reducer sales_reducer_byStore.py -file sales_mapper_byStore.py -file sales_reducer_byStore.py -input purchases.txt -output salesout2
hadoop fs -put access_log
