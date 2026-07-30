from ..schemas.formulas import *

class FormulasAPI:
    endpoint_bulk_recalc_formula = "/data/object/bulkFormulaCalculation/recalculate/formula/{formulaId}" # Re-calculates a formula for ALL objects
    endpoint_delete_formula = "/object/objectType/{objectTypeId}/formulas/{id}" # Deletes a formula for a specific object type

    # Initialises the FormulasAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Endpoint to recalculate a specific formula for all objects
    def recalculate_for_all_objs(self, formula_id, check_previous=True) -> str:
        params = {
            "checkPrevious": str(check_previous).lower()
        }

        job_id = self.client.safe_post(self.endpoint_bulk_recalc_formula.format(formulaId=formula_id), params=params).get("jobId")

        return self.client.utility.wait_for_job(job_id=job_id).payload

    # Endpoint to delete a specific formula for a specific object type
    def delete_formula(self, formula_id, object_type_id) -> str:

        response = self.client.safe_delete(self.endpoint_delete_formula.format(objectTypeId=object_type_id, id=formula_id))
        return response