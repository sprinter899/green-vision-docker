import os
from flask import Flask, flash, request, redirect, render_template
import core

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "secret key"



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('main_page.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(file.filename)

            nuc = core.Core(file.filename)

            flash("mass = ", nuc.mass, "gr")
            flash("day = ", nuc.day)


            os.remove(file.filename)
            return redirect('/')

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
    #app.run()
