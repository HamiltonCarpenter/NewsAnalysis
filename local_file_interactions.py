import re
import string
from misc_helper_funcs_and_constants import *
from database_interactions import *  

class LocalFileHandler:

    #replace hard coded root with define in file somewhere 
    def __init__(self):
        self.root = "/home/hog/Documents/nltk_practice/ArticleFiles/"

    #Creates the project specific file struture that is to be appended to the directory root
    def generate_organizational_path(self, doc_status,outlet,category,date):
        year = date.year
        month = date.month
        day = date.day
        return(doc_status+'/'+str(year)+'/'+str(month)+'/'+str(day))+'/'+category+'/'+outlet+'/'

    #splits the path so that we can check each nested directory one at a time
    def split_path_string_to_list(self, instring):
        dirty_list = instring.split("/")
        clean_list = [level for level in dirty_list if '' != level]
        return clean_list

    #RENAME
    #combines the file storage root and the organizational structure  
    def find_absolute_file_path(self, structure):
        return self.root+structure

    #RENAME
    #Combines filename with the complete path
    def find_absolute_document_location(self, structure,file_name):
        dir_structure = self.find_absolute_file_path(structure)
        if(structure[-1] != '/'):
            structure = structure + '/'
            
        return dir_structure+file_name
    
    #finds where the file is for a given url
    def get_absolute_document_location(self,url,is_raw=True):
        db = DatabaseManager()
        date = db.get_date_for_url_db(url)
        outlet = db.get_outlet_for_url_db(url)
        doc_status = raw if is_raw else clean
        
        structure = self.generate_organizational_path(doc_status,outlet,politics,date)
        
        file_name = self.convert_url_to_filename(url)
        return self.find_absolute_document_location(structure,file_name)
        
    #replace hardcoded root
    #remove and replace root is dumb 
    def update_path_structure(self, structure):
        if(self.root in structure):
            structure = structure.split(self.root)[1]
        #REMOVE ROOT HERE
        structure_layers = self.split_path_string_to_list(structure)
        #if structure_layers[-1] ==
        current_verefied_depth = self.root
        created = False

        for level in structure_layers:
            test = current_verefied_depth+'/'+level
            if os.path.exists(test):
                current_verefied_depth = test
            elif ".txt" in level:  #allows function to take file locations and build path for
                pass
            else:
                os.mkdir(test)
                current_verefied_depth = test
                created = True
        return created

    #def correct_location(self):
    #    return (os.path.exists("article_files"))
    def path_exists(self, inpath):
        return (os.path.exists(inpath))

    #RENAME TO READ FILE
    def get_text_from_location(self, file_location):
        if not self.path_exists(file_location):         #change to file exists
            print("path: "+ file_location+ " does not exist")
            return 0
        else:    
            with open(file_location, 'r') as content_file:
                content = content_file.read()
                return content

    #gets rid of bad characters that would be incompatible with file system. 
    #there should be better existing solutions that I should look into  
    def convert_url_to_filename(self, url):
        url = url.replace('.','_')
        url = url.replace('/','_')
        name = url + '.txt'
        return name

    #splits the filename and the file path 
    def split_filename_and_path(self,string):
        ls = string.rsplit('/',1)
        return (ls[0]+'/',ls[1])
    
    #writes a string to a given file location under given filename
    def write_text_to_location(self, text,filename,filepath):
        if not self.path_exists(filepath):
            print("path: "+ filepath+ " does not exist")
            return 0
        else:    
            f=open(filepath+filename, "w+")
            f.write(text)
            return 1
        
    #verifies that a given string contains a text file extention
    def string_contains_text_file(self, string):
        x = re.findall(".txt+", string)
        if len(x)==0:
            return True
        else:
            return False
        
    #writes doc to either standard clean or standard raw location 
    def write_doc_to_location(self,document,destination):
        if destination == standard_clean_directory or destination == standard_raw_directory:
            if destination == standard_clean_directory:
                file_location = self.get_absolute_document_location(document.url,is_raw=False)
            else:
                file_location = self.get_absolute_document_location(document.url,is_raw=True)
            print('file loc: ',file_location)
            pair = self.split_filename_and_path(file_location)

            filepath = pair[0]
            print('filepath: ',filepath)
            filename = pair[1]
            print('filename: ',filename)
            self.update_path_structure(filepath)
            self.write_text_to_location(document.text,filename,filepath)
            print('writing to: ',filepath,filename)
            
        else:
            print("Haven't implemented general purpose writing yet")
        

