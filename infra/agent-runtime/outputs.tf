output "agent_runtime_resource_name" {
  description = "Fully qualified name of the MG Guide Agent Runtime resource."
  value       = google_vertex_ai_reasoning_engine.mg_guide.name
}

output "runtime_service_account_email" {
  description = "Existing service account bound to the Agent Runtime."
  value       = var.runtime_service_account_email
}
