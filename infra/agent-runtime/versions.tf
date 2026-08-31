terraform {
  required_version = ">= 1.7.0, < 1.10.0"

  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 7.28.0, < 7.29.0"
    }
  }
}
