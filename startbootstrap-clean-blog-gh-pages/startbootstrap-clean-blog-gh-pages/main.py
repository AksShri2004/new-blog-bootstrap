from flask import Flask, render_template, request
import requests

data  =requests.get("https://api.npoint.io/674f5423f73deab1e9a7").json()



app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", data= data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/submitted", methods = ["POST"])
def handle_data():
    req = request.form
    name = req["name"]
    email = req["email"]
    phone = req["phone"]
    message = req["message"]

    import smtplib
    import os

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=os.getenv("email"), password=os.getenv("pass"))
        connection.sendmail(
            from_addr=os.getenv("email"),
            to_addrs= os.getenv("rec"),
            msg=f"Received a query from {name}.\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )

    return "<h1> MESSAGE SENT SUCCESSFULLY.</H1>"


@app.route("/post/<id>")
def post(id):
    id = int(id) - 1
    return render_template("post.html", id = id, data = data)


if __name__ == "__main__":
    app.run(debug=True)
