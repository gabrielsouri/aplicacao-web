import os
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.abspath('templates'))

@app.route('/')
def home():
    return render_template("home.html",titulo='HOME')


@app.route('/config')
def config():
    menu_op = ["Usuarios","Veiculos","Patrimonio"]
    return render_template("config.html",menu=menu_op)

if __name__ == "__main__":
    app.run(debug=True)
