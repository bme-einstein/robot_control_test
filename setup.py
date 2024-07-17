from setuptools import find_packages, setup

package_name = 'pub_traj_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rafaelromaquela',
    maintainer_email='rafaelromaquela@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'Traj=pub_traj_py.2points:main',
            'C_Pose=pub_traj_py.Subscriber:main',
            'control_offset=pub_traj_py.pu_and_sub:main',
            'motion=pub_traj_py.motion_plannig:main',
        ],
    },
)
