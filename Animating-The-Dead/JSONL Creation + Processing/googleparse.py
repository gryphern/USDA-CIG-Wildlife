#
# Using https://python.plainenglish.io/data-extraction-parse-a-3-nested-json-object-23cb978b66ad
#
# Python libraries
import pandas as pd
import argparse
import json
import openpyxl

parser = argparse.ArgumentParser(description='Read and decode JSONL results')
parser.add_argument('inputFilename')
parser.add_argument('-o',dest='outputFilename', default='googleparse-results')

args = parser.parse_args()
if args.inputFilename is not None:
    print("The file name is '{}', output is '{}'".format(args.inputFilename,args.outputFilename))
else:
    print('Oh well ; No args, no problems')

inputFD = open(args.inputFilename, 'r')
jsonLines = inputFD.readlines()

# Start the DFALL dataframe
dfALL = pd.DataFrame()

# Strips the newline character
for aline in jsonLines:
    lineData = json.loads(aline)
#    print("Line{}: {}".format(count, aline.strip()))
    subtree_content = lineData['instance']
    subtree_prediction  = lineData['prediction']
#    print("\nsubtree_content: '" + str(subtree_content) + "'")
#    print("\nsubtree_prediction: '" + str(subtree_prediction) + "'")
    print("------")
    print("Content: '" + subtree_content['content'])
    print("mimeType: '" + subtree_content['mimeType'] + "'")
#   output the PREDICTION section(s)
    dfpredict = pd.DataFrame(subtree_prediction,index=None)
    dfpredict['content'] = subtree_content['content']
    print(dfpredict)
    dfALL = dfALL.append(dfpredict)
    
# now write the accumulated dataframe
outputExcelFilename  = args.outputFilename + ".xlsx"
print("Output to EXCEL at '" + outputExcelFilename + "'")
with pd.ExcelWriter(outputExcelFilename) as writer:
        dfALL.to_excel(writer,sheet_name="Sheet1")
        

        
