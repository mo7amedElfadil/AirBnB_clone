"""models init
initializes the file storage by reloading the objects
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
