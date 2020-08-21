
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import requests_with_caching
import json

parameters = dict()
def get_movies_from_tastedive(movie_name) :
    parameters['q'] = movie_name
    parameters['type'] = 'movies'
    parameters['limit'] = '5'
    res = requests_with_caching.get('https://tastedive.com/api/similar', params = parameters) 
    result = json.loads(res.text)
    print(result)
    return result

def extract_movie_titles(result) :
     return [each['Name'] for each in result['Similar']['Results']]

movie_title_list = list()    
def get_related_titles(movie_list) :
    if(len(movie_list) == 0) :
        return []
    for each_movie in movie_list :
        each_movie_title_list = extract_movie_titles(get_movies_from_tastedive(each_movie))
        for each_title in each_movie_title_list :
            if(movie_title_list.count(each_title) == 0) :
                movie_title_list.append(each_title)
    return movie_title_list

parameters2 = dict()
def get_movie_data(title) :
    parameters2['t'] = title
    parameters2['r'] = 'json'
    res = requests_with_caching.get('http://www.omdbapi.com/', params = parameters2) 
    result = json.loads(res.text)
    return result
    
def get_movie_rating(rating = get_movie_data("Deadpool 2")) :
    temp_list = rating['Ratings']
    for each in temp_list :
        if(each['Source'] == 'Rotten Tomatoes') :
            return int(each['Value'][:2])
    return 0 

input_movie_list = ['Deadpool 2', 'Black Panther']
def get_sorted_recommendations(input_movie_list) :
    movie_list = get_related_titles(input_movie_list)
    movie_list.sort()
    
    recom = dict()
    for each in movie_list :
        rating = get_movie_rating(get_movie_data(each))
        recom[each] = rating
    
    lst = sorted(recom.items(), key = lambda x: x[1], reverse = True)
    print(lst)
    final_list = list()
    for each in lst:
        final_list.append(each[0])
    return final_list
                                                     
    
    