from setuptools import setup, find_packages


setup(
    name='toki-service',
    version='1.2.2',
    description='Toki service to manage CSV files and process invoices on top of them',
    long_description='''
    ''',
    author='Stanimir Simeonov',
    author_email='simeonov8809@gmail.com',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'toki = toki.app:main',
        ],
        'faust.codecs': [
            'avro_new_csv_file_event = toki.serialization_codecs.avro:avro_new_csv_file_event_codec',
            'avro_validated_event = toki.serialization_codecs.avro:avro_validated_event_codec',
        ],
    },
)
