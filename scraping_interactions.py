from misc_helper_funcs_and_constants import *
from database_interactions import *  
from local_file_interactions import * 

def scrape_section_for_urls(outlet,section_identifier,url_storage):
    http = urllib3.PoolManager()

    response = http.request('GET', url_storage[outlet][section_identifier])
    soup = BeautifulSoup(response.data)
    #print(soup.prettify())
    s = soup.find_all('a', href=True)

    valid_links = []
    for link in s:
        #keep non text pages out 
        if link['href'].find('politics') != -1 and link['href'].find('.html') != -1 and link['href'].find('/interactive/') == -1 and link['href'].find('/video/') == -1 and link['href'].find('index.html') == -1:
            if link['href'] not in valid_links:
                valid_links.append(link['href'])
    return valid_links

def scrape_outlets_for_urls(url_storage):
    for outlet in url_storage:
        for sec_url_pair in url_storage[outlet]:
            pass
#def convert_urls():
#    pass



#refactor so im not directely indexing response tuples
#update the section here
def scrape_unscraped_articles():
    lf = LocalFileHandler()
    db = DatabaseManager()

    unscrapped_articles = db.get_unscraped_urls_from_db()
    doc_status = "Raw"
    category = "Politics"
    #REPLACE HARDCODES
    for article in unscrapped_articles:
        url = article[1]
        
        date = db.get_date_for_url_db(url)
        outlet = db.get_outlet_for_url_db(url)
        organizational_path = lf.generate_organizational_path(doc_status,outlet,category,date)
        file_path=lf.find_absolute_file_path(organizational_path) #directory structure above the file without the name
        
        #REEPLACE POLITICS HARDCODE
        
        raw_text = scrape_article_for_raw_text(outlet,category,url)        
        filename = lf.convert_url_to_filename(url)
        
        lf.update_path_structure(organizational_path) #create file hirarchy, takes only organization as input
        lf.write_text_to_location(raw_text,filename,file_path)
        
        file_loc=lf.find_absolute_document_location(organizational_path,filename) #directory structure with file name
        db.set_path_for_file_db(url, file_loc)
        
        db.mark_url_as_scraped_db(url)
        print("test complete for: ")
        print(url)
        #break #for testing 1 update
        time.sleep(60+random.randrange(0,60))

        #move raw below the date
        
def scrape_article_for_raw_text(outlet,section,url):
    http = urllib3.PoolManager()

    response = http.request('GET', url)
    soup = BeautifulSoup(response.data)
    #print(soup.prettify())
    return str(soup)
