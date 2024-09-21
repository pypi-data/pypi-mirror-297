from streamlit.web import cli
import os

project_path = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(project_path, 'app.py')


def run():
    cli.main_run([app_path])


if __name__ == "__main__":
    run()
