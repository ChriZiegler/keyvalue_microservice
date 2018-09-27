from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database/keyvalue.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class KeyValue(db.Model):
    key = db.Column(db.String(),primary_key=True, unique=True, nullable=False)
    value = db.Column(db.String(), unique=False, nullable=False)
    def __repr__(self):
        return "Key: {}, Value: {}".format(self.key, self.value)


def handle_get(key):
    """ Look up the value of our key. If we don't have anything in
    our database with that key, return None

    :param str key: The key to look up in our database. The key cannot
                    be blank.
    :returns KeyValue or NoneType: The matching keyvalue or None
    """
    keyvalue = KeyValue.query.filter_by(key=key).first()
    return keyvalue


def handle_set(key, value):
    """ Add a new entry to our database, containing the key and value.

    :param str key: The key part of our key-value pair. All keys in our DB must
                    be unique. If a duplicate key is given, its value is
                    overwritten in the database with the new value.
    :param str value: The value of our key-value pair. Does not need to be unique.
    :returns KeyValue: The new keyvalue that was just created and added to the DB.
    """
    new_keyvalue = KeyValue(key=key, value=value)
    db.session.merge(new_keyvalue)
    db.session.commit()
    return new_keyvalue


@app.route("/", methods=['Get', 'Post'])
def index():
    if request.form:
        get_key_request = request.form.get('get_key')
        set_value_request = request.form.get('set_value')
        set_key_request = request.form.get('set_key')

        if get_key_request:
            return render_template("get.html",
                                   key_query=handle_get(get_key_request))
        elif set_key_request:
            return render_template("set.html",
                                   value_set=handle_set(set_key_request,
                                                        set_value_request))

    return render_template("index.html")


if __name__ == "__main__":
    db.create_all()
    app.run(port=8000, debug=True)
