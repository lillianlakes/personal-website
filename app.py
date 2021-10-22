from flask import Flask, render_template, request, flash
from flask_compress import Compress
from forms.forms import ContactForm
from flask_mail import Mail, Message
import os

app= Flask(__name__, template_folder='')

Compress(app)

app.secret_key = 'DONOTTELL'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = 'lillian.lakes@gmail.com'
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PW")

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def handle_contact_form():
    """Handle the contact form."""

    form = ContactForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            flash('Hmmm. Something isn\'t quite right with your submission.')
            return render_template('index.html', form=form)
        else:
            """Send Email."""
            msg = Message("Website Contact Form",
                       recipients=["lillian.lakes@gmail.com"],
                       sender=(form.name.data, form.email.data))
            msg.body = f"Name: {form.name.data} \n Email: {form.email.data} \n Message: {form.message.data}"
            mail.send(msg)

            """Reset form after sending email."""
            form.name.data = ""
            form.email.data = ""
            form.message.data = ""

            return render_template('index.html', form=form, success=True)

    elif request.method == 'GET':
        return render_template('index.html', form=form)