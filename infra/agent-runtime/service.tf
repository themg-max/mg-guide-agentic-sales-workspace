resource "google_vertex_ai_reasoning_engine" "mg_guide" {
  provider     = google-beta
  display_name = var.runtime_display_name
  description  = "MG Guide Agent Runtime"
  project      = var.project_id
  region       = var.region

  spec {
    agent_framework = "google-adk"
    service_account = var.runtime_service_account_email

    source_code_spec {
      inline_source {
        source_archive = var.agent_source_archive_b64
      }
      python_spec {
        entrypoint_module = "app.agent"
        entrypoint_object = "agent_runtime_app"
        requirements_file = "requirements.txt"
        version           = "3.12"
      }
    }
  }
}
