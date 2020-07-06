from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("requirements-build.txt") as f:
    build_requirements = f.read().splitlines()

with open("runtime/requirements-deploy.txt") as f:
    deploy_requirements = f.read().splitlines()


setup(
    name='query_api',
    version='1.0.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        "dev": build_requirements + deploy_requirements,
    },
)
