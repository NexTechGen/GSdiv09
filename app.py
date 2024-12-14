from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, ConfigurationError
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = (
    "mongodb+srv://Ruzait:2023ET139@cluster0.loq8v.mongodb.net/testAPI?retryWrites=true&w=majority&appName=Cluster0"
)
app.secret_key = 'your_secret_key_here'

try:
    mongo = PyMongo(app)
    # Test the connection during initialization
    mongo.cx.admin.command("ping")
    print("Connected to MongoDB successfully.")
except ConnectionFailure as e:
    mongo = None
    print(f"MongoDB connection failed\n Contact Admin Mr.Ruzaid Ahamed")
except ConfigurationError as e:
    print(f"Configuration error: {e}\n Contact Admin Mr.Ruzaid Ahamed")
except Exception as e:
    print(f"An error occurred: {e}\n Contact Admin Mr.Ruzaid Ahamed")

def update_ages():
    """
    Function to automatically update the age of all persons in the database.
    """
    current_date = datetime.now()
    persons = mongo.db.persons.find()
    kids = mongo.db.kids.find()

    for person in persons:
        if 'dob' in person:
            try:
                dob = datetime.strptime(person['dob'], "%Y-%m-%d")  # Ensure DOB is in 'YYYY-MM-DD' format
                age = (current_date - dob).days // 365
                mongo.db.persons.update_one({'_id': person['_id']}, {'$set': {'age': age}})
            except Exception as e:
                """ print(e) """
                pass

    for kid in kids:
        if 'dob' in kid:
            try:
                dob = datetime.strptime(kid['dob'], "%Y-%m-%d")  # Ensure DOB is in 'YYYY-MM-DD' format
                age = (current_date - dob).days // 365
                mongo.db.kids.update_one({'_id': kid['_id']}, {'$set': {'age': age}})
            except Exception as e:
                """ print(e) """
                pass


@app.route("/", methods=["GET", "POST"])
def index():
    update_ages()   
    if request.method == "POST":
        input_value = request.form["input_value"].upper().strip()
        house_number = mongo.db.houses.find_one({"house number": input_value})
        personNIC = mongo.db.persons.find_one({"nic": input_value})

        if house_number:
            person_data = mongo.db.persons.find({"house number": house_number["house number"]})
            kids_data = mongo.db.kids.find({"house number": house_number["house number"]})
            kidslist = []
            for kid in kids_data:
                kidslist.append(kid)
            return render_template("housNper.html", houseData=house_number, persons=person_data, kidsData=kidslist)

        elif personNIC:
            person_data = mongo.db.persons.find({"house number": personNIC["house number"]})
            house_data = mongo.db.houses.find_one({"house number": personNIC["house number"]})
            kids_data = mongo.db.kids.find({"house number": house_data["house number"]})
            return render_template("housNper.html", houseData=house_data, persons=person_data, kidsData=kids_data)

        else:
            return render_template("index.html", error="No data found")

    return render_template("index.html")

@app.route("/view_house/<house_id>", methods=['GET'])
def view_house(house_id):
    # Retrieve the house document
    house = mongo.db.houses.find_one({"_id": ObjectId(house_id)})
    if not house:
        flash("The requested house does not exist.", "danger")
        return redirect(url_for("index"))

    # Retrieve related persons and kids data
    persons = mongo.db.persons.find({"house number": house["house number"]})
    kids = mongo.db.kids.find({"house number": house["house number"]})
    kidslist = [kid for kid in kids]

    # Render the template with house data
    return render_template("housNper.html", houseData=house, persons=persons, kidsData=kidslist)


@app.route("/edit_house/<house_id>", methods=['GET', 'POST'])
def edit_house(house_id):
    # Retrieve the house document from the database using the house ID
    house = mongo.db.houses.find_one({"_id": ObjectId(house_id)})
    
    # List of family type options for the dropdown
    family_type_options = ["Usual Parent Family", "Single Mother Family", "Single Father Family", "No Parent Family"]
    house_type = ["No House", "Permenent House", "Semi Permanent House", "Temporary House"]
    land_size = ["No House", "500 Square Feet Of More", "Less then 500 Square Feet"]
    water_source = ["Water Board Pipe Supply", "Tube Water", "Bottled Water", "Water Supply and Well"]
    electricity = ["Ceylon Electricity Board", "Solar", "Solar and CEB"]
    toilet = ["Inside - Single Use", "Inside - Sharing with families", "No Toilet Facilities", "Outside - Single Use", "Publick Toilet"]


    if request.method == "POST":

        try:
            # Convert family income to an integer (in rupees)
            family_income = int(request.form.get("monthly_family_income", 0))  # Default to 0 if not provided
            family_expenditure = int(request.form.get("monthly_family_expenditure", 0))
            ceb =  int(request.form.get("electricity_consumption", 0))
            total_vehicles =  int(request.form.get("total_vehicles", 0))
            total_lands =  float(request.form.get("total_paddy_lands", 0))
        except ValueError:
            flash("ADD-9(Type Error):Enter Numerical value for Numerical Columne", "danger")
            return redirect(request.referrer or url_for("index"))

        # Collect updated data from the form submission
        updated_data = {
            "house number": request.form.get("house_number"),
            "monthly family income": family_income,
            "monthly family expenditure": family_expenditure,
            "average monthly electricity consumption": ceb,
            "ownership of the resident house": request.form.get("house_ownership"),
            "total paddy lands of house owner (in acre)": total_lands,
            "total vehicles of house owner": total_vehicles,
            "source of water": request.form.get("source_of_water"),
            "electricity": request.form.get("electricity"),
            "Total Machineries": request.form.get("machineries"),
            "toilet": request.form.get("toilet"),
            "type of house": request.form.get("house_type"),
            "house land size": request.form.get("land_size"),
            "family type": request.form.get("family_type"),  # Retrieve selected dropdown value
            "remark": request.form.get("remark"),
        }

        # Update the house document in the database
        mongo.db.houses.update_one({"_id": ObjectId(house_id)}, {"$set": updated_data})
        
        # Flash success message and redirect to the index page
        flash("The house was updated successfully!", "success")
        return redirect(url_for("view_house", house_id=house_id))

    # Render the edit house template, passing the house data and family type options
    return render_template(
        "edit_house.html",
        house=house,
        family_type_options=family_type_options,  # Pass the options for the dropdown
        house_type=house_type,
        land_size=land_size,
        water_source=water_source,
        electricity=electricity,
        toilet=toilet
    )


@app.route("/delete_house/<house_id>", methods=['GET', 'POST'])
def delete_house(house_id):
    # Deleting the house document and any related persons/kids
    mongo.db.houses.delete_one({"_id": ObjectId(house_id)})
    mongo.db.persons.delete_many({"house number": house_id})
    mongo.db.kids.delete_many({"house number": house_id})
    return redirect(url_for("index"))

if __name__ == "__main__":
    """ app.run(debug=True) """
    app.run(host='0.0.0.0', debug=True)
