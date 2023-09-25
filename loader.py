import pickle
import csv

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

def get_restaurant_data(restaurents):

    restaurant_data = []

    with open('dataset/processed/business.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            restaurant_id = row['business_id']
            if restaurant_id in restaurents:
                restaurant_name = row['name']
                restaurant_rating = row['stars']
                restaurant_image_url = "https://i.pinimg.com/736x/1c/53/c5/1c53c5b3f3c6e788bfd32f2b4d54ed59.jpg"  # If you have an 'image_url' column

                restaurant_data.append({
                                'name': restaurant_name,
                                'rating': restaurant_rating,
                                'image_url': restaurant_image_url
                            })
    return restaurant_data