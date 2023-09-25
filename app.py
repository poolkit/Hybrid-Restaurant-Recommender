from flask import Flask, render_template, request, redirect
from recommend import collab_recommend_restaurants
from loader import load_cache, load_encoders, create_dict, get_restaurant_data
from model import create_collab_model
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

loaded = False
def load_data():
    global loaded, collab_model, num_businesses, num_users, business2idx,  idx2business, user2idx, idx2user, user_cache

    if not loaded:
        business_encoder, user_encoder, num_businesses, num_users = load_encoders()
        business2idx, idx2business, user2idx, idx2user = create_dict(business_encoder, user_encoder)
        collab_model = create_collab_model(num_businesses, num_users)
        collab_model.load_weights('saved/model_weights.h5')
        user_cache = load_cache()

        loaded = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    user_id = request.form['UserID']
    return redirect(f'/recommendations/{user_id}')

# @app.route('/search', methods=['POST'])
# def search_restaurants():
#     selected_options = request.json.get('options', [])
#     return redirect(f'/recommendations/{user_id}')

@app.route('/recommendations/<user_id>')
def show_recommendations(user_id):
    load_data()
    top_10_restaurants = collab_recommend_restaurants(user_id, collab_model, idx2business, user2idx, user_cache)
    recommended_restaurants = get_restaurant_data(top_10_restaurants)
    return render_template('recommendations.html', recommended_restaurants=recommended_restaurants)
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)

# load_data()
# x = collab_recommend_restaurants('mh_-eMZ6K5RLWhZyISBhwA', collab_model, idx2business, user2idx, user_cache)
# x = get_restaurant_data(x)
# print(x)