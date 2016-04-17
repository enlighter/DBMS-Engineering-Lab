#Test and run hadoop operations
* First download `access_log` and `purchases.txt` data:

  `wget http://content.udacity-data.com/courses/ud617/access_log.gz`

  and the purchases.txt from:
  https://drive.google.com/open?id=0B7RCU39Osj3iUmpacVBZQmpYQ28
* Then extract the contents in this folder

##Hadoop operations
* Hadoop operations are listed in order in the shell script `hadoop-operations.sh`

##For testing
* e.g. `cat sales_data | ./mapper.py`
* testing map-reduce script in one pipeline:

  `cat sales_data | ./sales_mapper_byStore.py | sort | ./sales_reducer_byStore.py`

* testing map-reduce in pipeline category-wise:

  `cat sales_data | ./sales_mapper_byCategory.py | sort | ./sales_reducer_byCategory.py`

* other tests :

  `head -50 access_log | ./log_mapper.py | sort | ./log_reducer.py`

  `head -50 access_log | ./log_mapper_iphits.py | sort | ./log_reducer.py`

  `head -100 access_log | ./log_mapper_fhitsc.py | sort | ./log_reducer_max.py`
