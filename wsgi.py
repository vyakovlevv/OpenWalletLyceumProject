from main import *

if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 8080), host='0.0.0.0')
