import xursparks
import sys
from pyspark.sql.types import *
from pyspark.sql.functions import *

def prepareData():
    print("prepareData() :: start")
    print("prepareData() :: end")

def processData():
    print("processData()  :: start")
    # xursparks.generateDataQualityReport(dq_title="email title value",
    #                                     dq_file_path="<file/path/>",
    #                                     dq_df=targettabledataset,
    #                                     dq_message="email body message")

    xursparks.generateDataQualityReport()
    print("processData()  :: end")

if __name__ == '__main__':
    xursparks.initialize(sys.argv)
    prepareData()
    processData()
    xursparks.tearDown()