# ------------------------------
# Virtual Machine Resource Group
# ------------------------------

# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "vm" {
  name     = var.vmName
  location = var.location

  tags = {}
}

# Create virtual network
resource "azurerm_virtual_network" "vm" {
  name                 = "vm-vnet"
  location             = azurerm_resource_group.vm.location
  resource_group_name  = azurerm_resource_group.vm.name
  address_space        = ["10.0.0.0/16"]

  tags = {}
}

# Create subnet
resource "azurerm_subnet" "vmsubnet" {
  name                 = "vmsubnet"
  resource_group_name  = azurerm_resource_group.vm.name
  virtual_network_name = azurerm_virtual_network.vm.name
  address_prefix       = "10.0.2.0/24"
}

# Create public IPs
resource "azurerm_public_ip" "vm" {
  name                         = "vm-ip"
  location                     = azurerm_resource_group.vm.location
  resource_group_name          = azurerm_resource_group.vm.name
  
  allocation_method            = "Dynamic"
  sku                          = "Basic"
  ip_version                   = "IPv4"
  domain_name_label            = "opwenvmtest"
  idle_timeout_in_minutes      = 4

  tags = {}
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "vm" {
  name                = "vm-nsg"
  location            = azurerm_resource_group.vm.location
  resource_group_name = azurerm_resource_group.vm.name

  security_rule {
    name                       = "SSH"
    priority                   = 300
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "HTTPS"
    priority                   = 320
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "HTTP"
    priority                   = 340
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {}
}

# Create network interface
resource "azurerm_network_interface" "vm" {
  name                      = "vm-nic"
  location                  = azurerm_resource_group.vm.location
  resource_group_name       = azurerm_resource_group.vm.name

  ip_configuration {
    name                          = "vm-nicConfiguration"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.vm.id
    subnet_id                     = azurerm_subnet.vmsubnet.id
    primary                       = true
  }

  tags = {}
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "vm" {
  network_interface_id      = azurerm_network_interface.vm.id
  network_security_group_id = azurerm_network_security_group.vm.id
}

# Generate random text for a unique storage account name
resource "random_id" "randomVmId" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.vm.name
  }

  byte_length = 8
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "vm" {
  name                        = "diag${random_id.randomVmId.hex}"
  location                    = azurerm_resource_group.vm.location
  resource_group_name         = azurerm_resource_group.vm.name
  account_tier                = "Standard"
  account_replication_type    = "LRS"

  tags = {}
}

# Create (and display) an SSH key
resource "tls_private_key" "vm" {
  algorithm = "RSA"
  rsa_bits = 4096
}
output "tls_private_key" { value = tls_private_key.vm.private_key_pem }

# Create virtual machine
resource "azurerm_linux_virtual_machine" "vm" {
  name                  = "vm"
  location              = azurerm_resource_group.vm.location
  resource_group_name   = azurerm_resource_group.vm.name
  network_interface_ids = [azurerm_network_interface.vm.id]
  size                  = "Standard_D4s_v3"
  provision_vm_agent    = true

  os_disk {
    name                 = "vm-disk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  admin_username                  = var.RESOURCE_GROUP_NAME
  disable_password_authentication = true
  allow_extension_operations      = true

  admin_ssh_key {
    username       = var.RESOURCE_GROUP_NAME
    public_key     = tls_private_key.vm.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.vm.primary_blob_endpoint
  }

  tags = {}
}
