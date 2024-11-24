from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Extension Data
extension_names = ["Forces Temporelles", "Ecarlate et Violet", "Evolution à Paldéa", "Flammes Obsidiennes"]
extension_code = {
    "Forces Temporelles": "TEF",
    "Ecarlate et Violet": "SVI",
    "Evolution à Paldéa": "PAL",
    "Flammes Obsidiennes": "OBF"
}
extension_sheet = {
    "Forces Temporelles": "forces_temporelles",
    "Ecarlate et Violet": "ecarlate_et_violet",
    "Evolution à Paldéa": "evolutions_a_paldea",
    "Flammes Obsidiennes": "flammes_obsidiennes"
}

# Load Data Function
def load_data(selected_extension):
    pokemon_cards = pd.read_excel(
        "./data/collection.xlsx",
        sheet_name=extension_sheet[selected_extension]
    )
    pokemon_names = pd.read_csv(
        f"./data/extension_pokemon_id/{extension_sheet[selected_extension]}.csv", 
        sep=","
    )
    pokemon_cards = pokemon_cards.merge(pokemon_names, left_on="id", right_on="ID")
    pokemon_cards = pokemon_cards[["id", "Name", "type", "rareté", "nb"]]
    pokemon_cards = pokemon_cards.sort_values(by="id")
    selected_code = extension_code[selected_extension]
    pokemon_cards["image_url"] = pokemon_cards.apply(
        lambda x: f"https://www.pokecardex.com/assets/images/sets/{selected_code}/HD/{x.id}.jpg", axis=1
    )
    return pokemon_cards

@app.route("/")
def home():
    return render_template("index.html", extensions=extension_names)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Add authentication logic here
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/cards", methods=["GET"])
def display_cards():
    selected_extension = request.args.get("extension")
    rarities_filter = request.args.getlist("rarities")
    
    pokemon_cards = load_data(selected_extension)
    rarities = pokemon_cards['rareté'].unique().tolist()
    filtered_cards = pokemon_cards[pokemon_cards['rareté'].isin(rarities_filter or rarities)]
    return render_template("filtered_cards.html", cards=filtered_cards, rarities=rarities, extension=selected_extension)

@app.route("/image_url", methods=["POST"])
def get_image_url():
    card_id = request.json.get("card_id")
    extension = request.json.get("extension")
    pokemon_cards = load_data(extension)
    image_url = pokemon_cards[pokemon_cards['id'] == int(card_id)]["image_url"].iloc[0]
    return jsonify({"image_url": image_url})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        # Add registration logic here
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        # Add password reset logic here
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

if __name__ == "__main__":
    app.run(debug=True)
