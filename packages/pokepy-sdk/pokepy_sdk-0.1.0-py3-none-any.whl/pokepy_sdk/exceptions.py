class APIError(Exception):
    pass


class BadRequest(APIError):
    pass


class Unauthorized(APIError):
    pass


class NotFound(APIError):
    pass


class UnprocessibleEntity(APIError):
    pass
