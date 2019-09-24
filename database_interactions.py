#url id in urls database store url id
import json
from misc_helper_funcs_and_constants import *
class DatabaseManager:

    def __init__(self):
        #def default_newsdatabase_connect():
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="pythonuser",
          passwd="password",
          database="newsdatabase"
        ) 

        self.mycursor = self.mydb.cursor(buffered=True)
#    return self.mycursor
#self.mycursor = default_newsdatabase_connect()

    def get_date_for_url_db(self, url):
        sql = "SELECT date FROM urls WHERE url= %s"
        val = (url,)

        self.mycursor.execute(sql,val)
        row = self.mycursor.fetchall()
        assert(1 == len(row))
        db_date = row[0][0]
        obj_date = convert_m_d_y_to_date_object(db_date)
        return obj_date

    def get_outlet_for_url_db(self, url):
        sql = "SELECT outlet FROM urls WHERE url= %s"
        val = (url,)

        self.mycursor.execute(sql,val)
        row = self.mycursor.fetchall()
        assert(1 == len(row))
        outlet = row[0][0]
        return outlet

    def check_article_rawtext_present(self, url):
        t = (url,)
        #print(self.mycursor.execute('SELECT * FROM urls WHERE id=2'))
        self.mycursor.execute('SELECT * FROM check WHERE url=%s', t)
        match = self.mycursor.fetchall()
        return len(match) > 0
    

    def check_present(self,url):
        t = (url,)
        #print(self.mycursor.execute('SELECT * FROM urls WHERE id=2'))
        self.mycursor.execute('SELECT * FROM urls WHERE url=%s', t)
        match = self.mycursor.fetchall()
        return len(match) > 0

    def write_urls_to_db(self, url_list, outlet, category, date):
        for link in url_list:
            if not self.check_present(construct_full_url(link, outlet)):
                #print(construct_full_url('/2019/08/19/us/politics/elizabeth-warren-native-american.html', 'NewYorkTimes'))
                sql = "INSERT INTO urls (url, date, outlet) VALUES (%s, %s, %s)"
                val = (construct_full_url(link, outlet),date,outlet) #("https://www.nytimes.com"+link, "08/20/2019",NewYorkTimes)
                self.mycursor.execute(sql, val)

                self.mydb.commit()

                print(self.mycursor.rowcount, "record inserted.")
                
#URLS ABOVE ------------------------------------------------------
#

    def set_path_for_file_db(self, url, file_loc):
        self.mycursor = self.mydb.cursor()
        sql = "UPDATE Rawtext SET File_Location = %s WHERE URL = %s"
        val = (file_loc, url)
        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def mark_url_as_scraped_db(self, url):
        self.mycursor = self.mydb.cursor()
        sql = "UPDATE Rawtext SET Scraped = 1 WHERE URL = %s"
        val = (url,)
        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def get_unscraped_urls_from_db(self):
        sql = "SELECT * FROM Rawtext WHERE Scraped = 0"

        self.mycursor.execute(sql)
        unscrapped = self.mycursor.fetchall()
        return unscrapped

    def update_unscraped_article(self, url, file_location):
        #self.mycursor = self.mydb.cursor()

        sql = "UPDATE Rawtext SET File_Location = %s WHERE URL = %s"
        val = (file_location, URL)

        self.mycursor.execute(sql, val)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record(s) affected") 

    def write_raw_text_to_db(self, url, rawtext):
        if not check_article_rawtext_present(construct_full_url(url)):
            #print(construct_full_url('/2019/08/19/us/politics/elizabeth-warren-native-american.html', 'NewYorkTimes'))
            sql = "INSERT INTO raw_articles (url, raw_article) VALUES (%s, %s)"
            val = (construct_full_url(link, outlet),date,outlet) #("https://www.nytimes.com"+link, "08/20/2019",NewYorkTimes)
            self.mycursor.execute(sql, val)

            self.mydb.commit()

            print(self.mycursor.rowcount, "record inserted.")

    def update_scrape_table(self):
        #connect to db

        sql = "SELECT * FROM urls WHERE url NOT IN (SELECT URL FROM Rawtext)"

        self.mycursor.execute(sql)
        unscrapped = self.mycursor.fetchall()

        insert_sql = "INSERT INTO Rawtext (Scraped, URL, File_Location) VALUES (%s, %s, %s)"
        for x in unscrapped:

            URL=x[0]
            Scraped = 0
            File_Location= None

            insertval = (Scraped,URL,File_Location) #("https://www.nytimes.com"+link, "08/20/2019",NewYorkTimes)
            self.mycursor.execute(insert_sql, insertval)

            self.mydb.commit()
            print(URL+" Transered")

            #RAWTEXT ABOVE ------------------------------------------------------
            
    def update_parsed_table(self):
        #connect to db

        sql = "SELECT URL FROM Rawtext WHERE URL NOT IN (SELECT URL FROM Parsedtext)"

        self.mycursor.execute(sql)
        unscrapped = self.mycursor.fetchall()

        insert_sql = "INSERT INTO Parsedtext (Parsed, URL, File_Location) VALUES (%s, %s, %s)"
        for x in unscrapped:

            URL=x[0]
            Parsed = 0
            File_Location= None

            insertval = (Parsed,URL,File_Location) #("https://www.nytimes.com"+link, "08/20/2019",NewYorkTimes)
            self.mycursor.execute(insert_sql, insertval)

            self.mydb.commit()
            print(URL+" Transered")
            
    def get_uncleaned_urls_from_db(self):
        sql = "SELECT URL FROM Parsedtext WHERE Parsed = %s"
        val = (0,)

        self.mycursor.execute(sql,val)
        unscrapped = self.mycursor.fetchall()
        return unscrapped
        
    def set_cleaned_file_location(self,url,file_location):
        sql = "UPDATE Parsedtext SET File_Location = %s, Parsed = %s WHERE URL = %s"
        val = (file_location, 1, url)

        self.mycursor.execute(sql, val)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record(s) affected") 
        
    # PARSED TEXT ABOVE -----------------------------------------------------------------------
        
        
        
        #updates urls that are duplicates as such
        #refactor into a separate deduplicate function
        #probably want to convert form to importing all available urls then annotate 
        #convert to return list of urls not list of single tuples, remove [0] in duplicate 
    def get_unannotated_urls(self):
        #connect to db

        sql = "SELECT URL FROM urls WHERE URL NOT IN (SELECT url FROM StorySummaries)"

        self.mycursor.execute(sql)
        unscrapped = self.mycursor.fetchall()
        
        urls = []
        
        #change how this works, dont want to load everything into list, bad form
        for x in unscrapped: 
            #x = article_link[0]#rename x
            same_url = self.check_if_duplicate_url_already_in_story_summaries(x)
            if None == same_url:#no duplicate present
                urls.append(x)
            else:
                url = x
                descriptors = []
                same_stories = []
                exact_duplicates = [same_url]
                summary = "Duplicate"

                print("current url: ",x)
                print("duplicate url: ", same_url)
                self.add_summary_to_db(url, descriptors, same_stories, exact_duplicates, summary)
        return urls
    

    def add_summary_to_db(self, url, descriptors, same_stories, exact_duplicates, summary):
        sql = "INSERT INTO StorySummaries (url, descriptors, same_stories, exact_duplicates, summary) VALUES (%s, %s, %s, %s, %s)"
        val = (url,json.dumps({'descriptors':descriptors}),json.dumps({'same_stories':same_stories}),json.dumps({'exact_duplicates':exact_duplicates}),summary) 
        #("https://www.nytimes.com"+link, "08/20/2019",NewYorkTimes)
        self.mycursor.execute(sql, val)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record inserted.")
                
            
            #should set up system to do this based on parsed text
    def check_if_duplicate_url_already_in_story_summaries(self,url):
        if "washingtonpost.com" in url:
            #not yet tagged
            inner_text = url.split("washingtonpost.com")[1]
            inner_text = inner_text.split(".html")[0]
            inner_text = '%'+inner_text+'%'
            sql = "SELECT url FROM StorySummaries WHERE url LIKE %s"
            val = (inner_text,)
            
            self.mycursor.execute(sql,val)
            duplicates = self.mycursor.fetchall()
            
            #insert general purpose high threshold bag of words checker 
            assert len(duplicates)<2 # if i see more than 1 something has gone wrong, my method of checking for duplication involves checking for known issues 
            if 1 == len(duplicates):
                return duplicates[0][0]
            else: # no matches
                return None
        else: 
            return None
        
        
    def add_url_as_duplicate(self, url_to_add, aready_present_url):
        pass 
        add_summary_to_db(self, url, descriptors, same_stories, exact_duplicates, summary)
        
        
    #return the head 
        
    def identify_duplicate_stories_summaries_db(self):
        
        
        url = current_article
        descriptors = []#['Wilbur Ross','Huawei', 'trade war',"sanctions"]
        same_stories = []#['https://www.washingtonpost.com/politics/trump-again-undercuts-his-administrations-messy-tariffs-rhetoric/2019/08/19/6ca7752a-0a75-46cb-8b5f-096496acc028_story.html']
        exact_duplicates = ['https://www.washingtonpost.com/politics/after-two-more-mass-shootings-trump-again-appears-to-back-away-from-gun-background-checks/2019/08/19/ddbf75e4-c2af-11e9-b72f-b31dfaa77212_story.html']
        summary = "Duplicate" #"Huawei gets another 90 day extention on sanctions"

        db.add_summary_to_db(url, descriptors, same_stories, exact_duplicates, summary)
        'https://www.washingtonpost.com/politics/omar-tlaib-blast-israel-for-blocking-their-visit/2019/08/19/6c0ffda6-c2b9-11e9-850e-c0eef81a5224_story.html'
        'http://washingtonpost.com/politics/omar-tlaib-blast-israel-for-blocking-their-visit/2019/08/19/6c0ffda6-c2b9-11e9-850e-c0eef81a5224_story.html?tid=pm_politics_pop'
    
        if "washingtonpost.com" in url:
            #not yet tagged
            inner_text = url.split("washingtonpost.com")[1]
            inner_text = url.split(".html")[0]
        else:
            11+1
            
    #url varchar(1000), descriptors json, same_stories json, exact_duplicates json, summary varchar(10000), id MEDIUMINT NOT NULL AUTO_INCREMENT,
                
    #change to open new connection
    def open_connection_db(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="pythonuser",
          passwd="password",
          database="newsdatabase"
        ) 
        self.mycursor = self.mydb.cursor(buffered=True) 
        return self.mycursor
