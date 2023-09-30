import numpy as np
import random
import pickle
from loader import load_data, load_content_scores

def collab_recommend_restaurants(user_id):

    idx2business, user2idx, model, user_cache = load_data()

    if user_id in user_cache.keys():
        sorted_scores = user_cache[user_id]

    else:
        scores = {}
        useridx = user2idx[user_id]
        
        for business_id, business in idx2business.items():
            pred = model.predict([np.array([useridx]), np.array([business_id])])
            scores[business] = pred

        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        user_cache[user_id] = sorted_scores
        with open('saved/recommendation_cache.pickle', 'wb') as f:
            pickle.dump(user_cache, f)

    top_25 = sorted_scores[:25]
    top_25 = [t[0] for t in top_25]
    top_10_restaurents = random.sample(top_25, 10)
    return top_10_restaurents

def hybrid_recommend_restaurants(user_id, business_id):

    content_based_scores = load_content_scores()
    business_pool = content_based_scores[business_id].sort_values(ascending=False)[:30].index

    idx2business, user2idx, model, user_cache = load_data()
    scores = {}
    useridx = user2idx[user_id]
    
    for business_id, business in idx2business.items():
        if business in business_pool:
            pred = model.predict([np.array([useridx]), np.array([business_id])])
            scores[business] = pred

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_12 = sorted_scores[:12]
    top_12 = [t[0] for t in top_12]
    top_6_restaurants = random.sample(top_12, 6)
    return top_6_restaurants