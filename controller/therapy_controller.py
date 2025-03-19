from flask import Blueprint, jsonify
from pydantic import ValidationError
from model import HttpStatus
from constant import Blueprints, Endpoints, HttpMethod
from service import TherapyGenerationService, TherapyOutlineService

mod = Blueprint(Blueprints.THERAPY.value, __name__, url_prefix=Endpoints.THERAPY.value)


@mod.route(Endpoints.GENERATE_THERAPY.value, methods=[HttpMethod.POST.value])
def generate_therapy_outline(memory_id):
    try:
        TherapyGenerationService().generate_therapy(memory_id)
        return jsonify({"message": "Therapy generation started"}), HttpStatus.OK.value
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HttpStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_THERAPY_ID.value, methods=[HttpMethod.GET.value])
def get_therapy_outline(therapy_id):
    try:
        therapy_outline = TherapyOutlineService().get_therapy_outline_by_id(therapy_id)
        return jsonify(therapy_outline.model_dump()), HttpStatus.OK.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value
