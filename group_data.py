class Grouper(object):
    """
    Functions for identifying the groups of a list by an indicator
    A group should be a numeric number where the first digit signifies the
    major group, and each subsequent digit is a sub group of the previous level
    The object requires several fields when instanctiated as follows
    Grouper(data,group_index,specifity,data_index);
    data is the data file which is to be grouped_data
    group_index is the column index of the group number in data
    specifity decides which sub group to group by, 1 will group by the major
    group, 2 by the sub group to the major group etc.
    data_index is the column index of the data being collected in the groups
    """
    def __init__(self,data,group_index,specifity,data_index):
        """
        Initialise the group by reducing the group number to the required
        specifity
        """
        self.group_index = group_index
        self.data_index = data_index
        self.data=data
        #Set the parameters of group and data indexs for functions
        for i in xrange(len(data)):
        #Iterate for each row of the datafile
            if len(data[i][group_index])>specifity or\
            data[i][group_index] != '':
                self.data[i][group_index] = \
                data[i][group_index][0:specifity]
            else:
                pass
            #If the group number is not missing and longer than the required
            #specifity reduce the group to the number of required digits
            #Returns the input data list with the required groups
    def create_dict(self):
        """
        Function to group the elements of the data list using a dictionary
        """
        self.d = {'All Data':[]}
        #Create an initial dictionary - this will store all the data
        for l in self.data:
            self.d['All Data'].append(l[self.data_index])
            #For each line of the input data set, add the data to the 'All Data'
            #key
            if l[self.group_index] in self.d:
                #Check if the group already exists in the dictionary
                self.d[l[self.group_index]].append(l[self.data_index])
                #Add the data to the group
            else:
                self.d[l[self.group_index]]=[]
                #If the group does not exist, initialise the group with an empty
                #list
                self.d[l[self.group_index]].append(l[self.data_index])
                #Add the data to the newly created group
        #Returns a dictionary containing each group as a key and all the data
        #from each group as a list of lists
    def create_corpus(self):
        for key in self.d:
            self.d[key]=sum(self.d[key],[])
