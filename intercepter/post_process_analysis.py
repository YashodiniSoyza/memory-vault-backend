import threading
from functools import wraps


def post_process_analysis():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            memory = kwargs.get("memory") or (args[1] if len(args) > 1 else None)

            patient_id = getattr(memory, "patientId", None) if memory else None

            if patient_id:
                thread = threading.Thread(
                    target=_analyze_memories, args=(patient_id,), name=f"AnalysisThread-{patient_id}"
                )
                thread.start()

            return result
        return wrapper

    def _analyze_memories(patient_id):
        try:
            from service.media_description_analysis_service import MediaDescriptionAnalysisService
            analysis_service = MediaDescriptionAnalysisService()
            analysis_service.analyze_memories_by_patient_id(patient_id=patient_id)
        except Exception as e:
            print(f"Error during analysis for patient_id {patient_id}: {e}")

    return decorator
