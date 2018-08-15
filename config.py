from run import app
app.secret_key = "jaffa"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://jaffa:jaffa@localhost/JaffaData'