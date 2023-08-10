import os
from app import create_app

config_module = os.environ.get('config_module', 'config')

app = create_app(config_module)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'


@app.route("/")
def app_status():
    return "Blog Service is running", 200


if __name__ == "__main__":
    app.run()
