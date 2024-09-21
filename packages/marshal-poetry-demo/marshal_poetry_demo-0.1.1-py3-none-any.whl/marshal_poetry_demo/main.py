from streamlit.web import cli


def run():
    cli.main_run(["./poetry_demo/app.py"])


if __name__ == "__main__":
    run()
