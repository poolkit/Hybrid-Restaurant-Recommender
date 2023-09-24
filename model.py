from keras.layers import Embedding, Flatten, Input, Dot, Concatenate, Dense, Dropout, BatchNormalization
from keras.models import Model
from keras.regularizers import l2

def create_collab_model(num_businesses, num_users):
    embedding_dim=32

    user_input = Input(shape=(1,), name='user_input')
    business_input = Input(shape=(1,), name='business_input')

    user_embedding = Embedding(input_dim=num_users, output_dim=embedding_dim, embeddings_regularizer=l2(1e-6))(user_input)
    business_embedding = Embedding(input_dim=num_businesses, output_dim=embedding_dim, embeddings_regularizer=l2(1e-6))(business_input)

    user_flatten = Flatten()(user_embedding)
    business_flatten = Flatten()(business_embedding)

    merged = Concatenate()([user_flatten, business_flatten])
    merged = BatchNormalization()(merged)

    dense_layer = Dense(128, activation='relu')(merged)
    dropout = Dropout(0.4)(dense_layer)
    output_layer = Dense(1, activation='linear')(dropout)

    model = Model(inputs=[user_input, business_input], outputs=output_layer)
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

    return model