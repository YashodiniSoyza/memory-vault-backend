from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from model import Memory, HttpStatus
from service import MemoryService
from constant import Blueprints, Endpoints, Fields, HttpMethod


mod = Blueprint(Blueprints.MEMORY.value, __name__, url_prefix=Endpoints.MEMORY.value)


@mod.route(Endpoints.ROOT.value, methods=[HttpMethod.POST.value])
def save_memory():
    try:
        memory_id = MemoryService().save_memory(Memory(**request.json))
        return jsonify({"id": memory_id}), HttpStatus.CREATED.value
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HttpStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.ROOT.value, methods=[HttpMethod.GET.value])
def get_all_memories():
    try:
        memories = MemoryService().get_all_memories()
        return jsonify([memory.model_dump(by_alias=True) for memory in memories]), HttpStatus.OK.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_MEMORY_ID.value, methods=[HttpMethod.GET.value])
def get_memory_by_id(memory_id):
    try:
        memory = MemoryService().get_memory_by_id(memory_id)
        return jsonify(memory.model_dump(by_alias=True)), HttpStatus.OK.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_MEMORY_ID.value, methods=[HttpMethod.PUT.value])
def update_memory_by_id(memory_id):
    try:
        memory = MemoryService().update_memory_by_id(memory_id, Memory(**request.json))
        return jsonify({"updated": memory}), HttpStatus.OK.value
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HttpStatus.BAD_REQUEST.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_MEMORY_ID.value, methods=[HttpMethod.DELETE.value])
def delete_memory_by_id(memory_id):
    try:
        memory = MemoryService().delete_memory_by_id(memory_id)
        return jsonify({"deleted": memory}), HttpStatus.OK.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_PATIENT_ID.value, methods=[HttpMethod.GET.value])
def get_memories_by_patient_id(patient_id):
    try:
        memories = MemoryService().get_memories_by_patient_id(patient_id)
        return jsonify([memory.model_dump(by_alias=True) for memory in memories]), HttpStatus.OK.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value
