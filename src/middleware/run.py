from api import app
from parse import j2m

if __name__ == '__main__':
    j2m.sample_to_database()
    app.run(host="0.0.0.0", port =5000, debug=False)