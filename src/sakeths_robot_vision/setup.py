from setuptools import find_packages, setup

package_name = 'sakeths_robot_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test'], include=['modules_to_import']), # "include" MUST contain this folder if custom modules want to be imported.  
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dev-machine',
    maintainer_email='sakethsarma07@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'image_subscriber = sakeths_robot_vision.node:main'
        ],
    },
)
