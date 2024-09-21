import json
import os
from pathlib import Path

import pandas as pd
from jinja2 import FileSystemLoader, Environment, select_autoescape
from jinjasql import JinjaSql

from mipi_datamanager.core.database_tools import odbc
from mipi_datamanager.core.common import dict_to_string
from mipi_datamanager.core.database_tools.query import execute_sql


class JinjaWorkSpace:
    """
    This class sets up an instance of Jinja. It allows you to render jinja templates into executable sql scripts.
    Requires all jinja templates to be located within a specified 'root_path' directory.

    back end: this class incorporates a jinjasql instance into a preconfigured jinja2 environment

    """

    def __init__(self, root_path):
        # todo change to packageloader for jungle

        # Jinja Envionment
        self.file_loader = FileSystemLoader(root_path)
        self.environment = Environment(loader=self.file_loader,
                                       autoescape=select_autoescape(
                                           enabled_extensions=['html'],  # Enable autoescape for HTML
                                           disabled_extensions=['txt'],  # Disable autoescape for TXT
                                           default_for_string=False  # Disable autoescape for any other types by default
                                       ))

        # whitespace control
        self.environment.trim_blocks = True
        self.environment.lstrip_blocks = True
        self.environment.keep_trailing_newline = True

        # JinjaSql Env
        self.j = JinjaSql(env=self.environment, param_style='pyformat')

        # Constants
        self.dox_temp_path = Path(__file__).parent.parent / "templates" / "jinja_header.txt"

    def resolve_file(self, temp_inner_path: str, jinja_parameters_dict: dict, header=False) -> str:
        """
        Resolves a template file into a runable query. If dox is provided it will add a header continaing
        documentation and arguments used. to create the query.

        Args:
            temp_inner_path: Path to the template starting from root path
            jinja_parameters_dict:
            dox:

        Returns: SQL query string

        """

        if not jinja_parameters_dict:
            jinja_parameters_dict = {}

        template = self.environment.get_template(temp_inner_path)

        query, bind_parms = self.j.prepare_query(template, jinja_parameters_dict)
        formatted_query = query % bind_parms

        if header is True:
            formatted_query = self._get_header(temp_inner_path,jinja_parameters_dict, bind_parms) + formatted_query

        return formatted_query

    def execute_file(self, temp_inner_path: str, connection: odbc.Odbc, jinja_parameters_dict: dict = None) -> pd.DataFrame:
        """
        Runs the resolved jinja template and retrieves the data from database.

        Args:
            temp_inner_path: Path to the template starting from root path
            jinja_parameters_dict: dictionary of jinja args. keys much match the place holders in the jinja template
            connection: odbc connection object

        Returns: Pandas Dataframe

        """

        sql = self.resolve_file(temp_inner_path, jinja_parameters_dict)
        return execute_sql(sql, connection)

    def _get_header(self, inner_path, jinja_parameters_dict: dict, bind_dict,
                    dox=None) -> str:

        """Creates a header for a jinja template, contains:
        - Header disclamer and best practice reminder
        - search path used for jinja env
        - jinja_parameters_dict assigned
        - bind_parms used for render"""

        search_path = self.file_loader.searchpath

        jinja_parameters_dict = dict_to_string(jinja_parameters_dict)
        bind_parms = dict_to_string(bind_dict)

        with open(self.dox_temp_path, "r") as f:
            header = f.read().format(search_path[0], jinja_parameters_dict, bind_parms, dox)

        return header

    def export_sql(self, inner_path: str, jinja_parameters_dict: dict, out_path) -> None:
        sql = self.resolve_file(str(inner_path), jinja_parameters_dict, header=True)

        with open(out_path, "w") as o:
            o.write(sql)


class JungleWorkSpace(JinjaWorkSpace):
    def __init__(self, root_path):
        # overwrite dox template
        super().__init__(root_path)
        self.dox_temp_path = Path(__file__).parent.parent / "templates" / "jungle_header.txt"
        self.master_config = self._read_master_config(root_path)

    def _get_header(self, inner_path, jinja_parameters_dict: dict, bind_dict, dox=None) -> str:
        _path = Path(inner_path)
        return super()._get_header(inner_path, jinja_parameters_dict, bind_dict,
                                   dox=self.master_config[str(_path.parent)][str(_path.name)]["meta"]["description"])

    @staticmethod
    def _read_master_config(root_path):
        master_config_path = os.path.join(root_path, "master_config.json")
        with open(master_config_path, "r") as f:
            master_config = json.load(f)
        return master_config
