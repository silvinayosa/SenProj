import pandas as pd
import numpy as np
import sqlite3
# connect db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()

venue_data = pd.read_sql_query("SELECT * FROM venue", conn)
cost_data = pd.read_sql_query("SELECT * FROM cost", conn)


# Load the datasets
# cost_data = pd.read_csv('/content/cost.csv')
# venue_data = pd.read_csv('/content/venue.csv')

# Extract the necessary columns from cost_data
cost_subset = cost_data[['Longitude', 'Latitude', 'Facility_Name']]
cost_subset = cost_subset.rename(columns={'Name': 'Facility_Name'})

# Add the required columns with the specified values
cost_subset['Prov_Terr'] = 'bc'
cost_subset['ODRSF_facility_type'] = 'studio'

# Concatenate the new data to the venue_data
updated_venue_data = pd.concat([venue_data, cost_subset], ignore_index=True)

# Save the updated venue data to a new CSV file
updated_venue_data.to_csv('updated_venue.csv', index=False)

print("finish")

"""GAN Model"""

import pandas as pd
import numpy as np
import tensorflow as tf
from keras import layers
from sklearn.preprocessing import MinMaxScaler


venue_data = pd.read_sql_query("SELECT * FROM venue", conn)
cost_data = pd.read_sql_query("SELECT * FROM cost", conn)

# Load the datasets
# cost_data = pd.read_csv('/content/cost.csv')
# venue_data = pd.read_csv('/content/updated_venue.csv')

# Preprocess the 'Price' column to remove '$' and convert to float
cost_data['Price'] = cost_data['Price'].replace('[\$,]', '', regex=True).astype(float)

# Merge the data on 'Latitude' and 'Longitude'
merged_data = pd.merge(venue_data, cost_data, on=['Latitude', 'Longitude'], how='left')

# Prepare data for GAN training
data = merged_data[['Latitude', 'Longitude', 'Price']].dropna().values

# Normalize the data
scaler = MinMaxScaler()
data = scaler.fit_transform(data)

# GAN model definition
def build_generator():
    model = tf.keras.Sequential([
        layers.Dense(128, activation='relu', input_dim=2),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='linear')
    ])
    return model

def build_discriminator():
    model = tf.keras.Sequential([
        layers.Dense(128, activation='relu', input_dim=3),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

generator = build_generator()
discriminator = build_discriminator()

discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Combined GAN model
discriminator.trainable = False

gan_input = layers.Input(shape=(2,))
generated_price = generator(gan_input)
gan_output = discriminator(tf.concat([gan_input, generated_price], axis=1))

gan = tf.keras.Model(gan_input, gan_output)
gan.compile(optimizer='adam', loss='binary_crossentropy')

# Training the GAN
def train_gan(gan, generator, discriminator, data, epochs=10000, batch_size=64):
    for epoch in range(epochs):
        # Train discriminator
        indices = np.random.randint(0, data.shape[0], batch_size)
        real_data = data[indices]
        noise = np.random.normal(0, 1, (batch_size, 2))
        generated_data = generator.predict(noise)

        combined_real_data = np.hstack((real_data[:, :2], real_data[:, 2:]))
        combined_fake_data = np.hstack((noise, generated_data))

        X = np.vstack((combined_real_data, combined_fake_data))
        y = np.zeros(2 * batch_size)
        y[:batch_size] = 0.9

        discriminator.trainable = True
        d_loss = discriminator.train_on_batch(X, y)

        # Train generator
        noise = np.random.normal(0, 1, (batch_size, 2))
        y_gen = np.ones(batch_size)

        discriminator.trainable = False
        g_loss = gan.train_on_batch(noise, y_gen)

        if epoch % 1000 == 0:
            print(f'Epoch: {epoch}, D Loss: {d_loss[0]}, G Loss: {g_loss}')

train_gan(gan, generator, discriminator, data)

# Generate synthetic price data
def generate_synthetic_data(generator, num_samples):
    noise = np.random.normal(0, 1, (num_samples, 2))
    synthetic_prices = generator.predict(noise)
    return scaler.inverse_transform(np.hstack((noise, synthetic_prices)))

synthetic_data = generate_synthetic_data(generator, len(venue_data))

# Create the output DataFrame
synthetic_df = pd.DataFrame(synthetic_data, columns=['Latitude', 'Longitude', 'Price'])
synthetic_df['Name'] = venue_data['Facility_Name']

# Save the synthetic data to a new CSV file
synthetic_df.to_csv('synthetic_cost_data.csv', index=False)

synthetic_df['Price'] = synthetic_df['Price'].abs()
synthetic_df['Price'] = synthetic_df['Price'].astype(int)
synthetic_df.to_csv('synthetic_cost_data.csv', index=False)
