import pickle

def load_encoders():
    with open('saved/business_encoder.pickle', 'rb') as b:
        business_encoder = pickle.load(b)

    with open('saved/user_encoder.pickle', 'rb') as b:
        user_encoder = pickle.load(b)
    
    return business_encoder, user_encoder, len(business_encoder.classes_), len(user_encoder.classes_)


def create_dict(business_encoder, user_encoder):
    business2idx = dict(zip(business_encoder.classes_, business_encoder.transform(business_encoder.classes_)))
    idx2business = dict(zip(business_encoder.transform(business_encoder.classes_), business_encoder.classes_))

    user2idx = dict(zip(user_encoder.classes_, user_encoder.transform(user_encoder.classes_)))
    idx2user = dict(zip(user_encoder.transform(user_encoder.classes_), user_encoder.classes_))

    return business2idx, idx2business, user2idx, idx2user

def load_cache():
    try:
        with open('saved/recommendation_cache.pickle', 'rb') as b:
            user_cache = pickle.load(b)
    except:
        user_cache = {}
    return user_cache