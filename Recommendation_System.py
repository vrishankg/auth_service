import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from scipy.spatial import distance
import numpy as np
import requests
import json

restaurant_url = 'http://127.0.0.1:5000/get_restaurants'
response1 = requests.get(restaurant_url)

users_url = 'http://127.0.0.1:5000/get_users?name=Alice'
response2 = requests.get(users_url)

# data_dict = json.loads(response1)
data_dict = response1.json()

restaurants = pd.DataFrame(data_dict['restaurants'])

# data_dict1 = json.loads(response2)
data_dict1 = response2.json()
# print(data_dict1['users'][0])
user_preferences = data_dict1['users'][0]

# if response1.status_code == 200:
#     # Convert the JSON response to a DataFrame
#     restaurant_data = response1.json()
#     restaurants = pd.DataFrame(restaurant_data)

#     # Display the DataFrame
#     # print(restaurants)
# else:
#     print(f"Error: {response1.status_code}, {response1.text}")

# if response2.status_code == 200:
#     # Convert the JSON response to a DataFrame
#     user_data = response2.json()
#     user_preferences = pd.DataFrame(user_data)

#     # Display the DataFrame
#     # print(users)
# else:
#     print(f"Error: {response2.status_code}, {response2.text}")

# restaurants = pd.DataFrame({
#     'name': ['The Gourmet Spot', 'Family Feast', 'Vegan Delight', 'Quick Bites', 'Fine Dine In'],
#     'preferred_cuisines': ['Italian', 'American', 'Vegan', 'Fast Food', 'French'],
#     'price_range': ['$$', '$', '$$', '$', '$$$$'],
#     'city': ['Raleigh', 'Raleigh', 'Raleigh', 'Raleigh', 'Raleigh'],
#     'state': ['NC', 'NC', 'NC', 'NC','NC'],
#     'coordinates': [(35.7796, -78.6382), (35.7796, -78.6382), (35.7796, -78.6382), (35.7796, -78.6382), (35.7796, -78.6382)],
#     'preferred_ambiance': ['Romantic', 'Casual', 'Quiet', 'Casual', 'Elegant'],
#     'Dietary Restrictions': ['None', 'None', 'Vegan', 'None', 'None'] ,
#     'menu_url': ['http://example.com/restaurant1/menu','http://example.com/restaurant2/menu','http://example.com/restaurant2/menu','http://example.com/restaurant2/menu','http://example.com/restaurant2/menu']
# })


# user_preferences = {
#     'id': 'user_name',
#     'name': 'John',
#     'preferred_cuisines': ['Italian'],  
#     'budget': '$$',
#     'preferred_ambiance': 'Quiet',
#     'location_preference': (35.7796, -78.6382),
#     'Dietary Restrictions': ['Vegan'], 
#     'city': 'Raleigh',  
#     'state': 'NC'  ,
#     'preferred_language': 'es',
# }



enc = OneHotEncoder()
restaurant_features = enc.fit_transform(restaurants[['preferred_cuisines', 'budget', 'city', 'state', 'preferred_ambiance', 'dietary_restrictions']]).toarray()

# Convert user_preferences to DataFrame and transform
user_preferences_adjusted = {
    'preferred_cuisines': user_preferences['preferred_cuisines'][0],  
    'budget': user_preferences['budget'],  
    'city': user_preferences['city'],  
    'state': user_preferences['state'],  
    'preferred_ambiance': user_preferences['preferred_ambiance'], 
    'dietary_restrictions': user_preferences['dietary_restrictions'][0]
}
user_df_adjusted = pd.DataFrame([user_preferences_adjusted])
user_features = enc.transform(user_df_adjusted).toarray()

# Calculate cosine similarity for categorical features
similarity_scores = cosine_similarity(user_features, restaurant_features)

# Calculate Euclidean distance for coordinates
user_location = np.array(user_preferences['location_preference'])
restaurant_locations = np.stack(restaurants['coordinates'])
location_distances = distance.cdist([user_location], restaurant_locations, 'euclidean')[0]

# Normalize distances
max_distance = np.max(location_distances)
normalized_distances = location_distances / max_distance

# Combine similarity score and location distance (with a weight, here 0.5 for demonstration)
total_similarity_score = similarity_scores[0] - 0.5 * normalized_distances

# Add similarity score to DataFrame
restaurants['similarity_score'] = total_similarity_score

# Sort restaurants based on similarity score
recommended_restaurants = restaurants.sort_values(by='similarity_score', ascending=False)

# Display top N recommendations
N = 3
print(recommended_restaurants.head(N))

