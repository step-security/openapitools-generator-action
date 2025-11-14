from subprocess import call
from sys import argv
from os import getenv, getuid

(_, generator, docker_repository, docker_image, generator_tag, sha, openapi_file, openapi_url, config_file, template_dir, *args) = argv

# Always use SHA for pinned image
docker_image_ref = f"{docker_repository}/{docker_image}@sha256:{sha}"

cmd = [
    "docker", "run",
    "-u", f"{getuid()}:1001",
    "--rm",
    "--workdir", "/github/workspace",
    "-v", f"{getenv('GITHUB_WORKSPACE')}:/github/workspace",
    docker_image_ref,
    "generate",
    "-g", generator,
    "-o", f"/github/workspace/{generator}-client"
]

if openapi_url == "UNSET":
    if not openapi_file.startswith("/"):
        openapi_file = f"/github/workspace/{openapi_file}"
    cmd.extend(["-i", openapi_file])
else:
    cmd.extend(["-i", openapi_url])

if config_file != "UNSET":
    if not config_file.startswith("/"):
        config_file = f"/github/workspace/{config_file}"
    cmd.extend(["-c", config_file])

if template_dir != "UNSET":
    if not template_dir.startswith("/"):
        template_dir = f"/github/workspace/{template_dir}"
    cmd.extend(["-t", template_dir])

if args:
    cmd.extend(args)

# Call the command and return the exit code
exit(call(cmd))
