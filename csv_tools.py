import csv
import os

def get_content(filepath, content_index, separator=','):
    '''returns a list of the content at a particular index '''
    contentList = []
    if(os.path.exists(filepath)):
        with open(filepath, encoding='utf-8') as csvFile:
            csv_reader = csv.reader(csvFile, delimiter=separator)
            for row in csv_reader:
                if len(row) > content_index:
                    # get list content from csv at index
                    contentList.append(row[content_index])
    
    return contentList

def get_content_as_hashmap(filepath, content_index, separator=','):
    '''returns a list of the content at a particular index '''
    contentDict = {}
    if(os.path.exists(filepath)):
        with open(filepath, encoding='utf-8') as csvFile:
            csv_reader = csv.reader(csvFile, delimiter=separator)
            for row in csv_reader:
                if len(row) > content_index:
                    # get list content from csv at index
                    _key = row[content_index]
                    if _key not in contentDict:
                        contentDict[_key] = _key
                    # contentList.append(row[content_index])
    
    return contentDict


