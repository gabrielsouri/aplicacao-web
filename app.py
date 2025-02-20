from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",titulo='HOME')


@app.route('/config')
def config():
    menu_op = ["Usuarios","Veiculos","Patrimonio"]
    return render_template("config.html",menu=menu_op)


#app.run(debug=True)
