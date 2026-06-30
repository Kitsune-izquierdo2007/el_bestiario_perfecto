from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")


def load_all_creatures():

    creatures = []

    if not os.path.exists(DATA_FOLDER):
        return creatures

    for filename in os.listdir(DATA_FOLDER):

        if filename.endswith(".json"):

            path = os.path.join(DATA_FOLDER, filename)

            try:

                with open(path, "r", encoding="utf-8") as file:

                    data = json.load(file)

                    if isinstance(data, list):
                        creatures.extend(data)

            except Exception as e:

                print(f"ERROR EN {filename}")
                print(e)

    return creatures


@app.route("/")
def index():

    creatures = load_all_creatures()

    return render_template(
        "index.html",
        creatures=creatures
    )


@app.route("/creature/<int:id>")
def creature(id):

    creatures = load_all_creatures()

    selected = next(
        (c for c in creatures if c["id"] == id),
        None
    )

    if not selected:

        return "Criatura no encontrada", 404

    return render_template(
        "creature.html",
        creature=selected
    )


@app.route("/mythology/<name>")
def mythology(name):

    file_path = os.path.join(
        DATA_FOLDER,
        f"{name.lower()}.json"
    )

    if not os.path.exists(file_path):

        return "Mitología no encontrada", 404

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            creatures = json.load(file)

    except Exception as e:

        return f"Error leyendo {name}.json: {e}"

    return render_template(
        "index.html",
        creatures=creatures
    )


@app.route("/search")
def search():

    query = request.args.get(
        "q",
        ""
    ).lower()

    creatures = load_all_creatures()

    results = []

    for creature in creatures:

        if query in creature["name"].lower():

            results.append(creature)

    return render_template(
        "index.html",
        creatures=results
    )


@app.route("/rarity/<rarity>")
def rarity():

    rarity_name = request.view_args["rarity"]

    creatures = load_all_creatures()

    results = []

    for creature in creatures:

        if creature["rarity"].lower() == rarity_name.lower():

            results.append(creature)

    return render_template(
        "index.html",
        creatures=results
    )


@app.errorhandler(404)
def page_not_found(error):

    return (
        "<h1>404</h1><p>Página no encontrada.</p>",
        404
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )