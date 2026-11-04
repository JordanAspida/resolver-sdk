from ..schemas.formulas import FormulaDetails, FormulaVariable

class FormulasAPI:
    endpoint_bulk_recalc_formula = "/data/object/bulkFormulaCalculation/recalculate/formula/{formulaId}" # Re-calculates a formula for ALL objects
    endpoint_delete_formula = "/object/objectType/{objectTypeId}/formulas/{id}" # Deletes a formula for a specific object type
    endpoint_get_formlae_for_obj_type = "/object/objectType/{objectTypeId}/formulas" # Retrieve all formula for an object type
    endpoint_get_formula_variables = "/object/objectType/{objectTypeId}/formulas/{formulaId}/variables"

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

    # Retrieve all formulas for an object type
    def get_formulae_for_obj_type(self, obj_type_id) -> list[FormulaDetails]:
        response = self.client.safe_get(self.endpoint_get_formlae_for_obj_type.format(objectTypeId=obj_type_id)).get("data", [])

        return [FormulaDetails(**formula) for formula in response]

    # Retrieve all variables in a formula
    def get_formula_variables(self, obj_type_id, formula_id) -> list[FormulaVariable]:
        response = self.client.safe_get(self.endpoint_get_formula_variables.format(objectTypeId=obj_type_id, formulaId=formula_id)).get("data", [])

        return [FormulaVariable(**var) for var in response]

