from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from model import Patient, HttpStatus
from service import PatientService
from constant import Blueprints, Endpoints, Fields, HttpMethod


mod = Blueprint(Blueprints.PATIENT.value, __name__,
                url_prefix=Endpoints.PATIENT.value)


@mod.route(Endpoints.ROOT.value, methods=[HttpMethod.POST.value])
def save_patient():
    try:
        patient_id = PatientService().save_patient(Patient(**request.json))
        return jsonify("id", patient_id), HttpStatus.CREATED.value
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HttpStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.ROOT.value, methods=[HttpMethod.GET.value])
def get_all_patients():
    try:
        patients = PatientService().get_all_patients()
        return jsonify([patient.model_dump(by_alias=True) for patient in patients]), HttpStatus.OK.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_PATIENT_ID.value, methods=[HttpMethod.GET.value])
def get_patient_by_id(patient_id):
    try:
        patient = PatientService().get_patient_by_id(patient_id)
        return jsonify(patient.model_dump(by_alias=True)), HttpStatus.OK.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_PATIENT_ID.value, methods=[HttpMethod.PUT.value])
def update_patient_by_id(patient_id):
    try:
        patient = PatientService().update_patient_by_id(patient_id, Patient(**request.json))
        return jsonify({"updated": patient}), HttpStatus.OK.value
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HttpStatus.BAD_REQUEST.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@mod.route(Endpoints.BY_PATIENT_ID.value, methods=[HttpMethod.DELETE.value])
def delete_patient_by_id(patient_id):
    try:
        patient = PatientService().delete_patient_by_id(patient_id)
        return jsonify({"deleted": patient}), HttpStatus.OK.value
    except ValueError as ve:
        return jsonify({"errors": str(ve)}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        return jsonify({"errors": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value
