from api import app
from parse import j2m

if __name__ == '__main__':
    j2m.sample_to_database()
    app.run(debug=False)