from setuptools import setup,find_packages

setup(
        name='vehicle_detection_lib',
        version='0.1',
        packages=find_packages(),
        install_requires=[
            'torch>=1.7.0',
            'opencv-python>=4.5.0',
            'ultralytics',

        ],
        description='A library for vehicle detection using yolo.',
        author='Wan Abdul Muiz',
        author_email='wwanabdulmuiz@gmail.com',

        classifier=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independant',
        ],

        Python_requires='>=3.6',
    )
