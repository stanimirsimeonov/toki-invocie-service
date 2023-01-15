SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True,
    'REQUIRED_SETTINGS': ('KAFKA_BOOTSTRAP_SERVER',),
}

# The following variables can be ovirriden from ENV
WORKER = "toki"
WORKER_PORT = 6066
KAFKA_BOOTSTRAP_SERVER = "kafka://localhost:29092"
KAFKA_BOOSTRAP_SERVER_NAME = "kafka"
KAFKA_BOOSTRAP_SERVER_PORT = 29092
SCHEMA_REGISTRY_URL = "http://localhost:8081"
SCHEMA_REGISTRY_SERVER = "localhost"
SCHEMA_REGISTRY_SERVER_PORT = 8081

VAR_DYNAMODB_TABLE_UPLOADED_FILES = {
    'TableName': 'uploaded_files',
    'KeySchema': [
        {'AttributeName': 'bucket', 'KeyType': 'HASH'},
        {'AttributeName': 'filename', 'KeyType': 'RANGE'},
    ],
    'LocalSecondaryIndexes': [
        {
            'IndexName': "IndexCreatingRange",
            'KeySchema': [
                {'AttributeName': 'bucket', 'KeyType': 'HASH'},
                {'AttributeName': 'created_at', 'KeyType': 'RANGE'},
            ],
            'Projection': {
                'ProjectionType': "ALL"
            }
        }
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'bucket', 'AttributeType': 'S'},
        {'AttributeName': 'filename', 'AttributeType': 'S'},
        {'AttributeName': 'created_at', 'AttributeType': 'S'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
}

VAR_DYNAMODB_TABLE_CONSUMPTION_RATES = {
    'TableName': 'consumption_rates',
    'KeySchema': [
        {'AttributeName': 'asDate', 'KeyType': 'HASH'},
        {'AttributeName': 'asTime', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'asDate', 'AttributeType': 'S'},
        {'AttributeName': 'asTime', 'AttributeType': 'S'},
        {'AttributeName': 'asTimestamp', 'AttributeType': 'N'},
        {'AttributeName': 'rate', 'AttributeType': 'N'},
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': "IndexTimestampRange",
            'KeySchema': [
                {'AttributeName': 'asTimestamp', 'KeyType': 'HASH'},
                {'AttributeName': 'rate', 'KeyType': 'RANGE'},
            ],
            'Projection': {
                'ProjectionType': "ALL"
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 100,
                'WriteCapacityUnits': 100
            }
        },
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'toki': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
