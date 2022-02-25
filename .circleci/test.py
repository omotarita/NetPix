from dash.testing.application_runners import import_app

def test(dash_duo):

    app = import_app(".circleci.app")

    timeout = 30

    return None
