import setuptools 
### Create a setup.py file to define metadata and dependencies. Use setuptools to package your code into a distributable format, such as a Python Egg or Wheel.###
setuptools.setup ( 
    name='prophet_table', 
    version='1.0', 
    description="FIS Prophet File Inspector and Processor",
    author='Kin Tsang', 
    author_email='kinming0807oppo@gmail.com', 
    long_description= "This is a python library to facilitate the processing of model points used for actuarial software Prophet, produced by FIS. \n It utilizes the power of the Pandas library so you can easily parse, process and filter the model points.",
    url="https://github.com/bensonby/mpfi",
    packages= setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        "pandas>=2.0.1",
    ],
    
    python_requires='>=3.9.7',
)

