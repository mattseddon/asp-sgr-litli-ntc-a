import nox

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True

project = nox.project.load_toml()
python_versions = nox.project.python_versions(project)
locations = "src", "tests"


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    session.install(".[tests]")
    session.run("pytest")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.install("-e", ".[dev]")

    args = *(session.posargs or ("--show-diff-on-failure",)), "--all-files"
    session.run("pre-commit", "run", *args)
