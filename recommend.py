import numpy as np
import random
import pickle

def collab_recommend_restaurants(user_id, model, idx2business, user2idx, user_cache):

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