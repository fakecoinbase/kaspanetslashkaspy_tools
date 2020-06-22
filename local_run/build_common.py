import os
import subprocess


def build_image(*, service_name, build_dir, extra_parameter=None, commit_number, context_dir):
    cmd_args = []
    cmd_args.extend(['docker', 'build', '-f', 'Dockerfile'])
    if extra_parameter is not None:
        cmd_args.extend(['--build-arg', extra_parameter])
    cmd_args.extend(['-t', service_name + ':' + commit_number])
    cmd_args.extend([context_dir])
    completed_process = subprocess.run(args=cmd_args, capture_output=True, cwd=build_dir)
    completed_process.check_returncode()


def get_git_commit(repo_dir, branch):
    """
    Get the commit id of HEAD  (just first 12 characters)
    :return: a string with the commit id
    """
    completed_process = subprocess.run(args=['git', 'checkout', branch], capture_output=True,
                                       cwd=repo_dir)
    completed_process.check_returncode()
    completed_process = subprocess.run(args=['git', 'pull'], capture_output=True, cwd=repo_dir)
    completed_process.check_returncode()
    completed_process = subprocess.run(args=['git', 'rev-parse', '--short=12', 'HEAD'], capture_output=True,
                                       cwd=repo_dir)
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    git_commit = completed_process.stdout
    return git_commit.decode('utf-8')[:-1]  # remove \n from the end


def tag_service(service_name, commit_number):
    cmd_args = []
    cmd_args.extend(['docker', 'tag'])
    cmd_args.extend([service_name + ':' + commit_number])
    cmd_args.extend([service_name + ':' + 'latest'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    completed_process.check_returncode()


def remove_all_images_and_containers():
    """
    Remove all containers and all images from your computer!!!
    Use carefully.
    :return: None
    """
    remove_all_containers()
    remove_all_images()


def remove_all_images():
    cmd_args = []
    cmd_args.extend(['docker', 'system', 'prune', '-f', '-a'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


def remove_all_containers():
    """
    Removes all containers.
    :return: None
    """
    containers = get_all_containers()
    if not containers:
        return
    cmd_args = []
    cmd_args.extend(['docker', 'rm', '-f'])
    cmd_args.extend(containers)
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


def get_all_containers():
    """
    Finds all container (both stopped and running)
    :return: All container ids as a list
    """
    cmd_args = []
    cmd_args.extend(['docker', 'ps', '-a', '-q'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    containers = completed_process.stdout.split()
    return containers
