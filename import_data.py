import csv,sys,os,urllib2
#Import the CSV module to read text files
class Importer(object):
    """
    Object to import files
    Requires a text file string or open URL object and a delimeter string
    Will return imported attribute which contains the text
    file as a list
    """
    def __init__(self, imp_file, delim):
        if os.path.isfile(imp_file):
            with(open(imp_file)) as f:
            #Open file to import
                reader=csv.reader(f, delimiter=delim)
                #Reads in the file using the parameter
                temp_list=list(reader)
                self.imported=[x for x in temp_list if x]
                #Returns the imported file as a list of each non-missing row
        elif type(imp_file)==file:
            reader=csv.reader(imp_file, delimiter=delim)
            #Reads in the file using the parameter
            temp_list=list(reader)
            self.imported=[x for x in temp_list if x]
            #Returns the imported file as a list of each non-missing row
        else:
            f=urllib2.urlopen(imp_file)
            #If no file exists locally, look for url to read
            reader=csv.reader(f,delimiter=delim)
            temp_list=list(reader)
            self.imported=[x for x in temp_list if x]
            #Returns the imported file as a list of each non-missing row
