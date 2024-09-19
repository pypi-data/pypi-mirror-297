import os
import shlex
import tarfile
from pathlib import Path
from typing import Mapping
from contextlib import contextmanager
import shutil

import yaml
from ploomber.env.envdict import EnvDict

from ploomber.util.default import path_to_env_from_spec

from ploomber.io._commander import CommanderStop
from ploomber_core.telemetry import telemetry

from soopervisor.commons import source, dependencies
from soopervisor.exceptions import (
    ConfigurationError,
    MissingDockerfileError,
    ConfigurationFileTypeError,
)


def _validate_repository(repository):
    if repository == "your-repository/name":
        raise ConfigurationError(
            f"Invalid repository {repository!r} "
            "in soopervisor.yaml, please add a valid value."
        )


def cp_ploomber_home(pkg_name):
    # Generate ploomber home
    home_path = Path(telemetry.get_home_dir(), "stats")
    home_path = home_path.expanduser()

    if home_path.exists():
        target = Path("dist", f"{pkg_name}.tar.gz")
        archive = tarfile.open(target, "w:gz")
        archive.add(home_path, arcname="ploomber/stats")
        archive.close()


def modify_wildcard(entity):
    return entity.replace("*", "ploomber")


def get_dependencies():
    """
    Fetch all dependency files and corresponding lock files
    mapped to corresponding task patterns, e.g., requirements.fit-__.txt
    and requirements.fit-__.lock.txt mapped to pattern fit-*.
    """

    requirement_files = dependencies.get_task_dependency_files("requirements", "txt")
    dependency_files = (
        requirement_files
        if requirement_files
        else dependencies.get_task_dependency_files("environment", "yml")
    )

    lock_paths = {task: paths["lock"] for task, paths in dependency_files.items()}
    return dependency_files, lock_paths


@contextmanager
def prepare_env_file(entry_point: str):
    """
    Given an entrypoint pipeline.yaml file determine the env.yaml in use
    and populate it with the default placeholders or ignore them if
    they already exist. The env file will be created in the root of
    the pipeline file if one doesn't exist.
    """
    path_to_env = path_to_env_from_spec(entry_point)
    user_provided_env = path_to_env is not None

    if user_provided_env:
        env_default = EnvDict({}, path_to_here=Path(path_to_env).parent)

        env_data = yaml.safe_load(Path(path_to_env).read_text())
        if not isinstance(env_data, Mapping):
            raise ConfigurationFileTypeError(path_to_env, env_data)
        env_data = dict(env_data)
        if "git" in env_default:
            env_data.setdefault("git", env_default["git"])
        if "git_hash" in env_default:
            env_data.setdefault("git_hash", env_default["git_hash"])
        if "build_time" in env_default:
            env_data.setdefault("build_time", env_default["build_time"])
    else:
        path_to_env = Path(entry_point).parents[0] / "env.yaml"
        env_default = EnvDict({}, path_to_here=Path(path_to_env).parent)
        env_data = {}

        if "git" in env_default:
            env_data.setdefault("git", env_default["git"])
        if "git_hash" in env_default:
            env_data.setdefault("git_hash", env_default["git_hash"])

    path_to_env = Path(path_to_env).resolve()
    path_to_backup = Path("env.backup.yaml").resolve()

    if user_provided_env:
        shutil.copy(path_to_env, path_to_backup)

    try:
        path_to_env.write_text(yaml.safe_dump(env_data))
        yield
    finally:
        if user_provided_env:
            shutil.copy(path_to_backup, path_to_env)
            path_to_backup.unlink()
        else:
            path_to_env.unlink()


def build_image(
    e,
    cfg,
    env_name,
    until,
    entry_point,
    skip_tests,
    ignore_git,
    pkg_name,
    version,
    task,
):
    """Build Docker image

    Parameters
    ----------
    pkg_name : str
        Project name, used to tag the Docker image (e.g. {pkg_name}:{version})

    version : str
        Project version, user to tag the Docker image
        (e.g. {pkg_name}:{version})
    """

    e.cp("dist")

    e.cd(env_name)

    if task:
        suffix = "" if task == "default" else f"-{modify_wildcard(task)}"
        image_local = f"{pkg_name}{suffix}:{version}"

    args = ["docker", "build", ".", "--tag", image_local]

    # NOTE: this is used in Ploomber Cloud, but it isn't documented in
    # soopervisor's docs
    if "DOCKER_ARGS" in os.environ:
        args = args + shlex.split(os.environ["DOCKER_ARGS"])

    print(f"docker args: {args}")

    # how to allow passing --no-cache?
    e.run(*args, description="Building image")

    if not skip_tests:
        # test "ploomber status" in docker image
        e.run(
            "docker",
            "run",
            image_local,
            "ploomber",
            "status",
            "--entry-point",
            entry_point,
            description="Testing image",
            error_message="Error while testing your docker image with",
            hint=f'Use "docker run -it {image_local} /bin/bash" to '
            "start an interactive session to debug your image",
        )

        # check that the pipeline in the image has a configured File.client
        test_cmd = (
            "from ploomber.spec import DAGSpec; "
            f'print("File" in DAGSpec("{entry_point}")'
            ".to_dag().clients)"
        )

        e.run(
            "docker",
            "run",
            image_local,
            "python",
            "-c",
            test_cmd,
            description="Testing File client",
            error_message="Missing File client",
            hint=f'Run "docker run -it {image_local} /bin/bash" to '
            "to debug your image. Ensure a File client is configured",
            capture_output=True,
            expected_output="True\n",
            show_cmd=False,
        )

    if until == "build":
        raise CommanderStop('Done. Run "docker images" to see your image.')

    if cfg.repository:
        image_target = cfg.repository

        # Adding the latest tag if not a remote repo
        if ":" not in image_target:
            image_target = f"{image_target}{suffix}:{version}"

        e.run("docker", "tag", image_local, image_target, description="Tagging")
        e.run("docker", "push", image_target, description="Pushing image")
    else:
        image_target = image_local

    if until == "push":
        raise CommanderStop("Done. Image pushed to repository.")

    return image_target


def build(e, cfg, env_name, until, entry_point, skip_tests=False, ignore_git=False):
    """Build a docker image

    Parameters
    ----------
    e : Commander
        Commander instance

    cfg
        Configuration

    env_name : str
        Target environment name

    until : str
        Stop after certain starge

    entry_point : str
        Entry point to use path/to/pipeline.yaml

    skip_tests : bool, default=False
        Skip image testing (check dag loading and File.client configuration)
    """

    if not Path(env_name, "Dockerfile").is_file():
        raise MissingDockerfileError(env_name)

    # raise an error if the user didn't change the default value
    _validate_repository(cfg.repository)

    pkg_name, version = source.find_package_name_and_version()

    dependencies.check_lock_files_exist()
    dependency_files, lock_paths = get_dependencies()

    with prepare_env_file(entry_point):
        image_map = {}

        setup_flow = Path("setup.py").exists()

        # Generate source distribution
        if setup_flow:
            for task_pattern in sorted(dependency_files.keys()):

                if task_pattern != "default":
                    raise NotImplementedError(
                        "Multiple requirements.*.lock.txt or "
                        "environment.*.lock.yml files found along "
                        "with setup.py file. Please have either "
                        "of the two in the project root."
                    )
            # .egg-info may cause issues if MANIFEST.in was recently updated
            if Path("requirements.lock.txt").exists():
                e.cp("requirements.lock.txt")
            elif Path("environment.lock.yml").exists():
                e.cp("environment.lock.yml")

            e.rm("dist", "build", Path("src", pkg_name, f"{pkg_name}.egg-info"))
            e.run("python", "-m", "build", "--sdist", description="Packaging code")
            default_image_key = dependencies.get_default_image_key()

            image = build_image(
                e,
                cfg,
                env_name,
                until,
                entry_point,
                skip_tests,
                ignore_git,
                pkg_name,
                version,
                task=default_image_key,
            )

            image_map[default_image_key] = image
            # raise error if include is not None? and suggest to use MANIFEST.in
            # instead
        else:
            # sort keys so we iterate in deterministic order and can test easily
            for task in sorted(lock_paths.keys()):
                lock_file = lock_paths[task]

                if Path(lock_file).exists():
                    e.cp(lock_file)
                e.rm("dist")
                target = Path("dist", pkg_name)
                e.info("Packaging code")
                other_lock_files = [
                    file for file in list(lock_paths.values()) if file != lock_file
                ]
                exclude = cfg.exclude
                if cfg.exclude and other_lock_files:
                    exclude = cfg.exclude + other_lock_files
                elif not cfg.exclude and other_lock_files:
                    exclude = other_lock_files

                rename_files = {}
                if lock_file not in ("requirements.lock.txt", "environment.lock.yml"):
                    rename_files = (
                        {lock_file: "requirements.lock.txt"}
                        if "requirements" in lock_file
                        else {lock_file: "environment.lock.yml"}
                    )
                source.copy(
                    cmdr=e,
                    src=".",
                    dst=target,
                    include=cfg.include,
                    exclude=exclude,
                    ignore_git=ignore_git,
                    rename_files=rename_files,
                )
                source.compress_dir(e, target, Path("dist", f"{pkg_name}.tar.gz"))

                image = build_image(
                    e,
                    cfg,
                    env_name,
                    until,
                    entry_point,
                    skip_tests,
                    ignore_git,
                    pkg_name,
                    version,
                    task,
                )

                image_map[task] = image

                e.rm("dist")
                e.cd("..")

    if not setup_flow:
        # We need to go back to the env folder before return
        e.cd(env_name)

    return pkg_name, image_map
