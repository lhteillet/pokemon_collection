import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import base64


st.set_page_config(layout="centered")

# Page title and introduction
st.markdown("# La collection de Manon & Louis")

# Import data
extension_names = ["Forces Temporelles", "Ecarlate et Violet", "Evolution à Paldéa", "Flammes Obsidiennes"]
extension_code = {"Forces Temporelles": "TEF",
                   "Ecarlate et Violet": "SVI", 
                   "Evolution à Paldéa": "PAL", 
                   "Flammes Obsidiennes": "OBF"}
extension_sheet = {"Forces Temporelles": "forces_temporelles",
                   "Ecarlate et Violet": "ecarlate_et_violet", 
                   "Evolution à Paldéa": "evolutions_a_paldea", 
                   "Flammes Obsidiennes": "flammes_obsidiennes"}

selected_extension = st.sidebar.selectbox("Sélectionnez une extension", extension_names)
selected_code = extension_code[selected_extension]

pokemon_cards = pd.read_excel("collection.xlsx", sheet_name = extension_sheet[selected_extension])
pokemon_names = pd.read_csv(f"{extension_sheet[selected_extension]}.csv", sep=",")

pokemon_cards = pokemon_cards.merge(pokemon_names, left_on="id", right_on="ID")
pokemon_cards = pokemon_cards[["id","Name","type","rareté","nb"]]
pokemon_cards = pokemon_cards.sort_values(by="id")
pokemon_cards["image_url"] = pokemon_cards.apply(lambda x : f"https://www.pokecardex.com/assets/images/sets/{selected_code}/HD/{x.id}.jpg", axis=1)

# Multiselect for filtering by rarity
rarities = pokemon_cards['rareté'].unique()
selected_rarities = st.multiselect("Sélectionnez les raretés", options=rarities, default=rarities)


filtered_cards = pokemon_cards[pokemon_cards['rareté'].isin(selected_rarities)]

# Displaying the filtered data
st.markdown("### Cartes Pokémon")
# Configure grid options using GridOptionsBuilder
builder = GridOptionsBuilder.from_dataframe(filtered_cards)
builder.configure_pagination(enabled=True)
builder.configure_selection(selection_mode='single', use_checkbox=False)
grid_options = builder.build()

# Display AgGrid
return_value = AgGrid(filtered_cards, gridOptions=grid_options)
if return_value['selected_rows'] is not None:
    system_name = return_value['selected_rows']["image_url"]
    st.image(system_name.iloc[0])
else:
    st.write("No row selected")

# Footer
st.markdown("## Contactez-nous")
st.markdown("Pour toute question ou suggestion, n'hésitez pas à nous contacter à [louis.teillet.03@gmail.com](mailto:louis.teillet.03@gmail.com).")

