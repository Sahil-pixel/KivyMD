"""
Script creates a project with the MVC pattern
=============================================

.. versionadded:: 1.0.0

.. seealso::

    `MVC pattern <https://en.wikipedia.org/wiki/Model–view–controller>`_

.. rubric:: Use a clean architecture for your applications.

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/preview-mvc.png
    :align: center

Use a clean architecture for your applications. KivyMD allows you to quickly
create a project template with the MVC pattern. So far, this is the only
pattern that this utility offers. You can also include database support in
your project. At the moment, support for the Firebase database
(the basic implementation of the real time database) and RestDB
(the full implementation) is available.

Project creation
----------------

Template command::

    python -m kivymd.tools.patterns.create_project \\
        name_pattern \\
        path_to_project \\
        name_project \\
        python_version \\
        kivy_version

Example command::

    python -m kivymd.tools.patterns.create_project \\
        MVC \\
        /Users/macbookair/Projects \\
        MyMVCProject \\
        python3.10 \\
        2.1.0

This command will by default create a project with an MVC pattern.
Also, the project will create a virtual environment with Python 3.10,
Kivy version 2.1.0 and KivyMD master version.

.. note::
    Please note that the Python version you specified must be installed on your
    computer.

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/mvc-base.png
    :align: center

Creating a project using a database
-----------------------------------

.. note::
    Note that in the following command, you can use one of two database names:
    'firebase' or 'restdb'.

Template command::

    python -m kivymd.tools.patterns.create_project \\
        name_pattern \\
        path_to_project \\
        name_project \\
        python_version \\
        kivy_version \\
        --name_database

Example command::

    python -m kivymd.tools.patterns.create_project \\
        MVC \\
        /Users/macbookair/Projects \\
        MyMVCProject \\
        python3.10 \\
        2.1.0 \\
        --name_database restdb

This command will create a project with an MVC template by default.
The project will also create a virtual environment with Python 3.10,
Kivy version 2.1.0, KivyMD master version and a wrapper for working with
the database restdb.io.

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/mvc-database.png
    :align: center

.. note::
    Please note that database.py the shell in the `DataBase` class uses the
    `database_url` and `api_key` parameters on the test database (works only in read mode),
    so you should use your data for the database.

.. code-block:: python

    class DataBase:
        def __init__(self):
            database_url = "https://restdbio-5498.restdb.io"
            api_key = "7ce258d66f919d3a891d1166558765f0b4dbd"

Preview of the basic MVS template using the RestDB database
-----------------------------------------------------------

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/mvc-restbd-preview.png
    :align: center

Create project with hot reload
------------------------------

Template command::

    python -m kivymd.tools.patterns.create_project \\
        name_pattern \\
        path_to_project \\
        name_project \\
        python_version \\
        kivy_version \\
        --use_hotreload

Example command::

    python -m kivymd.tools.patterns.create_project \\
        MVC \\
        /Users/macbookair/Projects \\
        MyMVCProject \\
        python3.10 \\
        2.1.0 \\
        --use_hotreload yes

After creating the project, open the file `main.py`, there is a lot of useful
information. Also, the necessary information is in other modules of the project
in the form of comments. So do not forget to look at the source files of the
created project.

Others command line arguments
======================

Required Arguments
------------------

- pattern
    - the name of the pattern with which the project will be created

- directory
    - directory in which the project will be created

- name
    - project name

- python_version
    - the version of Python (specify as `python3.9` or `python3.8`) with
    - which the virtual environment will be created

- kivy_version
    - version of Kivy (specify as `2.1.0` or `master`) that will be used in the project

Optional arguments
------------------

- name_screen
    - the name of the class which be used when creating the project pattern

- name_database
    - provides a basic template for working with the 'firebase' library
    - or a complete implementation for working with a database 'restdb.io'

- use_hotreload
    - creates a hot reload entry point to the application

-use_localization
    - creates application localization files

.. warning:: On Windows, hot reloading of Python files may not work.
    But, for example, there is no such problem in macOS. If you fix this,
    please report it to the KivyMD community.
"""

import os
import re
import shutil
from typing import Union

from kivy import Logger, platform

from kivymd import path as kivymd_path
from kivymd.tools.argument_parser import ArgumentParserWithHelp

_database_model = '''import multitasking

from Model.base_model import BaseScreenModel

multitasking.set_max_threads(10)


class {name_screen}Model(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.{name_screen}.{module_name}.{name_screen}View` class.
    """

    def __init__(self, database):
        self.database = database
        # Dict:
        #     'login': 'KivyMD'
        #     'password': '1111'
        self.user_data = dict()
        self._data_validation_status = None

    @property
    def data_validation_status(self):
        return self._data_validation_status

    @data_validation_status.setter
    def data_validation_status(self, value):
        self._data_validation_status = value
        # We notify the View -
        # :class:`~View.{name_screen}.{module_name}.{name_screen}View` about the
        # changes that have occurred in the data model.
        self.notify_observers({notify_name_screen})

    @multitasking.task
    def check_data(self):
        """
        Get data from the database and compares this data with the data entered
        by the user. This method is completely asynchronous.
        It does not return any value.
        """

        data = self.database.get_data_from_collection(self.database.USER_DATA)
        data_validation_status = False

        if data:
            if self.database.name == "RestDB":
                data = data[0]
            else:
                data = list(data.values())[0]
            if (
                data["login"] == self.user_data["login"]
                and data["password"] == self.user_data["password"]
            ):
                data_validation_status = True
        self.data_validation_status = data_validation_status

    def set_user_data(self, key: str, value: str) -> None:
        """Sets a dictionary of data that the user enters."""

        self.user_data[key] = value

    def reset_data_validation_status(self) -> None:
        self.data_validation_status = None
'''

_without_database_model = '''from Model.base_model import BaseScreenModel


class {name_screen}Model(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.{module_name}.{name_screen}.{name_screen}View` class.
    """'''

_database_controller = '''
{import_module}


class {name_screen}Controller:
    """
    The `{name_screen}Controller` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.{module_name}.{name_screen}Model object
        self.view = {name_view}(
            controller=self, model=self.model
        )

    def set_user_data(self, key: str, value: str) -> None:
        """Called every time the user enters text into the text fields."""

        self.model.set_user_data(key, value)

    def on_tap_button_login(self) -> None:
        """Called when the `LOGIN` button is pressed."""

        self.view.show_dialog_wait()
        self.model.check_data()

    def reset_data_validation_status(self, *args) -> None:
        self.model.reset_data_validation_status()
'''

_without_database_controller = '''
{import_module}


class {name_screen}Controller:
    """
    The `{name_screen}Controller` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.{module_name}.{name_screen}Model
        self.view = {name_view}(controller=self, model=self.model)

    def on_tap_button_login(self) -> None:
        """Called when the `LOGIN` button is pressed."""

    def set_user_data(self, key, value) -> None:
        """Called every time the user enters text into the text fields."""
'''

_database_view_import = """from typing import Union

from kivy.clock import Clock

from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
"""

_without_database_view_import = """
"""

_database_view_methods = '''    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()
        self.dialog.bind(on_dismiss=self.controller.reset_data_validation_status)

    def show_dialog_wait(self) -> None:
        """Displays a wait dialog while the model is processing data."""

        self.dialog.auto_dismiss = False
        self.dialog.text = "Data validation..."
        self.dialog.open()

    def show_toast(self, interval: Union[int, float]) -> None:
        Snackbar(
            text="You have passed the verification successfully!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.8,
            bg_color=self.theme_cls.primary_color,
        ).open()
'''

_database_view_model_is_changed_method = """if self.model.data_validation_status:
            self.dialog.dismiss()
            Clock.schedule_once(self.show_toast, 1)
        if self.model.data_validation_status is False:
            self.dialog.text = "Wrong data!"
            self.dialog.auto_dismiss = True
"""

_firebase_requirements = """kivy==2.1.0
kivymd==1.0.0
multitasking
firebase
firebase-admin
python_jwt
gcloud
sseclient
pycryptodome==3.4.3
requests_toolbelt
"""

_without_firebase_requirements = """kivy==2.1.0
kivymd==1.0.0
"""

_hot_reload_main = '''
"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
DEBUG=1 python main.py
"""

import importlib
import os

from kivy import Config
from kivy.uix.screenmanager import ScreenManager

from PIL import ImageGrab

# TODO: You may know an easier way to get the size of a computer display.
resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", resolution[1])
Config.set("graphics", "width", "400")

from kivy.core.window import Window%s

# Place the application window on the right side of the computer screen.
Window.top = 0
Window.left = resolution[0] - Window.width

from kivymd.tools.hotreload.app import MDApp
%s%s

class %s(MDApp):
    KV_FILES = {
        os.path.join(
            os.getcwd(),
            "View",
            "%s",
            "%s.kv",
        ),
    }%s

    def build_app(self) -> ScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """

        import View.screens

        self.theme_cls.primary_palette = "Orange"
        self.manager_screens = ScreenManager()%s%s
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"](%s)
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

        return self.manager_screens

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()%s%s


%s().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.
'''

available_patterns = ["MVC"]
available_databases = ["firebase", "restdb"]


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    pattern_name = args.pattern
    project_directory = args.directory
    project_name = "".join(args.name.split(" "))
    kivy_version = args.kivy_version
    python_version = args.python_version
    if "3" not in python_version:
        parser.error("Python must be at least version 3")
    name_screen = "".join(args.name_screen.split(" "))
    path_to_project = os.path.join(project_directory, project_name)
    name_database = args.name_database
    if name_database != "no" and name_database not in available_databases:
        parser.error(
            f"The database name must be one of the {available_databases} list"
        )
    use_hotreload = args.use_hotreload
    use_localization = args.use_localization

    # Check arguments.
    if name_screen[-6:] != "Screen":
        parser.error(
            "Name of the screen must contain the word 'Screen' at the end. "
            "\nFor example - '... --name_screen MyFirstScreen'"
        )
    module_name = chek_camel_case_name_project(name_screen)
    if not module_name:
        parser.error(
            "The name of the screen should be written in camel case style. "
            "\nFor example - 'MyFirstScreen'"
        )
    module_name = "_".join([name.lower() for name in module_name])
    if not os.path.exists(
        os.path.join(kivymd_path, "tools", "patterns", pattern_name)
    ):
        parser.error(
            f"There is no {pattern_name} pattern.\n"
            f"Only {available_patterns} template is available."
        )

    # Call the functions of creating a project.
    if not os.path.exists(path_to_project):
        shutil.copytree(
            os.path.join(kivymd_path, "tools", "patterns", pattern_name),
            path_to_project,
        )
        create_main(
            name_database, use_localization, path_to_project, project_name
        )
        create_model(name_database, name_screen, module_name, path_to_project)
        create_controller(
            name_database,
            use_hotreload,
            name_screen,
            module_name,
            path_to_project,
        )
        create_view(
            name_database,
            use_localization,
            name_screen,
            module_name,
            path_to_project,
        )
        create_requirements(name_database, path_to_project)
        os.makedirs(os.path.join(path_to_project, "assets", "images"))
        os.mkdir(os.path.join(path_to_project, "assets", "fonts"))
        rename_ext_py_tmp_to_py(path_to_project)
        move_init(path_to_project, name_screen)

        if name_database != "no":
            check_databases(name_database, path_to_project)

        if use_hotreload == "yes":
            create_main_with_hotreload(
                path_to_project,
                project_name,
                name_screen,
                module_name,
                name_database,
                use_localization,
            )
            with open(
                os.path.join(path_to_project, "requirements.txt"),
                "a",
                encoding="utf-8",
            ) as requirements:
                requirements.write("watchdog")

        if use_localization == "yes":
            Logger.info("KivyMD: Create localization files...")
            create_makefile(
                path_to_project, project_name, module_name, name_screen
            )
            localization_po_file(path_to_project)
            create_mofile(path_to_project)
        else:
            os.remove(os.path.join(path_to_project, "messages.pot"))
            os.remove(os.path.join(path_to_project, "libs", "translation.py"))
            shutil.rmtree(os.path.join(path_to_project, "data"))
        Logger.info(f"KivyMD: Project '{path_to_project}' created")
        Logger.info(
            f"KivyMD: Create a virtual environment for '{path_to_project}' project..."
        )
        create_virtual_environment(python_version, path_to_project)
        Logger.info(
            f"KivyMD: Install requirements for '{path_to_project}' project..."
        )
        install_requirements(path_to_project, kivy_version, name_database)
    else:
        parser.error(f"The {path_to_project} project already exists")


def create_main_with_hotreload(
    path_to_project: str,
    project_name: str,
    name_screen: str,
    module_name: str,
    name_database: str,
    use_localization: str,
) -> None:
    with open(
        os.path.join(path_to_project, "main.py"), encoding="utf-8"
    ) as main_file:
        main_code = ""
        for string in main_file.readlines():
            main_code += f"# {string}"
    with open(
        os.path.join(path_to_project, "main.py"), "w", encoding="utf-8"
    ) as main_file:
        main_file.write(f"{_hot_reload_main}\n{main_code}")

    replace_in_file(
        os.path.join(path_to_project, "main.py"),
        (
            "\nfrom kivy.properties import StringProperty"
            if use_localization == "yes"
            else "",
            "\nfrom Model.database import DataBase" if name_database != "no" else "",
            "\nfrom libs.translation import Translation\n"
            if use_localization == "yes"
            else "",
            project_name,
            name_screen,
            module_name,
            '\n    lang = StringProperty("en")\n'
            if use_localization == "yes"
            else "",
            "\n        self.base = DataBase()\n" if name_database != "no" else "",
            "\n        self.translation = Translation(\n"
            '            self.lang, "%s", f"{self.directory}/data/locales"'
            "\n        )" % project_name
            if use_localization == "yes"
            else "",
            "self.database" if name_database != "no" else "",
            "\n\n    def on_lang(self, instance_app, lang_value: str) -> None:\n"
            "        self.translation.switch_lang(lang_value)\n"
            if use_localization == "yes"
            else "",
            "\n    def switch_lang(self) -> None:\n"
            '        """Switch lang."""\n\n'
            '        self.lang = "ru" if self.lang == "en" else "en"'
            if use_localization == "yes"
            else "",
            project_name,
        ),
    )


def create_main(
    name_database: str,
    use_localization: str,
    path_to_project: str,
    project_name: str,
) -> None:
    replace_in_file(
        os.path.join(path_to_project, "main.py_tmp"),
        (
            "\nfrom kivy.properties import StringProperty"
            if use_localization == "yes"
            else "",
            "\nfrom libs.translation import Translation"
            if use_localization == "yes"
            else "",
            "from Model.database import DataBase\n" if name_database != "no" else "",
            project_name,
            '\n    lang = StringProperty("en")\n'
            if use_localization == "yes"
            else "",
            "\n        self.translation = Translation(\n"
            '            self.lang, "%s", f"{self.directory}/data/locales"'
            "\n        )" % project_name
            if use_localization == "yes"
            else "",
            "self.database = DataBase()\n" if name_database != "no" else "",
            "self.database" if name_database != "no" else "",
            "\n    def on_lang(self, instance_app, lang_value: str) -> None:\n"
            "        self.translation.switch_lang(lang_value)\n"
            if use_localization == "yes"
            else "",
            "\n    def switch_lang(self) -> None:\n"
            '        """Switch lang."""\n\n'
            '        self.lang = "ru" if self.lang == "en" else "en"\n'
            if use_localization == "yes"
            else "",
            project_name,
        ),
    )


def create_model(
    name_database: str, name_screen: str, module_name: str, path_to_project: str
) -> None:
    if name_database != "no":
        database_model = _database_model.format(
            name_screen=name_screen,
            module_name=module_name,
            notify_name_screen=f'"{" ".join(module_name.split("_"))}"',
        )
        replace_in_file(
            os.path.join(path_to_project, "Model", "first_screen.py_tmp"),
            (database_model),
        )
    else:
        without_database_model = _without_database_model.format(
            module_name=module_name, name_screen=name_screen
        )
        replace_in_file(
            os.path.join(path_to_project, "Model", "first_screen.py_tmp"),
            (without_database_model),
        )
        os.remove(os.path.join(path_to_project, "Model", "database_firebase.py"))
        os.remove(os.path.join(path_to_project, "Model", "database_restdb.py"))
    os.rename(
        os.path.join(path_to_project, "Model", "first_screen.py_tmp"),
        os.path.join(path_to_project, "Model", f"{module_name}.py_tmp"),
    )


def create_controller(
    name_database: str,
    use_hotreload: str,
    name_screen: str,
    module_name: str,
    path_to_project: str,
) -> None:
    if name_database != "no":
        database_controller = _database_controller
    else:
        database_controller = _without_database_controller
    name_view = (
        f"View.{name_screen}.{module_name}.{name_screen}View"
        if use_hotreload == "yes"
        else f"{name_screen}View"
    )
    database_controller = database_controller.format(
        name_screen=name_screen,
        module_name=module_name,
        import_module=""
        f"import importlib\n\n"
        f"import View.{name_screen}.{module_name}\n\n"
        f"# We have to manually reload the view module in order to apply the\n"
        f"# changes made to the code on a subsequent hot reload.\n"
        f"# If you no longer need a hot reload, you can delete this instruction.\n"
        f"importlib.reload(View.{name_screen}.{module_name})"
        if use_hotreload == "yes"
        else f"\nfrom View.{name_screen}.{module_name} import {name_screen}View",
        name_view=name_view,
    )
    replace_in_file(
        os.path.join(path_to_project, "Controller", "first_screen.py_tmp"),
        (database_controller, name_view),
    )
    os.rename(
        os.path.join(path_to_project, "Controller", "first_screen.py_tmp"),
        os.path.join(path_to_project, "Controller", f"{module_name}.py_tmp"),
    )


def create_view(
    name_database: str,
    use_localization: str,
    name_screen: str,
    module_name: str,
    path_to_project: str,
) -> None:
    replace_in_file(
        os.path.join(path_to_project, "View", "screens.py_tmp"),
        (
            module_name,
            f"{name_screen}Model",
            module_name,
            f"{name_screen}Controller",
            f'"{" ".join(module_name.split("_"))}"',
            f"{name_screen}Model",
            f"{name_screen}Controller",
        ),
    )
    replace_in_file(
        os.path.join(path_to_project, "View", "FirstScreen", "first_screen.kv"),
        (
            f"{name_screen}View",
            name_screen,
            "app.switch_lang()" if use_localization == "yes" else "x",
            'app.translation._("To log in, enter your personal data:")'
            if use_localization == "yes"
            else '"To log in, enter your personal data:"',
            'app.translation._("Login")'
            if use_localization == "yes"
            else '"Login"',
            'app.translation._("Password")'
            if use_localization == "yes"
            else '"Password"',
            'app.translation._("LOGIN")'
            if use_localization == "yes"
            else '"LOGIN"',
        ),
    )
    replace_in_file(
        os.path.join(
            path_to_project, "View", "FirstScreen", "first_screen.py_tmp"
        ),
        (
            _database_view_import
            if name_database != "no"
            else _without_database_view_import,
            f"{name_screen}View",
            _database_view_methods if name_database != "no" else "",
            _database_view_model_is_changed_method
            if name_database != "no"
            else "",
        ),
    )
    replace_in_file(
        os.path.join(path_to_project, "View", "base_screen.py_tmp"),
        (
            module_name,
            f"{name_screen}Model",
            module_name,
            f"{name_screen}Controller",
            module_name,
            f"{name_screen}Model",
        ),
    )
    os.rename(
        os.path.join(path_to_project, "View", "base_screen.py_tmp"),
        os.path.join(path_to_project, "View", "base_screen.py"),
    )
    os.rename(
        os.path.join(path_to_project, "View", "FirstScreen", "first_screen.kv"),
        os.path.join(
            path_to_project, "View", "FirstScreen", f"{module_name}.kv"
        ),
    )
    os.rename(
        os.path.join(
            path_to_project, "View", "FirstScreen", "first_screen.py_tmp"
        ),
        os.path.join(
            path_to_project, "View", "FirstScreen", f"{module_name}.py_tmp"
        ),
    )
    os.rename(
        os.path.join(path_to_project, "View", "FirstScreen"),
        os.path.join(path_to_project, "View", name_screen),
    )


def create_requirements(name_database: str, path_to_project: str) -> None:
    with open(
        os.path.join(path_to_project, "requirements.txt"), "w", encoding="utf-8"
    ) as requirements:
        requirements.write(
            _firebase_requirements
            if name_database != "no"
            else _without_firebase_requirements
        )


def create_makefile(
    path_to_project: str, project_name: str, module_name: str, name_screen: str
) -> None:
    replace_in_file(
        os.path.join(path_to_project, "Makefile"),
        (
            name_screen,
            module_name,
            name_screen,
            module_name,
            project_name,
            project_name,
        ),
    )
    os.chdir(path_to_project)
    os.system("make po")


def create_mofile(path_to_project: str) -> None:
    os.chdir(path_to_project)
    os.system("make mo")


def create_virtual_environment(
    python_version: str, path_to_project: str
) -> None:
    os.system(f"{python_version} -m pip install virtualenv")
    os.system(
        f"virtualenv -p {python_version} {os.path.join(path_to_project, 'venv')}"
    )


def localization_po_file(path_to_project: str) -> None:
    path_to_file_po = os.path.join(
        path_to_project, "data", "locales", "po", "ru.po"
    )
    with open(path_to_file_po, "rt", encoding="utf-8") as file_po:
        file_po_content = (
            file_po.read()
            .replace(
                'msgid "To log in, enter your personal data:"\nmsgstr ""',
                'msgid "To log in, enter your personal data:"\nmsgstr "Для входа введите свои личные данные"',
            )
            .replace(
                'msgid "Login"\nmsgstr ""', 'msgid "Login"\nmsgstr "Логин"'
            )
            .replace(
                'msgid "Password"\nmsgstr ""',
                'msgid "Password"\nmsgstr "Пароль"',
            )
            .replace(
                'msgid "LOGIN"\nmsgstr ""', 'msgid "LOGIN"\nmsgstr "ЛОГИН"'
            )
        )
    with open(path_to_file_po, "wt", encoding="utf-8") as file_po:
        file_po.write(file_po_content)


def install_requirements(
    path_to_project: str, kivy_version: str, name_database: str
) -> None:
    python = os.path.join(path_to_project, "venv", "bin", "python3")
    if kivy_version == "master":
        if platform == "macosx":
            os.system(
                f"{python} -m pip install 'kivy[base] @ https://github.com/kivy/kivy/archive/master.zip'"
            )
        else:
            os.system(
                f"{python} -m pip install https://github.com/kivy/kivy/archive/master.zip"
            )
    elif kivy_version == "stable":
        os.system(f"{python} -m pip install kivy")
    else:
        os.system(f"{python} -m pip install kivy=={kivy_version}")
    os.system(
        f"{python} -m pip install https://github.com/kivymd/KivyMD/archive/master.zip"
    )
    os.system(f"{python} -m pip install watchdog")
    if name_database == "firebase":
        os.system(
            f"{python} -m pip install "
            f"multitasking "
            f"firebase "
            f"firebase-admin "
            f"python_jwt "
            f"gcloud "
            f"sseclient "
            f"pycryptodome==3.4.3 "
            f"requests_toolbelt "
            f"watchdog "
        )
    os.system(
        f"{os.path.join(path_to_project, 'venv', 'bin', 'python3')} -m pip list"
    )


def rename_ext_py_tmp_to_py(path_to_project: str) -> None:
    for path_to_dir, dirs, files in os.walk(path_to_project):
        for name_file in files:
            if os.path.splitext(name_file)[1] == ".py_tmp":
                os.rename(
                    os.path.join(path_to_dir, name_file),
                    os.path.join(
                        path_to_dir, f"{os.path.splitext(name_file)[0]}.py"
                    ),
                )


def move_init(path_to_project: str, name_screen: str) -> None:
    path_to_init_file = __file__.replace("create_project", "__init__")
    for name_dir in ("Controller", "Model", "Utility", "View"):
        shutil.copy(
            path_to_init_file,
            os.path.join(path_to_project, name_dir, "__init__.py"),
        )
    shutil.copy(
        path_to_init_file,
        os.path.join(path_to_project, "View", name_screen, "__init__.py"),
    )
    path_to_components = os.path.join(
        path_to_project, "View", name_screen, "components"
    )
    os.mkdir(path_to_components)
    shutil.copy(
        path_to_init_file, os.path.join(path_to_components, "__init__.py")
    )


def check_databases(name_database: str, path_to_project: str) -> None:
        databases = {"firebase": "restdb", "restdb": "firebase"}
        os.remove(
            os.path.join(
                path_to_project, "Model", f"database_{databases[name_database]}.py"
            )
        )
        os.rename(
            os.path.join(
                path_to_project, "Model", f"database_{name_database}.py"
            ),
            os.path.join(
                path_to_project, "Model", f"database.py"
            ),
        )


def chek_camel_case_name_project(name_project) -> Union[bool, list]:
    result = re.findall("[A-Z][a-z]*", name_project)
    if len(result) == 1:
        return False
    return result


def replace_in_file(path_to_file: str, args) -> None:
    with open(path_to_file, "rt", encoding="utf-8") as file_content:
        new_file_content = file_content.read() % (args)
        with open(path_to_file, "wt", encoding="utf-8") as original_file:
            original_file.write(new_file_content)


def create_argument_parser() -> ArgumentParserWithHelp:
    parser = ArgumentParserWithHelp(
        prog="create_project.py",
        allow_abbrev=False,
    )
    parser.add_argument(
        "pattern",
        help="the name of the pattern with which the project will be created.",
    )
    parser.add_argument(
        "directory",
        help="directory in which the project will be created.",
    )
    parser.add_argument(
        "name",
        help="project name.",
    )
    parser.add_argument(
        "python_version",
        help="the version of Python (specify as `python3.9` or `python3.8`) "
        "with which the virtual environment will be created.",
    )
    parser.add_argument(
        "kivy_version",
        help="version of Kivy (specify as `2.1.0` or `master`) that will be "
        "used in the project.",
    )
    parser.add_argument(
        "--name_screen",
        default="MainScreen",
        help="the name of the class wich be used when creating the project pattern.",
    )
    parser.add_argument(
        "--name_database",
        default="no",
        help="name of the database provider ('firebase' or 'restdb').",
    )
    parser.add_argument(
        "--use_hotreload",
        default="no",
        help="creates a hot reload entry point to the application.",
    )
    parser.add_argument(
        "--use_localization",
        default="no",
        help="creates application localization files.",
    )
    return parser


if __name__ == "__main__":
    main()
