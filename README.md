# OME2 Validator

The OME2 Validator is a tool for running the OME2 validation procedures on a topographic dataset.

## Building the Docker image

The validator tool is a containerized application
that is built to run within a Docker container.
This container contains all the required dependencies,
which makes deployment of the tool easier.

The Docker image can be built by running the command below
from the root of this repository:

```sh
docker build -f Dockerfile . -t eurogeographics/ome2-validator:latest
```

If the image has been successfully built,
running the command should show the tool's help message:

```sh
docker run --rm -it eurogeographics/ome2-validator
```

## Published Docker images

The [Publish Docker image workflow](.github/workflows/publish-image.yml) builds the
existing Dockerfile and pushes the image to GitHub Container Registry (GHCR):

- A push to `main` publishes `ghcr.io/openmapsforeurope2/ome2-validator:latest`.
- A pushed Git tag starting with `v` publishes the same image name with that exact tag, for example
  `ghcr.io/openmapsforeurope2/ome2-validator:v26.11.16.0`.
  Tag pushes do not update `latest`.

The image name is derived from the GitHub repository, so it follows the repository's
owner and name if the project is moved or forked.

Release tags follow `vYY.MM.DD.N`, where `N` is a zero-based release counter for
that date (for example, `v26.11.16.0`, then `v26.11.16.1`).
This is calendar versioning, not Semantic Versioning. Do not reuse release tags.
The workflow runs for pushed tags starting with `v`; it does not enforce the full date-and-counter format.
Git tags must also be valid Docker image tags; the documented convention is valid.

For example, to publish a release from the current commit:

```sh
git tag v26.11.16.0
git push origin v26.11.16.0
```

Here, `origin` is the remote for the GitHub repository; use your GitHub remote's
name if it differs.

The workflow uses the built-in `GITHUB_TOKEN` with `contents: read` and
`packages: write` permissions; no additional registry secret is required.
Organization policies must allow Actions to publish packages.
After the first successful publish, check the package's visibility in GitHub:
new packages are private by default. Make it public if anonymous pulls are needed;
otherwise, authenticate to GHCR before pulling.

To pull and run a published release:

```sh
docker run --rm ghcr.io/openmapsforeurope2/ome2-validator:v26.11.16.0
```

## Running the validator

Once the Docker image has been built, the validator tool can be run with a command like the one below:

```sh
docker run --rm -it --add-host host.docker.internal:host-gateway -v "$(pwd):/pwd" eurogeographics/ome2-validator /pwd/validation_parameters.jsonc
```

This command consists of several parts:

1. `docker run` to create a container from a Docker image.
2. `--rm` to clean up and remove the container after the validator has run.
3. `-it` instructs the Docker client to run the container interactively and attach it to your terminal.
4. `--add-host host.docker.internal:host-gateway` to expose the host machine running Docker as `host.docker.internal` to the validator tool within the container.
   Note that within the container `127.0.0.1` *does not* refer to the host machine, but to the container itself.
5. `-v "$(pwd):/pwd"` to mount the current working directory as `/pwd` within the container.
6. The name of the Docker image: `eurogeographics/ome2-validator`.
7. The path to the file `/pwd/validation_parameters.jsonc` that contains the validation parameters for the validation run.
   These parameters indicate, e.g., the location of the input data,
   which validation checks to perform and where to store the results.
   *Note that this file **does not** come with the project by default.*

### Validation parameters

The project comes with a [`validation_parameters.example.jsonc`](validation_parameters.example.jsonc) example file
that can be used to create a `validation_parameters.jsonc` file.
This file can then be passed as an argument to the validator tool
in order to configure and perform a validation run.

The validation parameters file supports the use of environment variables for the following settings:

- `specification`
- `task_name`
- For `input_database` and `outut_database`:
  - `host`
  - `port`
  - `name`
  - `password`

To refer to an environment variable, the value in the parameters file must be of the form `${VARIABLE_NAME}`.
It must start with a dollar sign and opening brace,
followed by the name of the environment variable
and end with a closing brace.

An example snippet is shown below:

```jsonc
   // ...
   "input_database": {
      "host": "${DB_HOST}",
      "port" : "${DB_PORT}",
      "name": "${DB_NAME}",
      "username": "${DB_USER}",
      "password": "${DB_PASS}"
   },
    // ...
```

## Development

This project comes with a definition for a [dev container](https://containers.dev/) that is tailored for [Visual Studio Code](https://code.visualstudio.com/)
When you open the project's root folder,
Visual Studio Code will recognize the existence of a dev container definition
and will prompt whether it should load the project in a dev container.
The advantage of a dev container is that it provisions an environment with all the required software and dependencies installed.
The developer only needs to have Docker and Visual Studio Code on its machine.

### Dev container environment variables

[The dev container's compose file](./.devcontainer/docker-compose.yml) is configured
to load environment variables defined in [the `devcontainer.env` file](./.devcontainer/devcontainer.env).

*Please do not commit changes to the environment file.*
It is recommended to have `git` ignore changes to the file
via the `git update-index --skip-worktree` command
or to build the dev container at least once in Visual Studio Code,
which will mark the file with `--skip-worktree` as well.
