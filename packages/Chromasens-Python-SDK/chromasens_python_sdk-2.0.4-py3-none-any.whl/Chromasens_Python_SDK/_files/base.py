"""
This module contains base classes for the models.
"""
# Author: Robert Wenk / Chromasens GmbH
# Date: 28.10.2019


#--------  CHANGE LOG ------------------------------------------------------------
#   DD  22.09.2023
#       Improvment: 
#       Added the option to force the use of a specified file format for "_filename_helper"
#       If the first entry of the list is marked with a "*" e.g. ['*.txt'], than this filetype is forced, no matter what is specified by the user.



from abc import ABC, abstractmethod
from inspect import getmembers, isclass

import os
import importlib
import ctypes

import datetime

MAX_MSG_STRING = 300

# clean up modes
CLEANUP_STOP_BY_USER = 0
CLEANUP_CLOSE_PROGRAM = 1
CLEANUP_STOP_SEQUENCE_NOK = 2

#------------------------------------------------------------------------------
# Error Codes
#------------------------------------------------------------------------------
class ERROR_CODES():
    """
    Class for error codes.
    """

    # basic codes
    OK = (0, 'OK')
    NOK_EXCEPTION = (-300, '')
    NOK_STRUCT_SIZE = (-301, 'NOK: Struct size is different')
    NOK_FILETYPE_NOT_AVAILABLE = (-302, 'NOK: The defined filetype is not available. Please use ".csv" or ".xlsx" !')
    NOK_SAVE_PERMISSION_DENIED = (-303, 'NOK: Save was not sucessfull, permission denied. Chose another path !')
    NOK_FILETYPE_DICT= (-304, 'NOK: Filetype must be a dict() with one or multiple dataframes ')
    NOK_FILETYPE =  (-305, '')
    NOK_FIELPATH = (-306, 'NOK: Path is not existing !')
    NOK_FILENAME_EMPTY = (-307, 'NOK: The filename is empty' )
    
    
    
    def __init__(self):
        _tmp = getmembers(self)
        self._error_codes = dict()

        for i in _tmp:
            if isinstance(i, tuple) and (i[0].startswith('NOK') or i[0].startswith('OK')):
                self._error_codes[i[1][0]] = i[1][1]
        
    def get_msg(self, _key, _msg=''):
        actual_msg = self._error_codes.get(_key)
        if actual_msg is not None:
            return actual_msg + _msg
        return 'NOK: Undefined Error'
    
    def set_msg(self, _key, _msg):
        actual_msg = self._error_codes.get(_key)
        if actual_msg is not None:
            self._error_codes[_key] = _msg
            return
        raise ValueError("Key {} is not defined in class ERROR_CODES!".format(_key))

class BaseModel(ABC):
    """
    This class contains functions, which are used in the models.
    """
    
    dll = None
    _error_codes = ERROR_CODES()
    is_device = False
    __class_obj_numpy = getattr(importlib.import_module('numpy'), 'ndarray')

    @abstractmethod
    def __init__(self):
        """
        Constructor.
        """

    def _clean_up(self, mode: int=CLEANUP_STOP_SEQUENCE_NOK):
        """
        Function for cleanup tasks...
        
        Args:
            mode (int): Clean up mode

        Returns:
            type(None): None
        """

    def _is_device(self) -> bool:
        """
        _is_device(self)
        Returns if the instantiation is a device.

        Returns:
            bool: True or False
        """
        
        return self.is_device
    
    def _set_error_message(self, _errno: int, _msg: str):
        """
        _set_error_message(self, _errno, _msg)
        Set an error message.
        
        Args:
            _errno (int): Error number
            _msg (str): Error message

        Returns:
            type(None): None
        """
        
        self._error_codes.set_msg(_errno, _msg)
        
    def _retval_helper(self, _retval: int, _value: object = None, _err_msg: str = '') -> (int, object, str):
        """
        _retval_helper(self, _retval, _value, _err_msg)
        Helper, for return tasks.

        Args:
            _retval (int): return value
            _value (object): Object
            _err_msg (str): Error Message

        Returns:
            tuple (int, object, str): (0, Object, 'OK') or (Error Code, Object, 'Error Message')
        """
        
        # get error message
        error_msg = self._error_codes.get_msg(_retval, _err_msg)
        
        # check, if the numpy array is contiguous
        if isinstance(_value, self.__class_obj_numpy):
            if not _value.flags['C_CONTIGUOUS']:
                _value = _value.copy()
        
        if self.dll:
        
            # init
            func = self.dll.get_error_string
            func.restype = ctypes.c_int
            func.argtypes = [ctypes.c_int, ctypes.c_char_p]
            ptr = ctypes.c_char_p(bytes(MAX_MSG_STRING))
            
            # error is undefined on python side -> try on dll side
            if error_msg == 'NOK: Undefined Error':
                retval = func(_retval, ptr)
                if retval == self._error_codes.OK[0]:
                    error_msg = ptr.value.decode()

        return _retval, _value, error_msg
    
    def _get_pointer_value(self, ptr: ctypes.c_char_p, retval: int) -> (int, str, str):
        """
        Helper function, to check if the pointer is None and get the value.

        Args:
            ptr (ctypes.c_char_p): Pointer
            retval (int): Return value

        Returns:
            tuple (int, str, str): (0, Value, 'OK') or (Error Code, '', 'Error Message')
        """

        value = ''
        msg = ''

        if ptr.value is not None:
            try:
                # decode byte array
                value = ptr.value.decode()
            except UnicodeDecodeError as e:
                msg = str(e)
                retval = self._error_codes.NOK_EXCEPTION[0]
            
        return self._retval_helper(retval, value, msg)
    
    def _test_struct_size(self, _module: object) -> (int, type(None), str):
        """
        _test_struct_size(self)
        Test the size from the implemented python structs.
        
        Args:
            _module (object): Module, where the structs are defined

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        if not self.dll:
            raise ValueError("dll not loaded...")

        # init
        func = self.dll.get_struct_size
        func.restype = ctypes.c_int
        func.argtypes = [ctypes.c_char_p]
        ptr = ctypes.c_char_p()
        
        # loop over the implemented structs
        cnt = 0
        _structs = getmembers(_module, isclass)
        for _s in _structs:
            if 'ctypes' in str(_s[1]):
                continue
            if 'IGNORE_STRUCT_SIZE_TEST' in _s[1].__doc__:
                continue
            ptr.value = _s[0].encode('utf-8')
            size = ctypes.sizeof(_s[1]())
            retval = func(ptr)
            
            # check
            if retval != size:
                self._logger.error("Struct size of '{}' does not match!".format(_s[0]))
                self._logger.error("Python size: {}".format(size))
                self._logger.error("C size: {}".format(retval))
                cnt += 1

        if cnt != self._error_codes.OK[0]:
            return self._retval_helper(self._error_codes.NOK_STRUCT_SIZE[0], None)
        
        return self._retval_helper(self._error_codes.OK[0], None)



    def  _filename_helper (self, filename: str, file_extension_list: list, add_time_stamp: bool = False, add_file_counter: bool = False, generate_not_existing_path: bool = False, prefix: str = '', suffix: str = '') -> (int, str, str):
        """
        _filename_helper(self, filename, dict_dataframes, add_time_stamp)
        helper to check and generate filenames. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            filename (str): filename of the resultfile. End filename with the filetype. CSV and XLSX are supported (.csv / .xls or .xlsx)
            prefix (str): Prefix for the filename (if add_file_counter = True -> Filecounter is the first part of the name)
            suffix (str): Suffix for the filename (if add_time_stamp = True -> Timestamp is the last part of the name)
            file_extension_list (list): list with possible filetypes e.g. ['.bmp', '.png', '.tif']. If the first entry of the list is marked with a "*" e.g. ['*.txt'], than this filetype is forced, no matter what is specified by the user.
            add_time_stamp(bool): adds a timestamp to the filename
            add_file_counter(bool): adds a 4 digit counter prefix to the file. 
            generate_not_existing_path(bool): Generate the filepath if it does not exist already. 

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        if isinstance(filename, bytes):
            filename = filename.decode()
            
        if isinstance(prefix, bytes):
            prefix = prefix.decode()
            
        if isinstance(suffix, bytes):
            suffix = suffix.decode()
            
        if filename == '':
            return self._retval_helper(self._error_codes.NOK_FILENAME_EMPTY[0]) 
                        
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
              
        file_path, file_name_extension = os.path.split(filename)
        
        file_name, file_extension = os.path.splitext(file_name_extension)
        
        if file_name == '':
            return self._retval_helper(self._error_codes.NOK_FILENAME_EMPTY[0]) 
        
        # set the first entry of the file extension list as default extension
        if file_extension == '':
            file_extension = file_extension_list[0]
            
        #force to use specified file ending if specified with "*"
        if file_extension_list[0][0] == '*':
            file_extension = file_extension_list[0][1:]
            
        elif file_extension not in file_extension_list:
            msg = f'NOK: Filetype not correct. Valid filetypes are {file_extension_list} !'
            return self._retval_helper(self._error_codes.NOK_FILETYPE[0], '', msg) 

        if generate_not_existing_path:
            if not os.path.isdir(file_path):
                os.makedirs(file_path)
                
        if not os.path.isdir(file_path):
            return self._retval_helper(self._error_codes.NOK_FIELPATH[0], '') 
        
        if prefix != '':
            file_name = f'{prefix}_{file_name}'  
        
        if suffix != '':
            file_name = f'{file_name}_{suffix}'  
            
                
        if add_time_stamp:
            tmp = datetime.datetime.now()
            tmp = tmp.strftime('-%d-%m-%Y-%H-%M-%S-') + str(tmp).rpartition('.')[2][:2] # 0.01 s resolution
               
            file_name = f'{file_name}{tmp}'  
           
        if add_file_counter:
            counter_number_high  = -1
            for file in os.listdir(file_path):
                _, _file_name_extension = os.path.split(file)
                
                if len(_file_name_extension) < 4:
                    continue
                
                if not _file_name_extension[:4].isnumeric():
                    continue
                
                if counter_number_high < int(_file_name_extension[:4]):
                    counter_number_high = int(_file_name_extension[:4])
                      
            file_name = f'{counter_number_high+1:04d}_{file_name}' 
                            
        filename_out = os.path.join(file_path, file_name+file_extension)
        
        return self._retval_helper(self._error_codes.OK[0], (filename_out, file_path, file_name, file_extension))
        
        

    
    
    