import sys, os, shutil, logging

from typing import Any
from random import randint

def choice_map(message: str, *choices: str, explicit_case: bool = False) -> str:
    while True:
        inp: str = input(f"\n\n\n{message}{"".join(" " * 60)}:").strip()

        inp = inp if explicit_case else inp.lower()

        if inp in choices:
            return inp

def confirmation() -> bool:
    return choice_map("[y]es (confirm) | [n]o (cancel)", "y", "n") == "y"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

CX_FREEZE_SETUP = """
from cx_Freeze import setup, Executable

build_options = {{
    "packages": [],
    "excludes": [
        "PyQt6",
        "PyQt5"
    ]
}}

setup(name="pbm repo",
      version = "1",
      description = "PyForge build",
      options = {{"build_exe": build_options}},
      executables = [Executable("./{}")]
)
"""


class PBM:
    latest_version: str = "v1.2.7"

    def init(self, path: str | None = None) -> None:
        try:
            path = path or sys.argv[2]
        except IndexError:
            logger.fatal(
                "missing pbm repo path, use `python -m pbm init <path>` instead, or `python -m pbm init .` to initialize the current directory.")
            return

        if ".pbm" not in os.listdir(path):
            os.mkdir(f"{path}/.pbm")
            os.mkdir(f"{path}/.pbm/bases")
            os.mkdir(f"{path}/.pbm/bases/main")

            logger.info("pbm repo initialized successfully")

            with open(".pbm/cx_freeze_setup.py", "w") as file:
                file.write(CX_FREEZE_SETUP.format("main.py"))

            self.set_version(self.latest_version)
            self.set_default_base("main")

        else:
            logger.fatal("already a pbm repo in '.', cannot initialize again. use `python -m pbm reinit` instead.")

    @staticmethod
    def get_version():
        try:
            with open(".pbm/init-version") as file:
                return file.read()
        except FileNotFoundError:
            return PBM.latest_version

    @staticmethod
    def get_default_base():
        with open(".pbm/default-base") as file:
            return file.read()

    @staticmethod
    def set_version(cont: str):
        with open(".pbm/init-version", "w") as file:
            return file.write(cont)

    @staticmethod
    def set_default_base(cont: str):
        with open(".pbm/default-base", "w") as file:
            return file.write(cont)

    def set_default_base_endpoint(self, name: str | None = None) -> None:
        name = name or "main"

        logger.warning("this will rename the physical default base directory as well as defaults in commands")
        logger.warning(f"from '{self.get_default_base()}' to '{name}'. this action cannot be undone.")
        logger.warning(f"your bases will be saved and won't be lost during the refactoring.")

        if confirmation():
            try:
                shutil.copytree(f".pbm/bases/{self.get_default_base()}", f".pbm/bases/{name}")
                shutil.rmtree(f".pbm/bases/{self.get_default_base()}")

                self.set_default_base(name)
            except FileNotFoundError:
                logger.error(f"could not find the '{self.get_default_base()}' base. operation cancelled.")

                return

    @staticmethod
    def ensure_pbm_dir() -> None:
        if not os.path.exists(".pbm"):
            logger.fatal("not a pbm repo, no .pbm directory.")
            exit(1)

    def destroy(self) -> bool:
        self.ensure_pbm_dir()

        logger.warning(
            "this will also detonate all bases of the pbm repo IN THE ./ (CURRENT) DIRECTORY. consider using `python -m pbm base export . *` to back up your bases.")
        logger.warning("are you sure you want to continue?")

        if confirmation():
            shutil.rmtree(".pbm")
            logger.info("pbm repo destroyed successfully")
            return True
        else:
            logger.warning("cancelled pbm repo destruction")

        return False

    def reinit(self) -> None:
        self.ensure_pbm_dir()

        old_version = self.get_version()

        if self.destroy():
            self.init(".")
            new_version = self.get_version()

            logger.info(f"pbm repo reinitialized successfully")
            logger.info(f"{old_version} -> {new_version}")
        else:
            logger.warning("cancelled pbm repo reinitialization")

    class Base:
        def __init__(self, pbm_instance: "PBM") -> None:
            self.pbm: PBM = pbm_instance

        def build(self, base: str | None = None, fn: str | None = None) -> None:
            logger.warning(f"this will overwrite your '{base}' build")

            if confirmation():
                self.pbm.ensure_pbm_dir()

                fn = fn or "main.py"

                with open(".pbm/cx_freeze_setup.py", "w") as file:
                    file.write(CX_FREEZE_SETUP.format(fn))

                os.system(f"python .pbm/cx_freeze_setup.py build_exe --build-exe .pbm/bases/{base}/{fn}")

                logger.info("build completed successfully")
            else:
                logger.warning("cancelled standard build")

        def new_base(self, base: str) -> None:
            self.pbm.ensure_pbm_dir()

            if os.path.exists(f".pbm/bases/{base}"):
                logger.warning(f"base '{base}' already exists")
            else:
                os.mkdir(f".pbm/bases/{base}")
                logger.info(f"base '{base}' created successfully")

        @staticmethod
        def export_all(location: str) -> None:
            export_id: int = randint(0, 99999)

            os.mkdir(f".pbm/global_export_{export_id}")
            shutil.make_archive(f"{location.strip('/\\')}/export_g{export_id}", "zip",
                                f".pbm/global_export_{export_id}")
            shutil.copytree(f".pbm/bases", f"{location.strip('/\\')}/g{export_id}.pbm")
            shutil.rmtree(f".pbm/global_export_{export_id}")

            logger.info(f"successfully created global export 'g{export_id}'")

        def export_base(self, location: str, base: str) -> None:
            self.pbm.ensure_pbm_dir()

            export_id: int = randint(0, 999999)

            if base == "*":
                self.export_all(location)
                return

            shutil.make_archive(f"{location.strip('/\\')}/export_{export_id}", "zip", f".pbm/bases/{base}")
            shutil.copytree(f".pbm/bases/{base}", f"{location.strip('/\\')}/{export_id}.pbm")

            logger.info(f"successfully created export '{export_id}'")

        def import_base(self, export_id: str, base: str, location: str | None = None) -> None:
            self.new_base(base)
            self.pbm.ensure_pbm_dir()

            logger.warning(
                "this will also detonate all bases of this pbm repo (and replace them with the imported ones). consider creating a new pbm repo in a separate directory, and merging manually."
            )

            if confirmation():
                location = location or "."
                source_path = f"{location}/{export_id}.pbm"

                if not os.path.exists(source_path):
                    logger.error(f"import failed: {source_path} does not exist.")
                    return

                if export_id.startswith("g"):
                    target_path = ".pbm/bases"
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported global export '{export_id}'")
                else:
                    target_path = f".pbm/bases/{base}"
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported base '{base}' from export '{export_id}'")
            else:
                logger.warning("cancelled base import")

        def delete_base(self, base: str | None = None) -> None:
            self.pbm.ensure_pbm_dir()
            base = base or self.pbm.get_default_base()

            logger.warning(
                f"this will delete your '{base}' build. consider using `python -m pbm export . {base}` to back up this build."
            )
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    shutil.rmtree(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(f"that base '{base}' does not exist.")
                    return

                logger.info("base deleted successfully")
            else:
                logger.warning("cancelled base deletion")

        def detonate(self, base: str | None = None) -> None:
            base = base or self.pbm.get_default_base()

            logger.warning(f"this will detonate your '{base}' build")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    shutil.rmtree(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(f"that build '{base}' does not exist.")
                    return

                os.mkdir(f".pbm/bases/{base}")
                logger.info("base detonated successfully")

            else:
                logger.warning("cancelled base detonation")

    def status(self) -> None:
        self.ensure_pbm_dir()

        version: str = self.get_version()
        default_base: str = self.get_default_base()
        builds: list[str] = os.listdir(".pbm/bases")

        logger.info(f"pbm repository in './': diagnosis")
        logger.info(f"version: {version} ({f"outdated by {self.latest_version}" if self.get_version() != self.latest_version else "up to date"})")
        logger.info(f"default base: {default_base}")
        logger.info(f"available builds: [{', '.join(builds) if builds else 'no bases available'}]")