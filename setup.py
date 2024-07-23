from setuptools import find_packages, setup

package_name = 'robot_control_test'

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
            'Traj=robot_control_test.2points:main',
            'C_Pose=robot_control_test.Subscriber:main',
            'control_offset=robot_control_test.pu_and_sub:main',
            'motion=robot_control_test.motion_plannig:main',
            'joint_controller=robot_control_test.test_joint_traj:main',
        ],
    },
)
