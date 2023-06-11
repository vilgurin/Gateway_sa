from fastapi import FastAPI

import requests
import json

from fastapi.responses import JSONResponse
from datetime import date

app = FastAPI()


from datetime import datetime, timedelta

@app.post("/membership/add_new/{name}/{description}/{price}")
def create_new_membership(name, description, price):
    template_membership = {
        "name" : name,
        "description" : description,
        "price" : price
    }

    requests.post("http://localhost:5005/api/membershiptypes/", json = template_membership)
    return

@app.post("/api/registration/{name}/{password}/{email}")
def send_info_to_db(name, password, email):

    template = {
                "Username": name,
                "Password": password,
                "email": email
                } 
    requests.post("http://localhost:5005/api/registration/", json = template)
    return 


@app.post("/membership/register_person/{email}/{membership_type}")
def register_person(email, membership_type):
    
    current_date = date.today()
    #formatted_date = current_date.strftime("%Y-%m-%d")


    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    future_date = current_date + timedelta(days=5*30)

    formatted_future_date = future_date.strftime("%Y-%m-%d")
    #print(formatted_future_date)

    response = get_user_id_from_email(email)
    print(response)

    if type(response) == str:
        print("No Such User in DataBase")
    elif type(response) == dict:
        user_id = response["Id"]

    url_membership_id = f"http://localhost:5005/api/membershiptypes/name/{membership_type}"
    resp = requests.get(url_membership_id)
    membership_id = resp.json()["Id"]
    print(membership_id)
    membership_template = {
                    "UserId":user_id,
                    "MembershipTypeId": membership_id,
                    "StartDate":formatted_date,
                    "EndDate":formatted_future_date,
                    "IsActive":True
                    }


    requests.post("http://localhost:5005/api/membership/", json = membership_template)
    return



@app.get("/get_id/{user_email}")
def get_user_id_from_email(user_email):

    "http://localhost:5005/api/registration/email/zhurba@example.com"
    url = f"http://localhost:5005/api/registration/email/{user_email}"
    resp = requests.get(url)
    resp_dict = resp.json()
    print(type(resp_dict))
    return resp_dict


@app.post("/start_training/{email}")
def start_training(email):
    
    response = get_user_id_from_email(email)

    if type(response) == str:
        print("No Such User in DataBase")
    elif type(response) == dict:
        user_id = response["Id"]
        t = {"usr_id": user_id}
        return_from_post = requests.post("http://127.0.0.1:8001/start", json = t)
        print(return_from_post)
        return return_from_post.json()
    
@app.post("/end_training/{email}")
def end_training(email):
    
    response = get_user_id_from_email(email)

    if type(response) == str:
        print("No Such User in DataBase")
    elif type(response) == dict:
        user_id = response["Id"]
        t = {"usr_id": user_id}
        return_from_post = requests.post("http://127.0.0.1:8001/end", json = t)
        print(return_from_post)
        return return_from_post
    


@app.post("/discount")
def discount():
    return_from_post = requests.post("http://127.0.0.1:8001/")

    return


# HERE Mongodb part


@app.get("/get_catalog")
def get_catalog():
    url = f"http://localhost:8002/catalogue"
    resp = requests.get(url)
    resp_dict = resp.json()
    print(resp_dict)
    return resp_dict


@app.post("/add_new_provider/{name}/{email}/{provider_descr}")
def add_new_provider(name, email, provider_descr):
    template = {
        "provider_name": name,
        "email": email,
        "provider_descr": provider_descr,
        "types": [
            {
            "type_name": "Dancing",
                "type_descr": "Dancing description!"
            },
            {
            "type_name": "Boxing",
                "type_descr": "Boxing description!"
            }
        ]
    }
    return_from_post = requests.post(f"http://localhost:8002/providers", json=template)
    return

@app.get("/get_provider/{provider_id}")
def get_provider(provider_id):
    url = f"http://localhost:8002/providers/{provider_id}"
    resp = requests.get(url)
    resp_dict = resp.json()
    print(resp_dict)
    return resp_dict
