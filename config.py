from apispec import APISpec

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

class Config:
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TASKS_PER_PAGE = 3
    JWT_SECRET_KEY = 'bdd278a162c44c32a6a8f977602af1de'
    APISPEC_SPEC = APISpec(
        title="TODO APP",
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    )
    APISPEC_SWAGGER_URL = '/swagger/'
