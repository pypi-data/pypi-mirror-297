import typing as t
from functools import wraps

from flask import session

from ._private_funcs import _check_against_values_allowed


def api_login_check(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
) -> t.Callable[..., t.Any]:
    """
    A decorator that is used to secure API routes that return JSON responses.

    :raw-html:`<br />`

    **Example of a route that requires a user to be logged in:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True)
        def api_page():
            ...

    :raw-html:`<br />`

    **You can also supply your own failed return JSON:**

    :raw-html:`<br />`

    .. code-block::

        @bp.route("/api/resource", methods=["GET"])
        @api_login_check('logged_in', True, fail_json={"error": "You are not logged in."})
        def api_page():
            ...

    :raw-html:`<br />`

    -----

    :param session_key: The session key to check for.
    :param values_allowed: A list of or singular value(s) that the session key must contain.
    :param fail_json: JSON that is returned on failure. {"error": "You are not logged in."} by default.
    :return: The decorated function, or a JSON response.
    """

    def api_login_check_wrapper(func: t.Any) -> t.Callable[..., t.Any]:
        @wraps(func)
        def inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            skey = session.get(session_key)
            if skey is not None:
                if _check_against_values_allowed(skey, values_allowed):
                    return func(*args, **kwargs)

            return fail_json

        return inner

    return api_login_check_wrapper
