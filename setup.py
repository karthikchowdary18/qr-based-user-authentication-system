from setuptools import find_packages, setup

package_name = 'user_authorization'

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
    maintainer='Karthik Chowdary Nunna',
    maintainer_email='kar8299s@hs-coburg.de',
    description='ROS 2 node for QR-based user authentication from camera input with topic-driven auth state publishing.',
    license='Proprietary',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'user_authorization = user_authorization.user_authorization:main',
        ],
    },
)
