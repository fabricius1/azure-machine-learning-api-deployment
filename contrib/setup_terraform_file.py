from decouple import config


MAIN_TF_TEXT ="""
variable "django-app-name" {
    description = "Set name for azurerm_linux_web_app resource below"
    default = "%s"
}

variable "location" {
  description = "Amazon location where all resources should be created"
  default     = "eastus"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.21.1"
    }
  }
}

provider "azurerm" {
  features {}
}

# Provide the Resource Group
resource "azurerm_resource_group" "rg_django_app" {
  name     = "rg-django-app"
  location = var.location
  tags = {
    environment = "dev"
    source      = "Terraform"
  }
}


# Provide the App Service Plan 
# resource "azurerm_app_service_plan" "django_service_plan" {
resource "azurerm_service_plan" "django_app_service_plan" {
  name                = "app-service-plan-django-apps"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg_django_app.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "linear-model-api" {
  name                = var.django-app-name
  resource_group_name = azurerm_resource_group.rg_django_app.name
  location            = var.location
  service_plan_id     = azurerm_service_plan.django_app_service_plan.id

  site_config {
    application_stack {
      docker_image     = "" # insert docker image path between quotes here
      docker_image_tag = "latest"
    }
  }
}""" % config('AZURE_WEB_APP_NAME')

with open('main.tf', 'w') as file:
    file.write(MAIN_TF_TEXT)
