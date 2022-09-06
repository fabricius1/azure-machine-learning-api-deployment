from django.core.management.utils import get_random_secret_key
import random
import sys
import os


# SETUP .env file
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

if len(sys.argv) == 1:
    azure_web_app_name = "".join([random.choice(chars) for x in range(15)])
elif len(sys.argv) == 2:
    azure_web_app_name = sys.argv[1]
else:
    raise TypeError('zero or one command line arguments were expected, '
                    f'got {len(sys.argv)}')

CONFIG_STRING = f"""
AZURE_WEB_APP_NAME=django-app-{azure_web_app_name}
DEBUG=False
SECRET_KEY={get_random_secret_key()}
ALLOWED_HOSTS=127.0.0.1, .localhost, 0.0.0.0, django-app-{azure_web_app_name}.azurewebsites.net
""".strip()

with open('.env', 'w') as file:
    file.write(CONFIG_STRING)


# SETUP main.tf file
main_tf_text ="""
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
  name                = var.django-app-name # "linear-regression-api"
  resource_group_name = azurerm_resource_group.rg_django_app.name
  location            = var.location
  service_plan_id     = azurerm_service_plan.django_app_service_plan.id

  site_config {
    application_stack {
      docker_image     = "" # insert docker image path between quotes here
      docker_image_tag = "latest"
    }
  }
}""" % ("django-app-" + azure_web_app_name)

with open('main.tf', 'w') as file:
    file.write(main_tf_text)
