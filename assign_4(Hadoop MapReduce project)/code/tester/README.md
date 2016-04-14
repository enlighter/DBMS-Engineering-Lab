#Test and run hadoop operations
* First download access_log data:
  wget http://content.udacity-data.com/courses/ud617/access_log.gz
* Then extract the contents in this folder

##Hadoop operations
* Hadoop operations are listed in order in the shell script `hadoop-operations.sh`

##For testing
* e.g. `cat sales_data | ./mapper.py`
* testing map-reduce script in one pipeline:

  `cat sales_data | ./mapper.py | sort | ./reducer.py`
