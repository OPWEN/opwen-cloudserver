# ------------------------------
# Test Resource Group
# ------------------------------

# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "test" {
    name     = "${var.RESOURCE_GROUP_NAME}test"
    location = var.location

    tags = {}
}
