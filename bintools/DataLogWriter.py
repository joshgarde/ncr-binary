import struct
from . import FieldTypes

class DataLogWriter:
    def __init__(self, filename, fields):
        assert isinstance(filename, str)
        assert isinstance(fields, list)
        
        self.file = open(filename, 'xb')
        self.fields = fields
        self.__writeHeader()
        
    def __writeHeader(self):
        magic = bytes('NC🚀2019', 'utf-8')
        fieldsLength = struct.pack('B', len(self.fields))
        self.file.write(magic)
        self.file.write(fieldsLength)
        
        for i in range(0, len(self.fields)):
            field = self.fields[i]
            name = field['name']
            type = field['type']
            size = type.size()
            
            if size == -1:
                size = fields['size']
            
            encodedName = bytes(name, 'utf-8')
            meta = struct.pack('HBBB', i, type.value, size, len(encodedName))
            
            self.file.write(meta)
            self.file.write(encodedName)
            
        self.file.flush()