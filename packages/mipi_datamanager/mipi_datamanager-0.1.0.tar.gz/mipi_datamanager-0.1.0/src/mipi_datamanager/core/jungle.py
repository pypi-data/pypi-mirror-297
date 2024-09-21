from pathlib import Path
import json
import os


class Jungle:
    def __init__(self, root_dir = None, conn_list = None):

        if root_dir is None:
            _path = os.environ.get("JUNGLE_PATH")
        else:
            _path = root_dir

        self.root_dir = Path(_path)


        self.conn_list = conn_list#TODO check master config for connections


    @property
    def path_master_config(self):
        return self.root_dir / "master_config.json"

    def pull_master_config(self):
        with open (self.path_master_config, "r") as f:
            data = json.load(f)
        return data

    def push_master_config(self,master_config):
        with open(self.path_master_config, 'w') as f:
            json.dump(master_config, f, indent=4)

    def pull_sql(self, inner_path):
        path = self.root_dir.joinpath(inner_path)
        with open(path, "r") as f:
            sql = f.read()
        return sql

    def push_sql(self,inner_path,sql):

        path_full = self.root_dir/inner_path
        print(self.root_dir)
        print(path_full)

        path_full.parent.mkdir(parents = True, exist_ok = True)

        with open(path_full, "w", newline="") as f:
            f.write(sql)

    def delete_sql(self, inner_path):
        path = self.root_dir.joinpath(inner_path)

        # Delete the SQL file
        if path.exists():
            path.unlink()
            print(f"Deleted file: {path}")

        # Remove any empty directories
        parent_dir = path.parent
        while parent_dir != self.root_dir and not any(parent_dir.iterdir()):
            parent_dir.rmdir()
            print(f"Deleted empty directory: {parent_dir}")
            parent_dir = parent_dir.parent

    def __repr__(self):
        return f"Jungle repository at: {self.root_dir}"