class FormsAPI:
    endpoint_get_forms = "/object/form"
    endpoint_get_form_struct = "/object/form/{id}/structure"
    endpoint_delete_form = "/object/form/{id}"
    endpoint_get_forms_in_nav_form = "/object/form/{formId}/load"

    # Initializes the FormsAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all forms with optional caching and refresh capability
    def get_all_forms(self, refresh=False):
        if self.client.cache["all_forms"] is not None and not refresh:
            return self.client.cache["all_forms"]
        response = self.client.safe_get(self.endpoint_get_forms)
        self.client.cache["all_forms"] = response.get("data", [])
        return self.client.cache["all_forms"]

    # Deletes a specific form by its ID
    def delete_form(self, form_id):
        return self.client.safe_delete(self.endpoint_delete_form.format(id=form_id))

    # Retrieves linked forms and optionally their components for a specific form
    def get_linked_forms(self, form_id, comps=False):
        resp = self.client.safe_get(self.endpoint_get_form_struct.format(id=form_id))
        if comps:
            return resp.get("forms", []), resp.get("components", [])
        return resp.get("forms", [])

    # Retrieves all reports associated with a specific form
    def get_form_reports(self, form_id):
        return self.client.safe_get(self.endpoint_get_form_struct.format(id=form_id)).get("reports", [])

    # Retrieves all formulas associated with a specific form
    def get_form_formula(self, form_id):
        return self.client.safe_get(self.endpoint_get_form_struct.format(id=form_id)).get("formulas", [])

    # Retrieves all roles associated with a specific form
    def get_form_roles(self, form_id):
        return self.client.safe_get(self.endpoint_get_form_struct.format(id=form_id)).get("roles", [])

    # Retrieves all forms loaded within a navigation form
    def get_all_forms_in_nav_form(self, nav_form_id):
        return self.client.safe_get(self.endpoint_get_forms_in_nav_form.format(formId=nav_form_id))
