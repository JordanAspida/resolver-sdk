from ..schemas.forms import FormDetails, FormStructure, ReportDetails, FormulaDetails, RoleDetails, FormComponent, NavFormNode
from typing import Union

class FormsAPI:
    endpoint_get_forms = "/object/form"
    endpoint_get_form_struct = "/object/form/{id}/structure"
    endpoint_delete_form = "/object/form/{id}"
    endpoint_get_forms_in_nav_form = "/object/form/{formId}/load"

    # Initializes the FormsAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all forms with optional caching and refresh capability
    def get_all_forms(self, refresh=False) -> list[FormDetails]:
        # Checks if already cached
        if self.client.cache["all_forms"] is not None and not refresh:
            return self.client.cache["all_forms"]
        
        response = self.client.safe_get(self.endpoint_get_forms)
        self.client.cache["all_forms"] = [FormDetails(**form_data) for form_data in response.get("data", [])]

        return self.client.cache["all_forms"]

    # Deletes a specific form by its ID
    def delete_form(self, form_id):
        return self.client.safe_delete(self.endpoint_delete_form.format(id=form_id))


    # Get full form structure
    def get_form_full_structure(self, form_id) -> FormStructure:
        if form_id in self.client.cache["form_structures"]:
            return self.client.cache["form_structures"].get(form_id)
        
        self.client.cache["form_structures"][form_id] = FormStructure(**self.client.safe_get(self.endpoint_get_form_struct.format(id=form_id)))
        return self.client.cache["form_structures"][form_id]

    # Retrieves linked forms and optionally their components for a specific form
    def get_linked_forms(self, form_id, comps=False) -> Union[list[FormDetails], tuple[list[FormDetails], list[FormComponent]]]:
        form_struct = self.get_form_full_structure(form_id=form_id)
        if comps:
            return form_struct.forms, form_struct.components
        return form_struct.forms

    # Retrieves all reports associated with a specific form
    def get_form_reports(self, form_id) -> list[ReportDetails]: 
        form_struct = self.get_form_full_structure(form_id=form_id)
        return form_struct.reports

    # Retrieves all formulas associated with a specific form
    def get_form_formula(self, form_id) -> Union[dict[int, FormulaDetails], list]:
        form_struct = self.get_form_full_structure(form_id=form_id)
        return form_struct.formulas

    # Retrieves all roles associated with a specific form
    def get_form_roles(self, form_id) -> list[RoleDetails]:
        form_struct = self.get_form_full_structure(form_id=form_id)
        return form_struct.roles
        

    # Retrieves all forms loaded within a navigation form
    def get_all_forms_in_nav_form(self, nav_form_id) -> list[NavFormNode]: 
        return [NavFormNode(**form_data) for form_data in self.client.safe_get(self.endpoint_get_forms_in_nav_form.format(formId=nav_form_id))]
