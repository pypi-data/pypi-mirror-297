from setuptools import find_packages, setup


def get_version() -> str:
    return "0.0.1"
    # Uncomment when ready to publish
    # version: Dict[str, str] = {}
    # with open(Path(__file__).parent / "dagster_sigma/version.py", encoding="utf8") as fp:
    #     exec(fp.read(), version)

    # return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = ""
setup(
    name="dagster_sigma",
    version=get_version(),
    author="Dagster Labs",
    author_email="hello@dagsterlabs.com",
    license="Apache-2.0",
    description="Build assets representing Sigma dashboards.",
    url=(
        "https://github.com/dagster-io/dagster/tree/master/python_modules/libraries/"
        "dagster-sigma"
    ),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["dagster_sigma_tests*"]),
    install_requires=[
        f"dagster{pin}",
        "sqlglot",
    ],
    include_package_data=True,
    python_requires=">=3.8,<3.13",
    zip_safe=False,
)
