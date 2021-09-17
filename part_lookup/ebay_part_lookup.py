


from ebaysdk.finding import Connection as Finding
from dotenv import load_dotenv
import collections
import time
import traceback
import string
import os

from .constants import *

load_dotenv()

EBAY_APPID = os.getenv('EBAY_APPID')

def create_ebay_filter(part_number,results_limit):
    return {
            'keywords': str(part_number),
                'itemFilter': [
                    
                ],
                'paginationInput': {
                    'entriesPerPage': results_limit,
                    'pageNumber': 1
                }
    }

def get_ebay_data(part_number,num_results):

    api = Finding(appid=EBAY_APPID, config_file=None)
    response = api.execute('findItemsAdvanced', create_ebay_filter(part_number,num_results))
    data = response.dict()
    results = data['searchResult']
    count = int(results['_count'])
    if (count==0): 
        return ([],0)
    return (results['item'],count)

def extract_part_data_from_titles(titles,part_number,manufacturers=[],blacklist=[]):

    #helper function for filtering a list of tuples
    def filter_kv_pairs(kv_pair_list,func):
        return [(k,v) for k,v in kv_pair_list if func(k,v)]

    # create list of all the words in the titles
    # titles=[]
    words = ' '.join(titles).split(' ')
    words = [w.upper() for w in words]

    # create frequency map of all words in titles (list of (word,frequency))
    # Note: this respects the order in which words were seen
    
    counts = collections.OrderedDict()

    for title in titles:
        for word in title.split(' '):
            word=word.upper()
            word=word.rstrip(string.punctuation)
            if word in counts:
                counts[word]+=1
            else:
                counts[word]=1

    word_counts=counts.items()

    title_exclude_list = manufacturers+blacklist+[part_number]

    #if in half of the results, word is probably relevant
    relevance_count = len(titles) // 2


    #relevant words
    s_words = filter_kv_pairs(word_counts, lambda _,count: count > relevance_count)
    #list of manufacturer names found
    s_manufacturers = filter_kv_pairs(s_words,lambda word,_: word in manufacturers)    
    s_manufacturers.sort(key=lambda m:m[1],reverse=True)

    #filter out manufacturer words, words from blacklist, and part number
    s_words = filter_kv_pairs(s_words,lambda word,_: word not in title_exclude_list)

    title = " ".join([word for word,value in s_words]) if s_words else None
    manufacturer = s_manufacturers[0][0] if s_manufacturers else None

    return {
        'title':title,
        'manufacturer':manufacturer,
        'part_number':part_number,
    }

def find_part_data_on_ebay(part_number:str):

    try:

        data, num_results = get_ebay_data(part_number,10)

    except Exception as e:
        print(e)
        return {'error':True, 'message':'ebay API error'}

    if not data:

        return {'error':False,'data_found':False,'data':None}
    
    # print(num_results)

    titles = [item['title'] for item in data]

    extracted_data = extract_part_data_from_titles(titles,part_number,MANUFACTURERS,WORD_FILTER)
    
    return {
        'error':False,
        'data_found':True,
        'data':extracted_data,
        'meta':
            {
                'results_found':num_results,
            }
        }


if __name__=="__main__":

    part_number='94001-08000-0S' 
    print(find_part_data_on_ebay(part_number))
