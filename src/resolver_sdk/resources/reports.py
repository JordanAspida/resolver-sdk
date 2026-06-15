class ReportsAPI:
    endpoint_get_reports = "/object/report"
    endpoint_get_report_components = "/object/report/{reportId}/reportComponents"
    endpoint_delete_report = "/object/report/{id}"

    # Initializes the ReportsAPI with a client reference
    def __init__(self, client):
        self.client = client

    # Retrieves all reports with optional caching and refresh capability
    def get_all_reports(self, refresh=False):
        if self.client.cache["all_reports"] is not None and not refresh:
            return self.client.cache["all_reports"]
        response = self.client.safe_get(self.endpoint_get_reports)
        self.client.cache["all_reports"] = response.get("data", [])
        return self.client.cache["all_reports"]

    # Deletes a specific report by its ID
    def delete_report(self, report_id):
        return self.client.safe_delete(self.endpoint_delete_report.format(id=report_id))

    # Retrieves all components of a specific report
    def get_report_components(self, report_id):
        return self.client.safe_get(self.endpoint_get_report_components.format(reportId=report_id)).get("data", [])
