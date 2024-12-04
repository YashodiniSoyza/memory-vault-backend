import importlib
import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS

from constant import EnvKeys
from helper.logger import Logger
from model import EnvironmentProfile

load_dotenv()

PORT = os.getenv(EnvKeys.PORT.value, 5000)
PROFILE = os.getenv(EnvKeys.PROFILE.value, EnvironmentProfile.STAGING.value)
app = Flask(__name__)
CORS(app)
logger = Logger(__name__)


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app.json = CustomJSONProvider(app)


def register_blueprints(flask_app):
    base_dir = os.path.dirname(__file__)
    module_dir = os.path.join(base_dir, 'controller')

    for root, _, files in os.walk(module_dir):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                module_path = os.path.relpath(os.path.join(root, filename), base_dir)
                module_name = module_path.replace(os.sep, '.').replace('.py', '')

                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'mod') and isinstance(module.mod, Blueprint):
                        flask_app.register_blueprint(module.mod)
                    else:
                        logger.warning(f"No 'mod' blueprint in {module_name}")
                except (ImportError, AttributeError):
                    logger.exception(f"Failed to import {module_name}")


if __name__ == '__main__':
    logger.info(f"Starting Flask server on port {PORT} in {PROFILE} environment")

    register_blueprints(app)
    app.run(host="0.0.0.0", port=PORT, debug=(PROFILE == EnvironmentProfile.LOCAL.value))
