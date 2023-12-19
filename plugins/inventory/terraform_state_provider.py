# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later


# python imports
import subprocess
import shutil
import tempfile
import re
import json

# Ansible imports
from ansible.module_utils.common import process
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

class TerraformInventoryError(Exception):
    pass

def _clean(var_str):
    return re.sub(r'\W|^(?=\d)','_', var_str)

# flatten json data to make it easier to set as variables
def flatten_json(y):
    out = {}

    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if isinstance(x, dict):

            for a in x:
                flatten(x[a], name + a + '_')

        # If the Nested key-value
        # pair is of list type
        elif isinstance(x, list):

            i = 0

            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# resource filtering function logic
def filter_function(type_list, tag_list, address_list):
    def myfilter(x):
        if type_list is not None and len(type_list) > 0:
            if not x['type'] in type_list:
                return False

        if address_list is not None and len(address_list) > 0:
            found = False
            for taddress in address_list:
                if re.search(taddress, x['address']):
                    found = True
                    break

            if not found:
                return found

        if tag_list is not None and len(tag_list) > 0:
            found = False
            for tagset in tag_list:
                setkey = next(iter(tagset))
                setval = tagset[setkey]
                if setkey in x['values']['tags_all']:
                    if re.search(setval, x['values']['tags_all'][setkey]):
                        found = True
                        break

            if not found:
                return found

        return True

    return myfilter

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "cloud.terraform.terraform_state_provider"

    project_path = None
    terraform_binary = None
    type_list = []
    address_list = []
    tag_list = []
    ip_param = []
    remote_state = None

    attr_keys = [
        "arn", "ami",
    ]

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('tf.yaml', 'tf.yml')):
                return True
        return False


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        cfg = self._read_config_data(path)
        self.project_path = cfg.get("project_path", None)
        self.terraform_binary = cfg.get("binary_path", None)
        self.type_list = cfg.get("type_list", [])
        self.address_list = cfg.get("address_list", [])
        self.ip_param = cfg.get("access_param", ["public_ip"])
        self.remote_state = cfg.get('remote_state', None)

        if isinstance(self.project_path, str):
            self.project_path = [self.project_path]

        if isinstance(self.type_list, str):
            self.type_list = [self.type_list]

        if isinstance(self.address_list, str):
            self.address_list = [self.address_list]

        # project_path must exist
        if self.project_path is None:
            raise TerraformInventoryError("project_path must exist")

        # validate and raise exception if terraform binary does not exist
        if self.terraform_binary is not None:
            if not shutil.which(self.terraform_binary):
                raise TerraformInventoryError(
                    f"Path for terraform_binary '{self.terraform_binary}' does not exist"
                )
        else:
            self.terraform_binary = process.get_bin_path("terraform", required=True)

        my_filter = filter_function(self.type_list, self.address_list, self.tag_list)

        for item in self.project_path:
            tempdir = None
            tdir = None
            try:
                if "git" in item:
                    tempdir = tempfile.mkdtemp()
                    tdir = tempdir
                    self._clone_gitrepo(tdir, item['git'])
                else:
                    tdir = item['path']

                init_cmd = self._build_tf_command(tdir, item)
                self.run_subprocess(init_cmd, tdir)
                show_cmd = self._build_tf_command(tdir, item, cmd_type="show")
                json_data = json.loads(self.run_subprocess(show_cmd, tdir)[1])
                if not "values" in json_data:
                    raise TerraformInventoryError(
                      f"Invalid result from show.  Project may be missing remote state: {json_data}"
                    )
                filtered_list = list(
                    filter(
                        my_filter,
                        json_data['values']['root_module']['resources']
                    )
                )
                self.inventory_from_show(inventory, filtered_list)
            finally:
                if tempdir is not None:
                    shutil.rmtree(tempdir, ignore_errors=True)

    def inventory_from_show(self, inventory, filtered_show_result):
        for resource in filtered_show_result:
            if "values" in resource:
                address = resource['address']

                for key in self.ip_param:
                    if not key in resource["values"]:
                        continue
                    inventory.add_host(address)
                    inventory.set_variable(
                        address, "ansible_host", resource['values'][key]
                    )
                    flattened_values = flatten_json(resource['values'])
                    for key, val in flattened_values.items():
                        if val is not None:
                            inventory.set_variable(address, key, val)

                    if "tags_all" in resource["values"]:
                        for tag_key, tag_val in resource['values']['tags_all'].items():
                            inventory.add_group(_clean(f"tag_{tag_key}_{tag_val}"))
                            inventory.add_child(_clean(f"tag_{tag_key}_{tag_val}"), address)
                    break

    def raise_for_status(self, cmd_result, cmd):
        if cmd_result[0] != 0:
            raise TerraformInventoryError(
                f"Command returned non-zero return code: {cmd_result[0]} " +
                f"from {cmd} - stderr:{cmd_result[1]} stdout:{cmd_result[2]}")

    def _clone_gitrepo(self, cwd, repo):
        return self.run_subprocess(["git", "clone", repo], cwd)

    def _build_backend(self, backend_dir, backend_type):
        backend_config = f'''
terraform {{
    backend "{backend_type}" {{}}
}}
'''
        with open(f"{backend_dir}/backend_{backend_type}.tf", "w", encoding="utf-8") as file:
            file.write(backend_config)

    def _build_tf_command(self, cwd, item, cmd_type="init"):
        cmd = [self.terraform_binary]
        if cmd_type == "init":
            cmd.append("init")
        elif cmd_type == "show":
            cmd.extend(["show", "-json"])
            return cmd
        else:
            raise TerraformInventoryError(
                f"Unexpected command type {cmd_type}, expected on 'init' or 'show'")
        if "remote_state" in item:
            self._build_backend(cwd, item['remote_state']['type'])
            for key,val in item['remote_state'].items():
                if key != "type":
                    cmd.extend(["-backend-config", f"{key}={val}"])

        return cmd

    def run_subprocess(self, cmd, cwd, check=False, raise_for_status=True):
        cmd_result = None
        cmd_result = subprocess.run(cmd, capture_output=True, check=check, cwd=cwd)
        if cmd_result.returncode != 0 and raise_for_status:
            raise TerraformInventoryError(
                f"Error running {cmd}: {cmd_result.returncode}\n" +
                f" -- {cmd_result.stderr.decode('utf-8')}\n"
                f" -- {cmd_result.stdout.decode('utf-8')}"
            )
        return (
            cmd_result.returncode,
            cmd_result.stdout.decode("utf-8"),
            cmd_result.stderr.decode("utf-8")
        )
