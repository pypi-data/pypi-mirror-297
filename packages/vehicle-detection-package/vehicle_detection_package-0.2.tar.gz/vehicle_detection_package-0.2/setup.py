from setuptools import setup, find_packages

setup(
    name='vehicle_detection_package',
    version='0.2',
    description='A package for vehicle detection and tracking using YOLOv8 and SORT',
    author='muiz',
    author_email='wwanabdulmuiz@gmail.com',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'ultralytics',
        'sort',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

