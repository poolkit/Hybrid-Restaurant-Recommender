from flask import Flask, render_template, request, redirect, flash
from recommend import collab_recommend_restaurants, hybrid_recommend_restaurants
from model import create_collab_model
from loader import get_restaurant_data
import warnings
import secrets
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    user_id = request.form['UserID']
    if not user_id:
        flash('UserID cannot be empty.', 'error')
        return redirect('/')
    return redirect(f'/recommendations/{user_id}')

@app.route('/recommendations/<user_id>')
def show_recommendations(user_id):
    top_10_restaurants = collab_recommend_restaurants(user_id)
    recommended_restaurants = get_restaurant_data(top_10_restaurants)
    return render_template('recommendations.html', recommended_restaurants=recommended_restaurants, user_id=user_id)

@app.route('/search', methods=['POST'])
def search_restaurants():
    selected_options = request.form.getlist('option')
    return render_template('search.html', selected_options=', '.join(selected_options))

@app.route('/restaurant/<restaurant_id>')
def restaurant_page(restaurant_id):
    restaurant_data = get_restaurant_data([restaurant_id])
    user_id = request.args.get('user_id')
    top_6_restaurants = hybrid_recommend_restaurants(user_id, restaurant_id)
    top_6_restaurants = get_restaurant_data(top_6_restaurants)
    restaurant = {
        'id': restaurant_id,
        'name': restaurant_data[0]['name'],
        'rating': restaurant_data[0]['rating'],
        'address': restaurant_data[0]['address'],
        'hours': restaurant_data[0]['hours'],
        'image_url': restaurant_data[0]['image_url']
        # Add other restaurant details here
    }
    return render_template('restaurant.html', restaurant=restaurant, top_6_restaurants=top_6_restaurants, user_id=user_id)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)

# load_data()
# x = collab_recommend_restaurants('mh_-eMZ6K5RLWhZyISBhwA', collab_model, idx2business, user2idx, user_cache)
# x = get_restaurant_data(x)
# print(x)
