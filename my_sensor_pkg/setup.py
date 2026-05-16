from setuptools import find_packages, setup

package_name = "my_sensor_pkg"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ajumal",
    maintainer_email="ajumal@todo.todo",
    description="My first ROS 2 sensor package",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "temperature_publisher = my_sensor_pkg.temperature_publisher:main",
            "temperature_subscriber = my_sensor_pkg.temperature_subscriber:main",
        ],
    },
)
