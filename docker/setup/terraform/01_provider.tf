# Configure Azure storage to manage Terraform State
# ref: https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage
terraform {
  backend "azurerm" {
    resource_group_name   = "tstate"
    storage_account_name  = "tstate31414"
    container_name        = "tstate"
    key                   = "terraform.tfstate"
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  version = "=2.23.0"

  features {}
}
