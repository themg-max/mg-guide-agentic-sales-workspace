variable "project_id" {
  description = "Google Cloud project that hosts the MG Guide Agent Runtime."
  type        = string

  validation {
    condition     = var.project_id == "ai-rolodex-to-crm"
    error_message = "The authoritative development binding targets ai-rolodex-to-crm."
  }
}

variable "region" {
  description = "Google Cloud region for the Agent Runtime resource."
  type        = string
  default     = "us-east1"

  validation {
    condition     = var.region == "us-east1"
    error_message = "The MG Guide Agent Runtime region is us-east1."
  }
}

variable "runtime_display_name" {
  description = "Display name for the single MG Guide Agent Runtime resource."
  type        = string
  default     = "mg-guide-orchestrator"
}

variable "runtime_service_account_email" {
  description = "Existing approved service account used by the Agent Runtime."
  type        = string

  validation {
    condition = var.runtime_service_account_email == (
      "mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )
    error_message = "Use the approved existing MG Guide Agent Runtime service account."
  }
}

variable "agent_source_archive_b64" {
  description = "Base64 ZIP source archive for the Agent Runtime source-code spec."
  type        = string
  sensitive   = true

  validation {
    condition     = length(trimspace(var.agent_source_archive_b64)) > 0
    error_message = "Provide a non-empty base64 source archive."
  }
}
