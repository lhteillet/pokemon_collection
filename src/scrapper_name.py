import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape
url = "https://example.com/pokemon-page"  # Replace with the actual URL

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty dictionary to store the Pokémon data
pokemon_dict = {}

# Find all the relevant divs
divs = soup.find_all('div', class_='serie-details-carte')

# Loop through each div and extract the ID, Pokémon name, and image URL
for div in divs:
    # Get the anchor tag within the div
    a_tag = div.find('a')
    if a_tag:
        # Extract the title attribute
        title = a_tag.get('title')
        if title:
            # Split the title to get the ID and Pokémon name
            parts = title.split()
            if len(parts) > 1:
                # Extract the ID and name
                id_part = parts[-1].split('/')[0]
                name_part = " ".join(parts[:-1])
                
                # Get the image tag
                img_tag = div.find('img')
                if img_tag:
                    # Extract the data-original attribute for the image URL
                    img_url = img_tag.get('data-original')
                    
                    # Add to the dictionary
                    pokemon_id = int(id_part)
                    pokemon_dict[pokemon_id] = {'name': name_part, 'image_url': img_url}

# Convert the dictionary to a DataFrame
pokemon_df = pd.DataFrame.from_dict(pokemon_dict, orient='index').reset_index()
pokemon_df.columns = ['ID', 'Name', 'Image URL']

# Save the DataFrame to a CSV file
pokemon_df.to_csv('pokemon_collection.csv', index=False)

print("Dictionary saved to pokemon_collection.csv")
