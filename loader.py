import pickle
import csv
from model import create_collab_model

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

def load_content_scores():
    with open('saved/content_based_scores.pickle', 'rb') as b:
        content_based_scores = pickle.load(b)
    return content_based_scores

def load_data():
    business_encoder, user_encoder, num_businesses, num_users = load_encoders()
    business2idx, idx2business, user2idx, idx2user = create_dict(business_encoder, user_encoder)
    collab_model = create_collab_model(num_businesses, num_users)
    collab_model.load_weights('saved/model_weights.h5')
    user_cache = load_cache()
    return idx2business, user2idx, collab_model, user_cache


def get_restaurant_data(restaurents):
    restaurant_data = []

    with open('dataset/processed/business.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            restaurant_id = row['business_id']
            if restaurant_id in restaurents:
                restaurant_name = row['name']
                restaurant_rating = row['stars']
                restaurant_address = row['address']
                restaurant_hours = row['hours']
                restaurant_image_url = "https://i.pinimg.com/736x/1c/53/c5/1c53c5b3f3c6e788bfd32f2b4d54ed59.jpg"  # If you have an 'image_url' column

                restaurant_data.append({
                                'id': restaurant_id,
                                'name': restaurant_name,
                                'rating': restaurant_rating,
                                'image_url': restaurant_image_url,
                                'address': restaurant_address,
                                'hours': restaurant_hours
                            })
    return restaurant_data

if __name__=='__main__':
    business_encoder, user_encoder, num_businesses, num_users = load_encoders()
    print(business_encoder)