import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import tomli
import yaml

from . import mock_dag
from .hypernode import HyperNode
from .node_handler import NodeHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NodeRegistry:
    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = Path(registry_path or self._get_default_registry_path())
        self.nodes: Dict[str, Dict[str, Any]] = self._load_registry()
        self.node_folder_template = self._get_node_folder_template()

    def _get_node_folder_template(self) -> str:
        try:
            with open(self.registry_path, "r") as f:
                registry = yaml.safe_load(f)
            return registry.get("node_folder_template", "tests/nodes/{node_name}/artifacts")
        except Exception as e:
            print(f"Error reading registry: {e}. Using default template.")
            return "tests/nodes/{node_name}/artifacts"

    def _load_registry(self) -> Dict[str, Dict[str, Any]]:
        if self.registry_path.exists():
            with open(self.registry_path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    def list_nodes(self) -> List[str]:
        final_nodes = []
        for name, node in self.nodes.items():
            if "hypster_config" in node and "hamilton_dags" in node:
                final_nodes.append(name)
        return final_nodes

    def create_or_get(
        self,
        node_name: str,
        folder: Optional[str] = None,
        overwrite: bool = False,
    ) -> "NodeHandler":
        if folder is None:
            folder = self.node_folder_template.format(node_name=node_name)
        if node_name in self.nodes:
            existing_folder = self.nodes[node_name]["folder"]
            if existing_folder != folder:
                if not overwrite:
                    raise ValueError(
                        f"Node '{node_name}' already exists with a different \
                            folder. "
                        f"Existing: {existing_folder}, Requested: {folder}. "
                        f"Use overwrite=True to create a new node."
                    )
                else:
                    print(
                        f"Overwriting existing node '{node_name}' with \
                            new folder: {folder}"
                    )
                    self.nodes[node_name] = {"folder": folder}
                    self._save_registry()
            else:
                print(f'Loaded existing node "{node_name}" from {existing_folder}')
        else:
            os.makedirs(folder, exist_ok=True)
            self.nodes[node_name] = {"folder": folder}
            self._save_registry()
            print(f'Created new node "{node_name}" in {folder}')

        return NodeHandler(node_name, folder, self)

    def set_hypster_config_for_node(
        self, node_name: str, config_path: str, builder_param_name: str
    ):
        # TODO: add builder param name to registry
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in registry")

        self.nodes[node_name]["hypster_config"] = config_path
        self._save_registry()

    def add_dag_to_node(self, node_name: str, dag_path: str):
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in registry")

        if "hamilton_dags" not in self.nodes[node_name]:
            self.nodes[node_name]["hamilton_dags"] = []

        if dag_path not in self.nodes[node_name]["hamilton_dags"]:
            self.nodes[node_name]["hamilton_dags"].append(dag_path)
        self._save_registry()

    def update_node(self, node_name: str, handler: "NodeHandler"):
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in registry")

        self.nodes[node_name] = {
            "folder": str(handler.folder),
            "hamilton_dags": [
                str(handler.folder / f"{node_name}_{module.__name__}.py")
                for module in handler.hamilton_dags
            ],
            "hypster_config": str(handler.folder / f"{node_name}_hypster_config.py")
            if handler.hypster_config
            else None,
        }
        self._save_registry()

    def mock(self, node_name: str) -> HyperNode:
        from hypster import HP, config

        @config
        def mock_config(hp: HP):
            mock_param = hp.select([1, 2], default=1)

        return HyperNode(node_name, [mock_dag], mock_config)

    def load(self, node_name: str) -> HyperNode:
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in registry")

        node_info = self.nodes[node_name]
        node_handler = NodeHandler(node_name, node_info["folder"], self)
        return node_handler.to_hypernode()

    def _save_registry(self):
        with open(self.registry_path, "w") as f:
            yaml.dump(self.nodes, f, default_flow_style=False, sort_keys=False)

    def delete(self, node_name: str):
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in registry")

        del self.nodes[node_name]
        self._save_registry()
        print(f"Deleted node '{node_name}' from registry")

    def _get_default_registry_path(self) -> str:
        try:
            # Look for pyproject.toml in the current directory and parent directories
            current_dir = Path.cwd()
            while current_dir != current_dir.parent:
                pyproject_path = current_dir / "pyproject.toml"
                if pyproject_path.exists():
                    with open(pyproject_path, "rb") as f:
                        pyproject_data = tomli.load(f)
                    registry_path = (
                        pyproject_data.get("tool", {})
                        .get("hypernodes", {})
                        .get("node_registry_path")
                    )
                    if registry_path:
                        registry_path = Path(registry_path)
                        if registry_path.is_absolute():
                            if registry_path.exists():
                                return str(registry_path)
                            else:
                                print(
                                    f"Warning: Specified registry path '{registry_path}' "
                                    f"does not exist. Using default."
                                )
                        else:
                            # If it's a relative path, make it relative to the pyproject.toml
                            full_path = pyproject_path.parent / registry_path
                            if full_path.exists():
                                return str(full_path)
                            else:
                                print(
                                    f"Warning: Specified registry path '{full_path}' "
                                    f"does not exist. Using default."
                                )
                current_dir = current_dir.parent

            # print(
            #    "No pyproject.toml found or no valid registry_path specified. Using default."
            # )
        except Exception as e:
            print(f"Error reading pyproject.toml: {e}. Using default registry path.")

        # Default fallback
        default_path = Path.cwd() / "conf" / "node_registry.yaml"
        default_path.parent.mkdir(parents=True, exist_ok=True)
        return str(default_path)
        raise ValueError("No valid registry path found")
