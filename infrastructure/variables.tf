variable "project_id" {
  description = "The GC Project ID"
  type        = string
  default     = "dezc-housing"
}

variable "region" {
  description = "The region where the project resources will be created"
  type        = string
  default     = "EUROPE-WEST2" # London, this is a low CO2 region 
}
