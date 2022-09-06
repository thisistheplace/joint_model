from dash import html
from requests import Response

from ...constants import RESTAPI_URL


class MeshApiHttpError(Exception):
    def __init__(self, response: Response):
        # Catch response for "Unprocecessable entity"
        if response.status_code == 422:
            # Generate helpful message together
            header = f"{response.status_code} Error: {response.reason}"
            msg = html.Div(
                [
                    html.H6(header),
                    html.P(response.text),
                    html.Br(),
                    html.A(
                        "Click here to review the required input format.",
                        href=f"{RESTAPI_URL}/docs",
                        target="_blank",
                    ),
                ]
            )
            self.toast_message = msg
            super().__init__(header)
        else:
            response.raise_for_status()
