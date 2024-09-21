from pydantic import BaseModel, Field
from herre import Herre
from fakts import Fakts
from .model import Manifest, Requirement
from typing import Callable, Dict
import importlib
import sys
import os
import traceback
import logging
import pkgutil

Params = Dict[str, str]


class Registration(BaseModel):
    name: str
    requirement: Requirement
    builder: Callable[[Herre, Fakts, Params], object]


basic_requirements = {
    "lok": Requirement(
        service="live.arkitekt.lok",
        description="An instance of ArkitektNext Lok to authenticate the user",
    ),
}


class ServiceBuilderRegistry:
    def __init__(self):
        self.service_builders = {}
        self.requirements = basic_requirements

    def register(
        self,
        name: str,
        service_builder: Callable[[Herre, Fakts], object],
        requirement: Requirement,
    ):
        self.service_builders[name] = service_builder
        self.requirements[name] = requirement

    def get(self, name):
        return self.services.get(name)

    def build_service_map(
        self, fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        return {
            name: builder(fakts, herre, params, manifest)
            for name, builder in self.service_builders.items()
        }

    def get_requirements(self):
        return self.requirements


class SetupInfo:
    services: Dict[str, object]


def check_and_import_services() -> ServiceBuilderRegistry:

    service_builder_registry = ServiceBuilderRegistry()

    # Function to load and call init_extensions from __rekuest__.py
    def load_and_call_init_extensions(module_name, rekuest_path):
        try:
            spec = importlib.util.spec_from_file_location(
                f"{module_name}.__arkitekt__", rekuest_path
            )
            rekuest_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(rekuest_module)
            if hasattr(rekuest_module, "init_services"):
                rekuest_module.init_services(service_builder_registry)
                logging.info(f"Called init_service function from {module_name}")
            else:
                logging.debug(f"No init_services function in {module_name}.__arkitekt__. Skipping.")
        except Exception as e:
            logging.critical(f"Failed to call init_services for {module_name}: {e}")
            traceback.print_exc()

    # Check local modules in the current working directory
    current_directory = os.getcwd()
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path) and os.path.isfile(
            os.path.join(item_path, "__init__.py")
        ):
            rekuest_path = os.path.join(item_path, "__arkitekt__.py")
            if os.path.isfile(rekuest_path):
                load_and_call_init_extensions(item, rekuest_path)

    # Check installed packages
    for _, module_name, _ in pkgutil.iter_modules():
        try:
            module_spec = importlib.util.find_spec(module_name)
            if module_spec and module_spec.origin:
                rekuest_path = os.path.join(
                    os.path.dirname(module_spec.origin), "__arkitekt__.py"
                )
                if os.path.isfile(rekuest_path):
                    load_and_call_init_extensions(module_name, rekuest_path)
        except Exception as e:
            print(
                f"Failed to call init_extensions for installed package {module_name}: {e}"
            )
            traceback.print_exc()

    return service_builder_registry


def check_and_return_already_imported_services() -> ServiceBuilderRegistry:
    service_builder_registry = ServiceBuilderRegistry()

    # Function to load and call init_services from __arkitekt__.py
    def load_and_call_init_services(module_name, arkitekt_path):
        try:
            # Compute the full module name of the __arkitekt__ module
            arkitekt_module_name = f"{module_name}.__arkitekt__"
    

            # Create a module spec
            spec = importlib.util.spec_from_file_location(
                arkitekt_module_name, arkitekt_path
            )
            arkitekt_module = importlib.util.module_from_spec(spec)

            # Execute the module
            spec.loader.exec_module(arkitekt_module)

            # Now call init_services
            if hasattr(arkitekt_module, "init_services"):
                arkitekt_module.init_services(service_builder_registry)
                logging.info(f"Called init_services function from {arkitekt_module_name}")
            else:
                logging.debug(f"No init_services function in {arkitekt_module_name}. Skipping.")
        except Exception as e:
            logging.critical(f"Failed to call init_services for {module_name}: {e}")
            traceback.print_exc()

    # Create a static list of sys.modules items to avoid RuntimeError
    imported_modules = list(sys.modules.items())

    # Keep track of processed top-level modules to avoid duplicates
    processed_modules = set()

    # Iterate over currently imported modules
    for module_name, module in imported_modules:
        if module is None:
            continue

        # Get the top-level parent module name
        top_level_module_name = module_name.split('.')[0]

        # Avoid processing the same top-level module multiple times
        if top_level_module_name in processed_modules:
            continue  # Already processed

        # Get the module from sys.modules
        top_level_module = sys.modules.get(top_level_module_name)
        if top_level_module is None:
            continue

        # Get the module's file location
        module_file = getattr(top_level_module, '__file__', None)
        if not module_file:
            continue  # Skip modules without a file attribute

        # Get the module's directory
        module_dir = os.path.dirname(module_file)
        arkitekt_path = os.path.join(module_dir, '__arkitekt__.py')

        # Check if __arkitekt__.py exists in the top-level module directory
        if os.path.isfile(arkitekt_path):
            load_and_call_init_services(top_level_module_name, arkitekt_path)
            processed_modules.add(top_level_module_name)

    return service_builder_registry
