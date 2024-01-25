from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

data = []

def veriAl():
    global data
    with sqlite3.connect('telephone.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tblTelephone")  
        data = cur.fetchall()
        for i in data:
            print(i)

def veriEkle(title, brand, year):
    with sqlite3.connect('telephone.db') as con:
        cur = con.cursor()
        cur.execute("insert into tblTelephone (telephonetitle, telephonebrand, telephoneyear) values (?,?,?)", (title, brand, year))
        con.commit()
        print("Veriler eklendi")

def veriSil(id):
    with sqlite3.connect('telephone.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblTelephone where id=?", [id])
        print("Veriler silindi")
        

def veriGuncelle(id, title, brand, year):
    with sqlite3.connect('telephone.db') as con:
        cur = con.cursor()
        cur.execute("update tblTelephone set telephonetitle=?, telephonebrand=?, telephoneyear=? where id=?", (title, brand, year, id))
        con.commit()
        print("Veriler güncellendi")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/telephones")
def telephones():
    veriAl()
    return render_template("telephones.html", veri=data)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/telephoneekle", methods=['GET', 'POST'])
def telephoneekle():
    print("telephoneekle")
    if request.method == "POST":
        telephonetitle = request.form['telephonetitle']
        telephonebrand = request.form['telephonebrand']
        telephoneyear = request.form['telephoneyear']
        veriEkle(telephonetitle, telephonebrand, telephoneyear)
    return render_template("telephoneekle.html")

@app.route("/telephonesil/<string:id>")
def telephonesil(id):
    print("telephone silinecek id", id)
    veriSil(id)
    return redirect(url_for("telephones"))

@app.route("/telephoneguncelle/<string:id>", methods=['GET', 'POST'])
def telephoneguncelle(id):
    if request.method == 'GET':
        print("Güncellenecek id", id)

        guncellenecekVeri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekVeri = list(d)
        return render_template("telephoneguncelle.html", veri=guncellenecekVeri)
    else:
        telephoneID = request.form['telephoneID']
        telephonetitle = request.form['telephonetitle']
        telephonebrand = request.form['telephonebrand']
        telephoneyear = request.form['telephoneyear']
        veriGuncelle(telephoneID, telephonetitle, telephonebrand, telephoneyear)
        return redirect(url_for("telephones"))

@app.route("/telephonedetay/<string:id>")
def telephonedetay(id):
    detayVeri = []
    for d in data:
        if str(d[0]) == id:
            detayVeri = list(d)
    return render_template("telephonedetay.html", veri=detayVeri)

if __name__ == "__main__":
    app.run(debug=True)

