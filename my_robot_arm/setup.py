from setuptools import find_packages, setup
import os
from glob import glob

package_name = "my_robot_arm"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "urdf"),
            glob("urdf/*.urdf")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ajumal",
    maintainer_email="ajumal@todo.todo",
    description="My robotic arm package",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "arm_controller = my_robot_arm.arm_controller:main",
        ],
    },
)
