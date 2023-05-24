# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER = r'C:\Users\USER\Desktop\employee_management\my-project\app\static\img'

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    UPLOAD_FOLDER = r'C:\Users\USER\Desktop\employee_management\my-project\app\static\img'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}