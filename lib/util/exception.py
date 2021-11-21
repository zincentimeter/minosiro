class MetaException(Exception):

    def __init__(self, instance):
        self.error_instance = instance
        self.message = 'This is an uncategorized error.'
    
    def __init__(self, message : str):
        self.message = message

    def __str__(self):
        return self.message