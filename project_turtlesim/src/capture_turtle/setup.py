from setuptools import setup

package_name = 'capture_turtle'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pangea',
    maintainer_email='quadri.2@iitj.ac.in',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "turtle_controller=capture_turtle.turtle_controller:main",
            "turtle_spawner=capture_turtle.turtle_spawner:main"
        ],
    },
)
