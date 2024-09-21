"""
Module for the CSI.dll implementation via ctypes.
"""
# Author: Daniel Dürhammer, Robert Wenk / Chromasens GmbH
# Date: 16.05.2024


#--------  CHANGE LOG ------------------------------------------------------------
#   DD  06.09.2023
#       Bugfix:
#       The behaviour of the .csi file changed again. The "scan_image_stack"
#       function failed when a error occurs if the stack is incomplete. 
#       With "ignore_dll_errors = TRUE" (function input variable) the functions
#       returns OK also for incomplete stacks.
#
#   DD  08.09.2023
#       Add function:
#       wait_until_reconnect_possible - Loops until the camera with the specified
#       device number is available. This function can be used to search for a 
#       camera after a restart. 
#   RW  08.09.2023
#       Improvement:
#       Support for RGBa10 bit + RGBa12 bit images.
#   OC  15.03.2024
#       Improvement:
#       added output of reconnect time to wait_until_reconnect_possible function
#
# ------------------REIMPLEMENTATION---------------------------------------
#
#   DD  22.05.2024
#       Reimplementation (of the parent class):
#       Reimplementation of the GenIcam class. The files are in a own GenIcam folder now.
#       The class "GenICam" can be used for not streamable GenIcam devices. (e.g. XLCX)
#       The class "GeniGenICamStreamable" can be used for streamable GenIcam cameras.
#       (e.g. allPIXA neo, evo, ...)
#       The files that comes with the Chromasens GenIcam SDK are used now. No additional
#       custom CATE files are needed anymore. -> Installing GCT is mandatory to use these 
#       classes. 
#       The mechanism of image acquisition is completely reimplemented. The native 
#       acquisition procudure is used to acquire images as intended by the API. 
#       Images can be grabed in a continious stream now. Singe image acquisition is
#       supported still as before.  
#       The method names now correspond to the naming convention.
#
#   DD  20.07.2024
#       New function
#       Added "get_register" and "set_register
#
#   DD  20.07.2024
#       Bugfix
#       Bugfix in the "discover_devices" method.
#
#   DD  13.09.2024
#       Bugfix
#       Activate filter driver for S2I TL
#
#   DD  13.09.2024
#       Improvement
#       The API return structures are automatically converted into dicts now.
#
#   DD  13.09.2024
#       Bugfix
#       Return an error for reading out not readable features (avoids a crash)


import ctypes
import os
import numpy as np
import cv2
import platform
import re
from time import time, sleep

from typing import Union

# model
import Chromasens_Python_SDK._files.base as _base
from Chromasens_Python_SDK._files.genicam import genicam_ds as _ds

#------------------------------------------------------------------------------
# Error Codes
#------------------------------------------------------------------------------
class ERROR_CODES(_base.ERROR_CODES):
    """
    Error Codes for the genicam module.

    Note:
        Please add any new Error Code in this class.\n
        The error message of errors with no text, e.g. NOK_EXCEPTION, can be set
        with the function _set_error_message(...). With the function
        _retval_helper(...) an error message can be appended to an existing message.
    """

    NOK_NO_DLL = (-1, 'NOK: Cannot find CSI.dll !')
    NOK_FEATURE_NOT_AVAILABLE = (-2, 'NOK: Feature ')
    NOK_IMAGE_FORMAT = (-3, 'NOK: Image format not supported')
    NOK_FEATURE_PATH_NAME_AND_VALUE = (-4, 'NOK: Feature name:value format is not valid')
    NOK_FORMAT_HEX_VALUE = (-5, 'NOK: Please use "0x" at the beginning !')
    NOK_CSI_MODULE_NOT_AVAILABLE = (-6, f'NOK: Module is not available. Select "{_ds.CSI_MODULE_LIST}"')
    NOK_NO_DEVICE_FOUND = (-7, 'NOK: No Device found. Check the physical connection of the interface')
    NOK_CAMERA_IS_NOT_OPEN = (-8, 'NOK: Camera is not open')
    NOK_FILE_NOT_AVAILABLE = (-9, 'NOK: File is not available !')
    NOK_INVALID_DEVICE_NUMBER = (-10, 'NOK: Invalid device number !')
    NOK_CAMERA_IS_OPEN = (-11, 'NOK: Camera is open')
    NOK_FEATURE_IS_READ_ONLY = (-12, 'NOK: Feature ')
    NOK_PARAMETER_TEMPORARY_NOT_AVAILABLE = (-13,'')
    NOK_IMAGE_NUMBER_OUT_OF_RANGE = (-14, 'NOK: Image number is out of range!')
    NOK_TIMEOUT_WAIT_FEATURE = (-15, 'NOK: Timeout while wait for feature execution')
    NOK_IMG_IN_STACK = (-16, 'Not every image in the image stack is a valid image')
    NOK_NUM_IMG_IN_STACK = (-17, 'The number of valid images in the image stack does not match the expected number')
    NOK_NO_IMAGE_IN_STACK = (-18, 'The image stack does not contain a valid image')
    NOK_VALUE_OUT_OF_RANGE = (-19, '')
    NOK_TIMEOUT_WAIT_RECONNECT = (-20, 'NOK: Timeout while wait for reconnect')
    NOK_STREAM_ALREADY_ACTIVE = (-21, 'NOK: The camera stream is already active!')
    NOK_DLL_ERROR = (-22, '')
    NOK_FILE_TYPE_VALID = (-23, 'NOK: The filetype is not valid for the camera')
    NOK_FILE_TYPE_MATCH = (-24, '')
    NOK_PACKAGE_CONSITENCY = (-25, 'NOK: No package consitency, package update failed !')
    NOK_BUFFER_OVERFLOW = (-26, '')
    NOK_MAX_FEATURE_LEN = (-27, '')
    NOK_FEATURE_VALUE = (-28, '')
    NOK_FEATURE_TYPE = (-29, '')
    NOK_TIMEOUT_COMMAND_EXECUTION = (-30, '')
    NOK_DEVICE_ALREADY_OPENED = (-31, 'NOK: The device is already opened, close other GenICam applications !')
    NOK_FEATURE_IS_NOT_READABLE = (-32, '')
    NOK_ENUM_NOT_VALID = (-33, '')
    NOK_ENVIORNMENT_PATH_NOT_AVAILABLE = (-34, 'NOK: The enviornment valiable "GENICAM_GENTL64_PATH" is not available. Install a camera SDK !')
    NOK_MODULE_HANDLE = (-35, 'NOK: The module handle is not available. ')
    NOK_FEATURE_TYPE_IS_NOT_READABLE = (-36, '')

class GenICamBase(_base.BaseModel):
    '''
    This class is intended to represent GenIcam devices which don't have the property "streamable" (Light Controllers / Sensors / ....)
    '''
        
    open_timeout = 1000
    discovery_timeout = 1000

    def __init__(self, dll_dir_path: str = r'C:\Program Files\Chromasens\GCT2\bin'):
        """
        __init__(self, dll_dir_path = r'C:\Program Files\Chromasens\GCT2\bin')
        Create an instance of a GenIcam device.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            dll_dir_path (str, optional): The path to the folder that contains the CSI file. 
            The CSI file represents the Chromasens SDK and provides functions to setup the 
            camera and grab images. For default installation the default parameter value can
            be used. 

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        #
        self.is_device = True

        super().__init__()
        self._error_codes = ERROR_CODES()
        self.device_handle = 0
        self.device_number = None
        self.transportLayerID = None
        self.dll = None
        self.feature_dict = dict()
        self.feature_not_valid = list()
        
        self.API_version = dict()

        platform_name = platform.uname()[0]
        if platform_name == "Windows":
            lib_name = "CSI.dll"
        elif platform_name == "Linux":
            lib_name = "libCSI.so"
        else:
            lib_name = "CSI"
            
        if not os.path.isfile(os.path.join(dll_dir_path, lib_name)):
            return self._retval_helper(self._error_codes.NOK_NO_DLL[0])
        
        if dll_dir_path not in os.environ['PATH']:
            os.environ['PATH'] = dll_dir_path + os.pathsep + os.environ['PATH']
            
        try:
            self.dll = ctypes.cdll.LoadLibrary(os.path.join(dll_dir_path, lib_name))
        except OSError:
            print(self._error_codes.NOK_NO_DLL[1])
            pass

        
        function = self.dll.csiInit
        function.argtypes = [ctypes.c_uint64]
        _ = function(_ds.CSI_LOGLEVEL_NONE, None, None)
        
        major = ctypes.c_uint32()
        minor = ctypes.c_uint32()
        patch = ctypes.c_uint32()
        revision = ctypes.c_uint32()
    
        function = self.dll.csiGetLibraryVersion
        _ = function(ctypes.byref(major), ctypes.byref(minor), ctypes.byref(patch), ctypes.byref(revision))
        
        self.API_version['major'] = major.value
        self.API_version['minor'] = minor.value
        self.API_version['patch'] = patch.value
        self.API_version['revision'] = revision.value
        
    
    def __del__(self):
        
        if self.device_handle != 0:
            self.close_connection()
            
        self.dll.csiClose()
            
        
        
    def __str__(self):
        
        if not self.device_handle:
            return f'Instance of {self.__class__.__name__} class'
        
        else:
            
            info_param_name_list = ['DeviceVendorName', 'DeviceModelName', 'DeviceSerialNumber']

            info_list = list()
            
            for info_param_name in info_param_name_list:
                
                retval = self.get_feature(info_param_name)
                if retval[0] != self._error_codes.OK[0]:
                    return f'Instance of {self.__class__.__name__} class'
                
                info_list.append(retval[1])
                
            if len(info_list) == 0:
                return f'Instance of {self.__class__.__name__} class'
            else:
                return ' | '.join(info_list)

            
      
    def open_connection(self, tl_producer_file_name: Union[str, list, type(None)] = None, device_number: int = 1) -> (int, type(None), str):
        """
        open_connection(self, tl_producer_file_name, device_number)
        Opens the connection to the GenIcam device via the transport layer. 
        The transport layer file (.cti) is provided by Chromasens in case 
        of a system without a framegrabber.
        
        S2I     - r'C:\Program Files\Chromasens\GCT2\GenTL\s2i\GEVTLS2I.cti'
        Kithara - r'C:\Program Files\Chromasens\GCT2\GenTL\Kithara\tkh_tl_gev_kithara.cti'
        
        For systems with a framegrabber the .cti file is provided by the framegrabber
        manufacturer. The following is an example of an Euresys CXP12 grabber.
        
        Euresys CXP12 - r'C:\Program Files\Euresys\eGrabber\cti\x86_64\coaxlink.cti'
        

        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            tl_producer_file_name (Union(str, list, type(None)), optional): Path to the transport layer producer file (.cti) 
                                                                            or a list with multiple paths to producer files. 
                                                                            If not specified the system enviornment path list
                                                                            GENICAM_GENTL64_PATH is used.
            device_number (int): Device number. For multiple devices for the same TL the device number must be incremented.
                                 Count starts at 1.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check dll
        if self.dll is None:
            return (self._error_codes.NOK_NO_DLL[0], None, self._error_codes.NOK_NO_DLL[1])

        if self.device_handle != 0:
            return self._retval_helper(self._error_codes.NOK_CAMERA_IS_OPEN[0])
        
        retval = self.discover_devices(tl_producer_file_name)
        if retval[0] != self._error_codes.OK[0]:
            return self._retval_helper(retval[0])

        device_info_dict_list = retval[1]
        
        if len(device_info_dict_list) == 0:
            return self._retval_helper(self._error_codes.NOK_NO_DEVICE_FOUND[0])

        if device_number > len(device_info_dict_list):
            return self._retval_helper(self._error_codes.NOK_INVALID_DEVICE_NUMBER[0])
        
        device_info_dict = device_info_dict_list[device_number-1]
        
        if device_info_dict['accessStatus'] != _ds.CSI_DEV_ACCESS_STATUS_READWRITE:
            return self._retval_helper(self._error_codes.NOK_DEVICE_ALREADY_OPENED[0])
        
        device_handle = _ds.csiHandle(0)
        
        function = self.dll.csiOpenDevice
        function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(_ds.csiHandle), ctypes.c_int64, ctypes.c_int64] 
        retval = function(device_info_dict['deviceIdentifier'], device_info_dict['interfaceID'],
                          ctypes.byref(device_handle), self.open_timeout, _ds.CSI_DEV_MODE_EXCLUSIVE)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
                
        self.device_handle = device_handle
        self.device_number = device_number
        self.transportLayerID = device_info_dict['tlProducerInfos']['transportLayerID'].decode()
        

        return self._retval_helper(self._error_codes.OK[0])
    
    
    
    def close_connection(self) -> (int, type(None), str):
        """
        close_connection(self)
        Closes the camera connection. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        #apply a sleep before the camera is closed. 
        #If a function is calleddirectly before a parameter is set this can cause a crash otherwise
        #The reason for this behaviour is unknown.
        sleep(2)
        
        # function call
        retval = self.dll.csiCloseDevice(self.device_handle)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        # reset
        self.device_handle = 0
        self.device_number = None

        return self._retval_helper(self._error_codes.OK[0])
    
        
    
    def set_feature(self, feature_name: str, feature_value: Union[bool, int, float, str, bytes], module: int = _ds.CSI_DEVICE_MODULE) -> (int, type(None), str):
        """
        set_feature(self, feature_name, feature_value, module)
        Sets a Genicam feature of the system. To set a camera feature the value
        of the parameter module must be _ds.CSI_DEVICE_MODULE.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            feature_name (str): Feature name
            feature_value (Union[bool, int, float, str, bytes]): Feature value
            module (int, optional): Supported Values = [CSI_TRANSPORTLAYER_MODULE, CSI_INTERFACE_MODULE, CSI_DEVICE_MODULE, CSI_LOCAL_DEVICE_MODULE, CSI_STREAM_MODULE, CSI_BUFFER_MODULE]
        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval

        retval = self.get_feature_parameter(feature_name, module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        feature_param_dict = retval[1]
        
        # check, if feature is available
        if feature_param_dict['type'] == _ds.CSI_UNKNOWN_TYPE:
            return self._retval_helper(self._error_codes.NOK_FEATURE_NOT_AVAILABLE[0], None, "'{}' is not available !".format(feature_name))
        
        # check if we have a feature with write access
        if feature_param_dict['access'] <= _ds.CSI_ACCESS_READ_ONLY:
            if feature_param_dict['type'] == _ds.CSI_ENUMERATION_TYPE and feature_param_dict['enumCounter'] == 1:
                return self._retval_helper(self._error_codes.OK[0])
            else:
                return self._retval_helper(self._error_codes.NOK_FEATURE_IS_READ_ONLY[0], None, "'{}' is read only !".format(feature_name))

        name = ctypes.c_char_p(feature_name.encode())
        
        #convert bytes to string
        if isinstance(feature_value, bytes):
            feature_value = feature_value.decode()
            
            
        retval = self._handle_helper(module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        handle = retval[1]
        
        #handle the different filetypes. In this python implementation the feature 
        #value is always a str variable. In the API there are different functions 
        #for different variable types. 
        if feature_param_dict['type'] in [_ds.CSI_BOOLEAN_TYPE]:
            
            if isinstance(feature_value, str):
                if feature_value not in ['0', '1', 'True', 'False']:
                    msg = f"NOK: For the GenIcam parameter '{feature_name}', the feature value must represent a bool. Possible: {['0', '1', 'True', 'False']} | Actual: {feature_value}" 
                    self._set_error_message(self._error_codes.NOK_FEATURE_VALUE[0], msg)
                    return self._retval_helper(self._error_codes.NOK_FEATURE_VALUE[0])
                
                #convert the value into a bool
                value = feature_value in ['True', '1']  

            else:
                value = bool(feature_value)
                
                
            function = self.dll.csiSetFeatureBool
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_bool, ctypes.c_int64]
            
            
        elif feature_param_dict['type'] in [_ds.CSI_INT_TYPE]:
            
            if isinstance(feature_value, str):
                if feature_value[0] in ('-', '+'):
                    check_int = feature_value[1:].isdigit()
                check_int =  feature_value.isdigit()
            
                if not check_int:
                    msg = f"NOK: For the GenIcam parameter '{feature_name}', the feature value must be a string that represents a int. e.g. '0', '1', '-2', '+3'" 
                    self._set_error_message(self._error_codes.NOK_FEATURE_TYPE[0], msg)
                    return self._retval_helper(self._error_codes.NOK_FEATURE_TYPE[0])
                
            value = int(feature_value)
                
            _min = feature_param_dict['minimumInt']
            _max = feature_param_dict['maximumInt']
            
            if not _min <= value <= _max:
                msg = f"NOK: For the GenIcam parameter '{feature_name}', the value must be: {_min} < feature_value < {_max}. | Actual: {int(feature_value)}" 
                self._set_error_message(self._error_codes.NOK_FEATURE_VALUE[0], msg)
                return self._retval_helper(self._error_codes.NOK_FEATURE_VALUE[0])
                
            function = self.dll.csiSetFeatureInt
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int64]


        elif feature_param_dict['type'] in [_ds.CSI_FLOAT_TYPE]:
            
            if isinstance(feature_value, str):
                if not feature_value.replace('.','',1).isdigit():
                    msg = f"NOK: For the GenIcam parameter '{feature_name}', the feature value must be a string that represents a float. e.g. '0', '1.7', '-2.1'" 
                    self._set_error_message(self._error_codes.NOK_FEATURE_TYPE[0], msg)
                    return self._retval_helper(self._error_codes.NOK_FEATURE_TYPE[0])
                
            value = float(feature_value)
            
            _min = feature_param_dict['minimumFlt']
            _max = feature_param_dict['maximumFlt']
            
            if not _min <= value <= _max:
                msg = f"NOK: For the GenIcam parameter '{feature_name}', the value must be: {_min} < feature_value < {_max}. | Actual: {float(feature_value)}" 
                self._set_error_message(self._error_codes.NOK_FEATURE_VALUE[0], msg)
                return self._retval_helper(self._error_codes.NOK_FEATURE_VALUE[0])
            
            value = ctypes.c_double(value)

            function = self.dll.csiSetFeatureFloat
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_double, ctypes.c_int64]
            


        elif feature_param_dict['type'] in [_ds.CSI_STRING_TYPE]:
            
            if not isinstance(feature_value, str):
                feature_value = str(feature_value)
            
            if (len(feature_value) > feature_param_dict['maximumStringLength']) and (feature_param_dict['type'] == _ds.CSI_STRING_TYPE):
                msg = f"NOK: The max. feature name len is: {feature_param_dict['maximumStringLength']} | Actual feature name len: {len(feature_value)}" 
                self._set_error_message(self._error_codes.NOK_MAX_FEATURE_LEN[0], msg)
                return self._retval_helper(self._error_codes.NOK_MAX_FEATURE_LEN[0])
            
            function = self.dll.csiSetFeatureString
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int64]
            value = ctypes.c_char_p(feature_value.encode())
            
            
        elif feature_param_dict['type'] in [_ds.CSI_ENUMERATION_TYPE]: 
            
            
            retval = self.get_feature_enum_list(feature_name, module)
            if retval[0] != self._error_codes.OK[0]:
                return retval
            
            enum_list = retval[1]
            
            if feature_value not in enum_list:
                msg = f"NOK: The feature enumeration {feature_name} doesn't contain: '{feature_value}' | Valid values: {enum_list}" 
                self._set_error_message(self._error_codes.NOK_ENUM_NOT_VALID[0], msg)
                return self._retval_helper(self._error_codes.NOK_ENUM_NOT_VALID[0]) 
            

            if not isinstance(feature_value, str):
                feature_value = str(feature_value)
            
            if (len(feature_value) > feature_param_dict['maximumStringLength']) and (feature_param_dict['type'] == _ds.CSI_STRING_TYPE):
                msg = f"NOK: The max. feature name len is: {feature_param_dict['maximumStringLength']} | Actual feature name len: {len(feature_value)}" 
                self._set_error_message(self._error_codes.NOK_MAX_FEATURE_LEN[0], msg)
                return self._retval_helper(self._error_codes.NOK_MAX_FEATURE_LEN[0])
            
            
            function = self.dll.csiSetFeatureEnum
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int64]
            value = ctypes.c_char_p(feature_value.encode())

            
        elif feature_param_dict['type'] in [_ds.CSI_REGISTER]: 
            
            if not isinstance(feature_value, str):
                feature_value = str(feature_value)
            
            function = self.dll.csiSetFeatureReg
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int64]
            value = ctypes.c_char_p(feature_value.encode())
            
            size = feature_param_dict['featureRegLength']
            
            #execute the function         
            retval = function(handle, name, value, size, module)
            if retval != self._error_codes.OK[0]:
                return self._error_description_helper(retval)


        elif feature_param_dict['type'] in [_ds.CSI_COMMAND]:
            
            function = self.dll.csiExecuteCommand
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int64]

            #execute the function (no "value" argument for csiExecuteCommand)    
            retval = function(handle, name, module)
            if retval != self._error_codes.OK[0]:
                return self._error_description_helper(retval)
            
            #check if the command is finiched 
            function = self.dll.csiIsCommandActive
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_int64]
            
            is_active = ctypes.c_bool(True)
            
            timeout_s = 20
            t0 = time()
            while is_active:
                retval = function(handle, name, ctypes.byref(is_active), module)
                
                if time()-t0 > timeout_s:
                    msg = f"NOK: timeout for the command feature '{feature_name}' no execution after {timeout_s} s" 
                    self._set_error_message(self._error_codes.NOK_TIMEOUT_COMMAND_EXECUTION[0], msg)
                    return self._retval_helper(self._error_codes.NOK_TIMEOUT_COMMAND_EXECUTION[0])

            return self._retval_helper(self._error_codes.OK[0])
            
        
        else:
            print(f"ERROR: {feature_param_dict['type']=}")
            
        #execute the function   
        retval = function(handle, name, value, module)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0])
    
    
    def get_feature(self, feature_name: str, module: int = _ds.CSI_DEVICE_MODULE) -> (int, Union[bool, int, float, str], str):
        """
        get_feature(self, feature_name, module)
        Readout a Genicam feature of the system. To get a camera feature the value
        of the parameter module must be _ds.CSI_DEVICE_MODULE.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            feature_name (str): Feature name
            module (int, optional): Supported Values = [CSI_TRANSPORTLAYER_MODULE, CSI_INTERFACE_MODULE, CSI_DEVICE_MODULE, CSI_LOCAL_DEVICE_MODULE, CSI_STREAM_MODULE, CSI_BUFFER_MODULE]

        Returns:
            tuple (int, Union[bool, int, float, str], str): (0, Value, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        if module not in _ds.CSI_MODULE_LIST:
            return self._retval_helper(self._error_codes.NOK_CSI_MODULE_NOT_AVAILABLE[0])

        retval = self.get_feature_parameter(feature_name, module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        feature_param_dict = retval[1]
        
        # check, if feature is available
        if feature_param_dict['type'] == _ds.CSI_UNKNOWN_TYPE:
            return self._retval_helper(self._error_codes.NOK_FEATURE_NOT_AVAILABLE[0], None, "'{}' is not available !".format(feature_name))
        
        # check if we have a feature with read access
        if feature_param_dict['access'] not in [_ds.CSI_ACCESS_READ_ONLY, _ds.CSI_ACCESS_READ_WRITE]:
            return self._retval_helper(self._error_codes.NOK_FEATURE_IS_NOT_READABLE[0], None, f"NOK: Feature: '{feature_name}' is not readable !")


        #handle the different filetypes.
        if feature_param_dict['type'] in [_ds.CSI_BOOLEAN_TYPE]:
            param_value_out = bool(feature_param_dict['valueInt'])
            
        elif feature_param_dict['type'] in [_ds.CSI_INT_TYPE]:
            param_value_out = feature_param_dict['valueInt']

        elif feature_param_dict['type'] in [_ds.CSI_FLOAT_TYPE]:
            param_value_out = feature_param_dict['valueFlt']

        elif feature_param_dict['type'] in [_ds.CSI_STRING_TYPE, _ds.CSI_ENUMERATION_TYPE]:
            param_value_out = feature_param_dict['valueStr'].decode()
            
        elif feature_param_dict['type'] in [_ds.CSI_COMMAND]: 
            return self._retval_helper(self._error_codes.NOK_FEATURE_TYPE_IS_NOT_READABLE[0], None, f"NOK: Feature: '{feature_name}' is type 'COMMAND' and therefore not readable !")
            
        elif feature_param_dict['type'] in [_ds.CSI_REGISTER]: 
            print('CSI_REGISTER access not implemented!')
            return self._retval_helper(self._error_codes.NOK_FEATURE_TYPE_IS_NOT_READABLE[0], None, f"NOK: Feature: '{feature_name}' is type 'REGISTER' and therefore not readable !")
   
        else:
            print(f"ERROR: {feature_param_dict['type']=}")
            return self._retval_helper(self._error_codes.NOK_FEATURE_IS_NOT_READABLE[0], None, f"NOK: Feature: '{feature_name}' is not readable !")



        return self._retval_helper(self._error_codes.OK[0], param_value_out)
        

    def set_register(self, address: str, val: str) -> (int, type(None), str):
        """
        set_register(self, address, val)
        Set a single register value. WARNING: This feature is only for experienced users. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
    
        Args:
            address (str): Register address
            val (str): Register value
    
        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
    
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        # check hex values
        if address[:2] != '0x' or val[:2] != '0x':
            return self._retval_helper(self._error_codes.NOK_FORMAT_HEX_VALUE[0])
        
        address = ctypes.c_char_p(address.encode())
        val = ctypes.c_char_p(val.encode())
    
        function = self.dll.csiSetRegisterValue
        function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
        retval = function(self.device_handle, address, val, 1)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
    
        return self._retval_helper(retval)
    
    
    def get_register(self, address: str, mask: str = '0xFFFFFFFF') -> (int, str, str):
        """
        get_register(self, address, mask)
        Get the actual register value represented as a string. WARNING: This feature is only for experienced users. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
    
        Args:
            address (str): Register address
            mask (str, optional): Bitmask
    
        Returns:
            tuple (int, str, str): (0, Register value, 'OK') or (Error Code, Register value, 'Error Message')
        """
     
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        # check hex value
        if address[:2] != '0x' or mask[:2] != '0x':
            return self._retval_helper(self._error_codes.NOK_FORMAT_HEX_VALUE[0], '')
        
        value = ctypes.create_string_buffer(10) # len(0x00000000) == 10
        address = ctypes.c_char_p(address.encode())
        
        function = self.dll.csiGetRegisterValue
        function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char * 10), ctypes.c_uint64]
        retval = function(self.device_handle, address, ctypes.cast(value, ctypes.c_char_p), 1)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        #mask and convert value        
        try:
            mask_int = int(mask, 16)
            value = int(value.value.decode('utf-8'), 16)
        except ValueError:
            return self._retval_helper(self._error_codes.NOK_FORMAT_HEX_VALUE[0], '')
        
        value = value & mask_int
        value = '0x' + hex(value)[2:].upper()
    
        return self._retval_helper(retval, value)


    def get_feature_parameter(self, feature_name: str, module: int = _ds.CSI_DEVICE_MODULE) -> (int, dict, str):
        """
        get_feature_parameter(self, feature_name, module)
        Returns the feature info dict of the requested feature. The dict contains information
        about the parameter.

        Args:
            feature_name (str): Feature name
            module (int, optional): Module

        Returns:
            tuple (int, dict, str): (0, param info dict, 'OK') or (Error Code, 0, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        param = _ds.csiFeatureParameter()
        
        function = self.dll.csiGetFeatureParameter
        function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(_ds.csiFeatureParameter), ctypes.c_int64]
        
        retval = self._handle_helper(module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        handle = retval[1]

        retval = function(handle, ctypes.c_char_p(feature_name.encode()), ctypes.byref(param), module)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)       
        
        
        retval = self._structure_to_dict_converter(param)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        param_info_dict = retval[1]

        return self._retval_helper(self._error_codes.OK[0], param_info_dict)
    
    
    def get_feature_enum_list(self, feature_name: str, module: int = _ds.CSI_DEVICE_MODULE) -> (int, list, str):
        """
        get_feature_enum_list(self)
        Returns all elements of a enumeration feature as a list of strings.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            feature_name (str): Feature name
            module (int, optional): Supported Values = [CSI_TRANSPORTLAYER_MODULE, CSI_INTERFACE_MODULE, CSI_DEVICE_MODULE, CSI_LOCAL_DEVICE_MODULE, CSI_STREAM_MODULE, CSI_BUFFER_MODULE]

        Returns:
            tuple (int, list, str): (0, Feature name list, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        if module not in _ds.CSI_MODULE_LIST:
            return self._retval_helper(self._error_codes.NOK_CSI_MODULE_NOT_AVAILABLE[0])

        retval = self.get_feature_parameter(feature_name, module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        feature_param_dict = retval[1]
        
        
        if feature_param_dict['type'] != _ds.CSI_ENUMERATION_TYPE:
            msg = f"NOK: The GenIcam parameter '{feature_name}', is not from type: 'CSI_ENUMERATION_TYPE' !" 
            self._set_error_message(self._error_codes.NOK_FEATURE_TYPE[0], msg)
            return self._retval_helper(self._error_codes.NOK_FEATURE_TYPE[0])
        
        retval = self._handle_helper(module)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        handle = retval[1]
        
        enum_list = []
        for i in range(feature_param_dict['enumCounter']):
            param_loop = _ds.csiFeatureParameter()
            function = self.dll.csiGetFeatureEnumEntryByIndex
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(_ds.csiFeatureParameter), ctypes.c_int64]
            retval = function(handle, ctypes.c_char_p(feature_name.encode()), i, ctypes.byref(param_loop), module)
            enum_list.append(param_loop.valueStr.decode())
            
        return self._retval_helper(self._error_codes.OK[0], enum_list) 
    
    
    def get_feature_dict(self) -> (int, dict, str):
        """
        get_feature_dict(self)
        Get all features from the device and return them as a dictionary.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:

        Returns:
            tuple (int, dict, str): (0, Feature, 'OK') or (Error Code, Empty Dict, 'Error Message')
        """

        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        feature = (_ds.csiFeatureParameter * _ds.MAX_FEATURE)()
        feature_list = _ds.FEATURE_PARAM_LIST_STRUCT()
        feature_list.feature = ctypes.cast(feature, ctypes.POINTER(_ds.csiFeatureParameter))

        # function call
        function = self.dll.csiGetFeatureList
        function.argtypes = [ctypes.c_uint64, ctypes.POINTER(_ds.FEATURE_PARAM_LIST_STRUCT), ctypes.c_int64]
        retval = function(self.device_handle, ctypes.byref(feature_list), 0) # mode = 0, don't get invisible features
        if retval != self._error_codes.OK[0]:
            # self._logger.error(self._retval_helper(retval, dict())[2])
            return self._error_description_helper(retval)
    
    
        max_level = feature_list.maxLevel + 1

        feature_names = list()
        level_ignore = max_level
        for _feat in range(feature_list.count):
            
            # get values
            name = feature[_feat].name.decode()
            level = feature[_feat].level
            _type = feature[_feat].type
            
            # reset, if we are at level 0
            if level == 0:
                feature_names.clear()
                actual_level = -1
            
            # actualize feature names list
            if actual_level < level:
                feature_names.append(name)  
            elif actual_level > level:
                _delta = actual_level - level
                for _x in range(_delta):
                    feature_names.pop(-1)
            feature_names[-1] = name

            # set actual level
            actual_level = level

            ignore_feature = False
            for _val in self.feature_not_valid:
                if _val == name:
                    ignore_feature = True
                    break
                
            # ignore child features
            if actual_level > level_ignore:
                continue
            else:
                level_ignore = max_level

            if ignore_feature:
                level_ignore = actual_level
                continue

            retval = self._get_feature_dict_helper(feature_names, actual_level, name, _type)
            
            # check
            if retval[0] != self._error_codes.OK[0]:
                print(f'Feature name: "{name}" is not valid.')
                # self._logger.error(self._retval_helper(retval[0], dict())[2])
                return self._retval_helper(retval[0], dict())

        return self._retval_helper(self._error_codes.OK[0], self.feature_dict)
    

    
    def upload_file(self, file_name: str, file_type: str) -> (int, type(None), str):
        """
        upload_file(self,dfs)
        Uploads a file from the PC to the device. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            file_name (str): file path of the file which is to be loaded to the device
            file_type (str): name of the filetype, must match to the file. Supported Values = [UserSet1, UserSet2, UserSet3, UserSet4, UserSet5, 
                                                                                               UserSet6, UserSet7, UserSet8, GammaLUT, DSNULUT1, DSNULUT2,
                                                                                               PRNULUT1, PRNULUT2, Application, Bitstream, 
                                                                                               Xml, PackageDescriptionFile]
        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        # check, if the file exists
        if file_name is None or not os.path.isfile(file_name):
            return self._retval_helper(self._error_codes.NOK_FILE_NOT_AVAILABLE[0])
        
        if  isinstance(file_name, str):
            file_name = bytes(file_name, 'utf8')
            
        if  isinstance(file_type, str):
            file_type = bytes(file_type, 'utf8')
            

        file_type_ptr = ctypes.create_string_buffer(_ds.CSI_INFO_STRING_BUFFER_SIZE)        
        
        function = self.dll.csiGetUpdateFileType
        function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char * _ds.CSI_INFO_STRING_BUFFER_SIZE), ctypes.c_size_t]
        retval = function(self.device_handle, file_name, ctypes.byref(file_type_ptr), _ds.CSI_INFO_STRING_BUFFER_SIZE)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        file_type_retval = file_type_ptr.value
        
        
        retval = self._type_check_upload(file_type, file_type_retval)
        if retval[0] != self._error_codes.OK[0]:
            return retval


        timeout = 60000 #timeout for the upload in ms
        function = self.dll.csiFileDownloadToDevice
        
        if self.API_version['major'] >= 0 and self.API_version['minor'] >= 16 and self.API_version['patch'] >= 4 and self.API_version['revision'] >= 0:
            #new version
            function.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
            retval = self.dll.csiFileDownloadToDevice(self.device_handle, self.device_handle, file_name, file_type, timeout, None, None)
            
        else:
            #old version
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
            retval = self.dll.csiFileDownloadToDevice(self.device_handle, file_name, file_type, timeout, None, None)
               
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
 
        return self._retval_helper(self._error_codes.OK[0])
    
  
    def upload_package(self, file_name: str) -> (int, type(None), str):
        """
        upload_package(self, file_name)
        Upload a (firmware) package to the camera.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            file_name (str): file path of the "listfile" which describes the package components.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """

        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]: 
            return retval
        
        # check, if the file exists
        if not os.path.isfile(file_name):
            return self._retval_helper(self._error_codes.NOK_FILE_NOT_AVAILABLE[0])

        # read file
        list_file = open(file_name,'r')
        lines = list_file.readlines()
        list_file.close()
        path = os.path.dirname(file_name)

        for line in lines:
            
            # ignore comments and VERSION
            if line[0] == ';':
                continue
        
            if 'VERSION' in line:
                print(line)
                continue
                        
            # get file name
            _file_type, _, _file_name = line.rpartition('=')
            _file_name = _file_name.strip()
            _file_type = _file_type.strip()
            _file_name = _file_name.split(",")[0]
            
            
            if _file_type == 'EXECUTE_COMMAND':
                
                if _file_name == 'DEVICE_PACKAGE_CONSISTENCY_CHECK':
                    retval = self.get_feature('DevicePackageConsistency')
                    if retval[0] != self._error_codes.OK[0]:
                        return retval
                    
                    consistency = retval[1]
                    
                    print(f'consistency = {bool(consistency)}')
                    if not consistency:
                        return self._retval_helper(self._error_codes.NOK_PACKAGE_CONSITENCY[0])
 
                elif _file_name == 'DEVICE_RESET':
                    print('device reset')
                    retval = self.set_feature('DeviceReset','1')
                    if retval[0] != self._error_codes.OK[0]:
                        return retval
                    
                continue

            print(f'Upload: {_file_name}')

            file_name = (path + os.sep + _file_name).encode()
            file_type = (_file_type.encode())
            
            retval = self.upload_file(file_name, file_type)
            if retval[0] != self._error_codes.OK[0]:
                return retval
        
        return self._retval_helper(self._error_codes.OK[0])
    
    
    def download_file(self, file_name: str, file_type: str) -> (int, type(None), str):
        """
        download_file(self, file_name, file_type)
        Downloads a file from the device to the PC. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            file_name (str): save file path of the file which is to be downloaded from the device.
            file_type (str): name of the filetype. Supported Values = [UserSet1, UserSet2, UserSet3, UserSet4, UserSet5, 
                                                                        UserSet6, UserSet7, UserSet8, GammaLUT, DSNULUT1, DSNULUT2,
                                                                        PRNULUT1, PRNULUT2, Application, Bitstream, 
                                                                        Xml, PackageDescriptionFile]

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """

        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        file_extension_assignment_dict = dict()
        file_extension_assignment_dict['UserSet'] = ['.txt']
        file_extension_assignment_dict['GammaLUT'] = ['.dd']
        file_extension_assignment_dict['DSNULUT'] = ['.dsnu']
        file_extension_assignment_dict['PRNULUT'] = ['.prnu']
        file_extension_assignment_dict['Application'] = ['.bin']
        file_extension_assignment_dict['Bitstream'] = ['.bin']
        file_extension_assignment_dict['Xml'] = ['.xml']
        file_extension_assignment_dict['PackageDescriptionFile'] = ['.txt']
        
        if re.sub(r'[0-9]', '', file_type) not in file_extension_assignment_dict:
            return self._retval_helper(self._error_codes.NOK_FILE_TYPE_VALID[0]) 

        file_extension_list = file_extension_assignment_dict[re.sub(r'[0-9]', '', file_type)]

        filename_helper_data_dict = {'filename' : file_name,
                                     'file_extension_list' : file_extension_list,
                                     }
        
        retval = self._filename_helper(**filename_helper_data_dict)
        if retval[0] != self._error_codes.OK[0]: 
            return (retval[0], None, retval[2])
        
        file_name, _file_path, _file_name, _file_extension = retval[1]
        
        if  isinstance(file_name, str):
            file_name = bytes(file_name, 'utf8')
            
        if  isinstance(file_type, str):
            file_type = bytes(file_type, 'utf8')
            
        timeout = 60000 #timeout for the download in ms            

        #interface changed in the API
        function = self.dll.csiFileUploadFromDevice
        
        if self.API_version['major'] >= 0 and self.API_version['minor'] >= 16 and self.API_version['patch'] >= 4 and self.API_version['revision'] >= 0:
            #new version
            function.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
            retval = self.dll.csiFileUploadFromDevice(self.device_handle, self.device_handle, file_name, file_type, timeout, None, None)
            
        else:
            #old version
            function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
            retval = self.dll.csiFileUploadFromDevice(self.device_handle, file_name, file_type, timeout, None, None)
            
            
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0])
    
    
    
    def discover_devices(self, tl_producer_file_path: Union[str, list, type(None)]  = None)  -> (int, list, str):
        """
        discover_devices(self, tl_producer_file_path)
        Finds all devices with the specified transport layer. Returns a device info dict.
        The len of the dict correspond to the number of devices found. If no devices are found,
        the dict is empty. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            tl_producer_file_name (Union(str, list, type(None)), optional): Path to the transport layer producer file (.cti) 
                                                                            or a list with multiple paths to producer files. 
                                                                            If not specified the system enviornment path list
                                                                            GENICAM_GENTL64_PATH is used.

        Returns:
            tuple (int, list, str): (0, device info dict list, 'Error Message') 
        """
        
        discovery_info = _ds.csiDiscoveryInfo()

        #search in the GENTL_PATH64 for transport layers is no TL is specified.
        if tl_producer_file_path is None:    
            tl_producer_file_path_tmp = os.environ.get('GENICAM_GENTL64_PATH')
            if tl_producer_file_path_tmp is None:
                return self._retval_helper(self._error_codes.NOK_ENVIORNMENT_PATH_NOT_AVAILABLE[0])
            
            tl_producer_file_path = tl_producer_file_path_tmp.split(';')
            
        #handles a string input (single TL specified)
        if isinstance(tl_producer_file_path, str):
            tl_producer_file_path = [tl_producer_file_path]
            
        valid_producer_list = []
        for _tl_producer_file_path in tl_producer_file_path:
            
            if os.path.isdir(_tl_producer_file_path):
                valid_producer_list.append(_tl_producer_file_path)
                
            elif os.path.isfile(_tl_producer_file_path):
                valid_producer_list.append(os.path.dirname(_tl_producer_file_path))
                
            else:
                #skip not valid TL paths
                continue

        if not valid_producer_list:
            return self._retval_helper(self._error_codes.NOK_FILE_NOT_AVAILABLE[0])
        
        # add the list of single valid producer stings to concat string 
        tl_producer_file_name_str = ';'.join(valid_producer_list)
        
        
        function = self.dll.csiDiscoverDevices
        function.argtypes = [ctypes.POINTER(_ds.csiDiscoveryInfo), ctypes.c_uint64]
        
        retval = function(ctypes.byref(discovery_info), self.discovery_timeout, None, ctypes.c_char_p(tl_producer_file_name_str.encode()), True)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        

        discovery_info_dict_list = list()
        for i in range(discovery_info.numDevices):
            
            
            retval = self._structure_to_dict_converter(discovery_info.devices[i])
            if retval[0] != self._error_codes.OK[0]:
                return retval
            discovery_info_dict = retval[1]
            discovery_info_dict_list.append(discovery_info_dict)
            
        return self._retval_helper(self._error_codes.OK[0], discovery_info_dict_list)
 
    
    def _check_helper(self) -> (int, type(None), str):
        """
        _check_helper(self, _value)
        Helper, for checking the basic conditions.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:


        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """

        # check dll
        if self.dll is None:
            return self._retval_helper(self._error_codes.NOK_NO_DLL[0])
        
        # check cam number
        if not self.device_handle:
            return self._retval_helper(self._error_codes.NOK_CAMERA_IS_NOT_OPEN[0])

         # ok
        return self._retval_helper(self._error_codes.OK[0])
    
    
    def _get_feature_dict_helper(self, feature_names, actual_level, name, _type) -> (int, type(None), str):
        """
        _get_feature_dict_helper(self, _key, _value)
        Helper, for creating the feature dictionary.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            feature_names (list): Feature names 
            actual_level (int): Actual feature level
            name (str): Actual feature name
            _type (int): Feature type

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        enum_list = list()
        
        if _type == _ds.CSI_ENUMERATION_TYPE:
            
            # get enum names
            retval = self._get_feature_enum_names(name)

            # check
            if retval[0] != self._error_codes.OK[0]:
                return self._retval_helper(retval[0])
            
            # populate list
            tmp = retval[1].split()
            for _val in tmp:
                enum_list.append(_val)
                
        if _type == _ds.CSI_BOOLEAN_TYPE:
            
            enum_list.append('False')
            enum_list.append('True')
        
        new_dict = {'{}'.format(name): {'type': _type, 'enums': enum_list, 'childs': {}}}
        
        # root feature
        if actual_level == 0:
            self.feature_dict[name] = new_dict[name]
        # get last feature and update
        else:
            for _x in range(actual_level):
                if _x == 0:
                    parent_dict = self.feature_dict[feature_names[_x]]['childs']
                else:
                    parent_dict = parent_dict[feature_names[_x]]['childs']
            parent_dict.update(new_dict)
            
        return self._retval_helper(self._error_codes.OK[0])
                
            
    def _get_feature_enum_names(self, _name: str) -> (int, str, str):
        """
        _get_feature_enum_names(self, _name)
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            _name (str): Feature name

        Returns:
            tuple (int, str, str): (0, Value, 'OK') or (Error Code, '', 'Error Message')
        """
        
        feature_enum_values = ''
        msg = ''

        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        name = ctypes.c_char_p(_name.encode())
        value = ctypes.c_char_p(bytes(_ds.MAX_FEATURE_ENUM_NAMES_LENGTH))
        
        function = self.dll.csiGetFeatureAllEnums
        function.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
        retval = function(self.device_handle, name, value, 0) # only space as seperator
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)

        retval, feature_enum_values, msg = self._get_pointer_value(value, retval)

        return self._retval_helper(retval, feature_enum_values, msg)
    
    
    def _type_check_upload(self, file_type: bytes, file_type_retval: bytes) -> (int, type(None), str):
        """
        _type_check_upload(self, file_type, file_type_retval)
        compares the specified filetpype with the filetype that is returend from the CSI function 
        that is used to request the filetype of a file. Returns an errormessage if the types
        don't match or if the filetype is invalid for an upload in the camera. 
        
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            _name (str): Feature name

        Returns:
            tuple (int, str, str): (0, Value, 'OK') or (Error Code, '', 'Error Message')
        """
        
        pattern = r'[0-9]'
        file_type_retval_comp = re.sub(pattern, '', file_type_retval.decode())
        file_type_comp = re.sub(pattern, '', file_type.decode())
        
        #filetype is not valid for the camera
        if file_type_retval_comp == '':
            return self._retval_helper(self._error_codes.NOK_FILE_TYPE_VALID[0])
        
        #filetype from the function  "csiGetUpdateFileType" doesn't match to the selected filetype
        if file_type_comp != file_type_retval_comp:         
            if (file_type_retval_comp == 'Default') and (file_type_comp == 'UserSet'):
                return self._retval_helper(self._error_codes.OK[0])
            else:
                msg = f"NOK: The specified fileytpe: '{file_type_comp}' doesn't match to the selected filetype: '{file_type_retval_comp}'"
                self._set_error_message(self._error_codes.NOK_FILE_TYPE_MATCH[0], msg)
                return self._retval_helper(self._error_codes.NOK_FILE_TYPE_MATCH[0])
        
        return self._retval_helper(self._error_codes.OK[0])
            
    
    def _handle_helper(self, module: int) -> (int, int, str):
        """
        _handle_helper(self, module)
        Returns the handle that corresponds to the module identifyer. The handle must be used to 
        access functions of the corresponding modules. 
        
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            _name (str): Feature name

        Returns:
            tuple (int, str, str): (0, Value, 'OK') or (Error Code, '', 'Error Message')
        """
        
        if module not in _ds.CSI_MODULE_LIST:
            return self._retval_helper(self._error_codes.NOK_CSI_MODULE_NOT_AVAILABLE[0])
        
        if module  == _ds.CSI_DEVICE_MODULE:
            handle = self.device_handle
            
        elif module == _ds.CSI_STREAM_MODULE:
            handle = self.datastream_handle
            
        else:
            return self._retval_helper(self._error_codes.NOK_MODULE_HANDLE[0])
            
        return self._retval_helper(self._error_codes.OK[0], handle) 
    
    def _error_description_helper(self, error_code: int) -> (int, type(None), str):
        """
        _error_description_helper(self, _value, _type)
        Returns a text errormessage for a DLL errorcode.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            _value (str): Feature value
            _type (str): Feature type

        Returns:
            tuple (int, str, str): (0, Value, 'OK') or (Error Code, '', 'Error Message')
        """

        error_str = ctypes.create_string_buffer(_ds.CSI_INFO_STRING_BUFFER_SIZE) 
        
        function = self.dll.csiGetErrorDescription
        function.argtypes = [ctypes.c_int64, ctypes.POINTER(ctypes.c_char * _ds.CSI_INFO_STRING_BUFFER_SIZE), ctypes.c_size_t]
        
        retval = function(error_code, ctypes.byref(error_str), ctypes.sizeof(error_str))
        
        if retval != 0:
            msg = "NOK: DLL error number: '{retval}' - unknown DLL error"
        else:
            msg = f"NOK: DLL error number: '{error_code}' - {error_str.value.decode()}"
            
        self._set_error_message(self._error_codes.NOK_DLL_ERROR[0], msg)
        return self._retval_helper(self._error_codes.NOK_DLL_ERROR[0])
    
    
    def _structure_to_dict_converter(self, structure) -> (int, dict, str):
                
        param_dict = dict()
        for field_name, field_type in list(structure._fields_):
            #print(f'{field_name:<20} --> {str(field_type):<20} --> {issubclass(field_type, ctypes._SimpleCData)}')
            
            if issubclass(field_type, ctypes._SimpleCData):  
                #normal ctypes variable -> write directly in the dict
                param_dict[field_name] = getattr(structure,field_name)
                
            else:
                sub_structure = getattr(structure, field_name)
                
                #handle equal to ctypes._SimpleCData?
                if not hasattr(sub_structure, '_fields_'):
                    param_dict[field_name] = getattr(structure,field_name)
                    continue
                
                #nested substructure -> write the substructure as a subdict 
                retval = self._structure_to_dict_converter(sub_structure)
                if retval[0] != self._error_codes.OK[0]:
                    return retval
                
                subdict = retval[1]
                param_dict[field_name] = subdict
                    
        return self._retval_helper(self._error_codes.OK[0], param_dict) 
    

class GenICamStreamable(GenICamBase):
    '''
    This class is intended to represent GenIcam devices which have the property "streamable" (Cameras / Sensors / ....)
    '''
    
    def __init__(self, dll_dir_path: str = r'C:\Program Files\Chromasens\GCT2\bin'):
        """"
        __init__(self, dll_dir_path)
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            dll_dir_path (str, optional): The path to the folder that contains the CSI file. 
            The CSI file represents the Chromasens SDK and provides functions to setup the 
            camera and grab images. For default installation the default parameter value can
            be used. 

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        super().__init__(dll_dir_path)
        
        self.new_buffer_event_handle = 0
        self.datastream_handle = 0
        
        self.camera_is_streaming = False
        self.stream_image_counter = None
        self.start_stream_imageNr = 0
        
    def __del__(self):
        
        super().__del__()
        
        
    def open_connection(self, tl_producer_file_name: Union[str, list, type(None)] = None, device_number: int = 1, num_buffers: int = 5) -> (int, type(None), str):
        """
        open_connection(self, tl_producer_file_name, device_number, num_buffers)
        Opens the connection to the GenIcam device via the transport layer. 
        The transport layer file (.cti) is provided by Chromasens in case 
        of a system without a framegrabber.
        
        S2I     - r'C:\Program Files\Chromasens\GCT2\GenTL\s2i\GEVTLS2I.cti'
        Kithara - r'C:\Program Files\Chromasens\GCT2\GenTL\Kithara\tkh_tl_gev_kithara.cti'
        
        For systems with a framegrabber the .cti file is provided by the framegrabber
        manufacturer. The following is an example of an Euresys CXP12 grabber.
        
        Euresys CXP12 - r'C:\Program Files\Euresys\eGrabber\cti\x86_64\coaxlink.cti'
        

        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            tl_producer_file_name (Union(str, list, type(None)), optional): Path to the transport layer producer file (.cti) 
                                                                            or a list with multiple paths to producer files. 
                                                                            If not specified the system enviornment path list
                                                                            GENICAM_GENTL64_PATH is used.
            device_number (int): Device number. For multiple devices for the same TL the device number must be incremented.
                                 Count starts at 1.            
            num_buffers (int, optional): number of buffers in the image FIFO buffer. 
                                         A lage number consumes a large amout of RAM.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        retval = super().open_connection(tl_producer_file_name, device_number)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        #abort camera stream (in case camera was not propertly closed after the last acquisition)
        try:
            retval = self.set_feature('AcquisitionAbort', '1')
            if retval[0] != self._error_codes.OK[0]:
                return retval
        except:
            pass
    
        return self._open_datastream(num_buffers)
        
        
    def close_connection(self) -> (int, type(None), str):
        """
        close_connection(self)
        Closes the camera datastream and the camera connection.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        if self.camera_is_streaming:
            self.stop_grab_image_async()
        
        retval = self._close_datastream()      
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        return super().close_connection()
   
    
    def grab_image_sync(self, timeout_ms: int = 5000)  -> (int, tuple, str):
        """
        grab_image_sync(self, timeout_ms = 5000)
        This function is a convenience function to acquire a single image.
        "grab_image_sync" is the complete sequence of the "grab_image_async" procedure. 
        In the background a sequence of the following methods are started. 
        -start_grab_image_async (in single frame mode)
        -grab_image_async
        -stop_grab_image_async
        Also sets the camera genicam parameter "AcquisitionMode" to "SingleFrame"
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            timeout_ms (int, optional): If the function has to wait longer than the "timeout_ms" for a new image, an error is generated.
            
        Returns:
            tuple (int, tuple(np.ndarray, dict), str): (0, (image, image metadata dict), 'OK') or (Error Code, '', 'Error Message')
        """
        
        retval = self.start_grab_image_async(grab_single_img = True)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        retval = self.grab_image_async(timeout_ms, False)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        #img data is a tuple with the img as np.array and a metadata dict
        img_data = retval[1]
        
        retval = self.stop_grab_image_async()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        return self._retval_helper(self._error_codes.OK[0], img_data) 
        
    
    def start_grab_image_async(self, grab_single_img: bool = False)  -> (int, type(None), str):
        """
        start_grab_image_async(self)
        This function starts an continious image acquisiton thread. After the acquisition
        thread is started, images can be acessed from the buffer with "grab_image_async".
        If all buffers are filled with images, new images are are rejected (buffer overflow).
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            grab_single_img(bool, optional): This function can be used to acquire a single image.
                                            With 'grab_single_img' = True only a single image 
                                            can be grabbed with "grab_img_acync". After this, the 
                                            stream has to be closed and reopened. 

        Returns:
            tuple (int, tuple(np.ndarray, dict), str): (0, (image, image metadata dict), 'OK') or (Error Code, '', 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        if self.camera_is_streaming:
            return self._retval_helper(self._error_codes.NOK_STREAM_ALREADY_ACTIVE[0])
        
        if grab_single_img:
            acquisition_mode_cam = 'SingleFrame'
            acquisition_mode_cam_dll = _ds.CSI_ACQUISITION_SINGLE_FRAME
        else:
            acquisition_mode_cam = 'Continuous'
            acquisition_mode_cam_dll = _ds.CSI_ACQUISITION_CONTINUOUS
        
        retval = self.set_feature('AcquisitionMode', acquisition_mode_cam)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        return self._start_acquisition(acquisition_mode_cam_dll)
    
     
    
    def grab_image_async(self, timeout_ms: int = 5000, raise_buffer_overflow_error: bool = False) -> (int, tuple, str):
        """
        grab_image_async(self, timeout_ms = 5000, raise_buffer_overflow_error = False)
        This function starts an continious image acquisiton thread if it is not already started.
        As soon a image is in the image buffer this function grabs the first image in the buffer (FIFO).
        The function provides the buffer content as np.array + metadata and releases the buffer allocation. 
        If all buffers are filled with images, new images are are rejected (buffer overflow).
        
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            timeout_ms (int, optional): If the function has to wait longer than the "timeout_ms" for a new image, an error is generated.
            raise_buffer_overflow_error (bool, optional): If frames are lost (buffer overflow) the function raises an error if "True".

        Returns:
            tuple (int, tuple(np.ndarray, dict), str): (0, (image, image metadata dict), 'OK') or (Error Code, '', 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        if not self.camera_is_streaming:
            retval = self.start_grab_image_async()
            if retval[0] != 0:
                return retval
 
           
        retval = self._function_call_get_next_image(timeout_ms)
        if retval[0] != 0:
            return retval
        
        ptr = retval[1]
    
        #create a dict with image meatadata 
        data_struct = ptr.contents
        
        
        param = ptr.contents
        
        retval = self._structure_to_dict_converter(ptr.contents)
        if retval[0] != 0:
            return retval
        
        img_metadata_dict = retval[1]
        
        if self.stream_image_counter is None:
            self.stream_image_counter = img_metadata_dict['imageNr']
            self.start_stream_imageNr = img_metadata_dict['imageNr'] - 1
        else:
            self.stream_image_counter += 1
            if raise_buffer_overflow_error:
                if self.stream_image_counter != img_metadata_dict['imageNr']:
                    msg = f"NOK: Buffer overflow error, image acquisition if faster than image handling! -> imageNr: {img_metadata_dict['imageNr']} | stream_image_counter: {self.stream_image_counter}"
                    self._set_error_message(self._error_codes.NOK_BUFFER_OVERFLOW[0], msg)
                    return self._retval_helper(self._error_codes.NOK_BUFFER_OVERFLOW[0])
         
        #add an image counter wich starts at 0 for a new stream
        img_metadata_dict['streamImageNr'] = img_metadata_dict['imageNr'] - self.start_stream_imageNr
        
        #convert the pointer to the image to a np.array
        p_img = data_struct.eventValue
        retval = self._convert_pointer_to_ndarray(p_img, data_struct.imageInfo)
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        img = retval[1]
        retval = self._convert_pixel_format(img, data_struct.imageInfo)
        #method doesn't contain errormessages at the moment
        if retval[0] != self._error_codes.OK[0]:
            return retval
        img = retval[1]
        
        #release the image memory
        function = self.dll.csiReleaseImage
        function.argtypes = [ctypes.c_uint64, ctypes.POINTER(_ds.csiNewBufferEventData)]
        
        retval = function(self.datastream_handle, ptr)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0], (img, img_metadata_dict)) 
    
    

    def abort_grab_image_async(self) -> (int, type(None), str):
        """
        abort_grab_image_async(self)
        This function stops the camera image acquisition immediately.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        function = self.dll.csiAbortAcquisition
        function.argtypes = [ctypes.c_uint64]
        retval = function(self.device_handle)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        self.camera_is_streaming = False
        
        return self._retval_helper(self._error_codes.OK[0]) 
    
    
            
    def stop_grab_image_async(self) -> (int, type(None), str):
        """
        stop_grab_image_async(self)
        This function stops the camera image acquisition after the complete acquisition of the current image.
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        function = self.dll.csiStopAcquisition
        function.argtypes = [ctypes.c_uint64]
        retval = function(self.device_handle)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        self.camera_is_streaming = False
        
        return self._retval_helper(self._error_codes.OK[0]) 
    
    
    def set_num_of_stream_buffers(self, num_buffers: int)  -> (int, type(None), str):
        """
        set_num_of_stream_buffers(self, num_buffers)
        Closes and unregisters a camera datastream and open and register it again with a
        new number of buffers. 
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            num_buffers (int): number of buffers in the image FIFO buffer. 
                                A lage number consumes a large amout of RAM.

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        # check
        retval = self._check_helper()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        if self.camera_is_streaming:
            retval = self.stop_grab_image_async()
            if retval[0] != self._error_codes.OK[0]:
                return retval
            
        retval = self._close_datastream()
        if retval[0] != self._error_codes.OK[0]:
            return retval
        
        return self._open_datastream(num_buffers)


    def _function_call_get_next_image(self, timeout_ms) -> (int, ctypes.POINTER(ctypes.c_ubyte), str):
        """
        _function_call_get_next_image(self)
        This helper function calls the "csiGetNextImage" function to get a pointer to the next image and metadata in the FIFO buffer.
        
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.
        
        Args:
            timeout_ms (int): If the function has to wait longer than the "timeout_ms" for a new image, an error is generated.

        Returns:
            tuple (int, ctypes.POINTER(ctypes.c_ubyte), str): (0, (image_data_pointer), 'OK') or (Error Code, '', 'Error Message')
        """
        
        #create a pointer to the result structure
        ptr = ctypes.POINTER(_ds.csiNewBufferEventData)()
        
        function = self.dll.csiGetNextImage
        function.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(_ds.csiNewBufferEventData)), ctypes.c_uint64]
        
        #provide a pointer to a pointer
        retval = function(self.new_buffer_event_handle, ctypes.byref(ptr), timeout_ms)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0], ptr) 


    def _open_datastream(self, num_buffers: int, stream_index: int = 0)  -> (int, type(None), str):
        """
        _open_datastream(self, num_buffers, stream_index)
        Opens and registers the camera datastream. This happens automatically when the "open_connection" function is used. 
        To change the number of buffers, the datastream have to be closed and opended again.  
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            num_buffers (int): number of buffers in the image FIFO buffer. 
                                A lage number consumes a large amout of RAM.
            stream_index (int): index of the stream. Only one stram possible for CHR cameras

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        self.datastream_handle = _ds.csiHandle(0)
        
        function = self.dll.csiCreateDataStream
        function.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint64]
        
        retval = function(self.device_handle, stream_index, ctypes.byref(self.datastream_handle), num_buffers, 0)
        if retval != self._error_codes.OK[0]:
            self.datastream_handle = 0
            return self._error_description_helper(retval)
        
        #activate filter driver for S2I TL
        if self.transportLayerID == 'GEVTLS2I.cti':
            retval = self.set_feature('EnableFilterDriver', True, _ds.CSI_STREAM_MODULE)
            if retval[0] != self._error_codes.OK[0]:
                return self._error_description_helper(retval)

        self.new_buffer_event_handle = _ds.csiHandle(0)
        event_type = _ds.csiHandle(_ds.CSI_EVT_NEWIMAGEDATA)
        
        function = self.dll.csiRegisterEvent
        function.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64)]
        
        retval = function(self.datastream_handle, event_type, ctypes.byref(self.new_buffer_event_handle))
        if retval != self._error_codes.OK[0]:
            self.new_buffer_event_handle = 0
            return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0]) 
    
    
    def _close_datastream(self)  -> (int, type(None), str):
        """
        _close_datastream(self,)
        Unregisters and closes the camera datastream. This happens automatically when the "close_connection" function is used.  
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
    
        if self.new_buffer_event_handle != 0:
            function = self.dll.csiUnregisterEvent
            function.argtypes = [ctypes.c_uint64]
            retval = function(self.new_buffer_event_handle)
            if retval != self._error_codes.OK[0]:
                return self._error_description_helper(retval)
        
        if self.datastream_handle != 0:
            function = self.dll.csiCloseDataStream
            function.argtypes = [ctypes.c_uint64]
            retval = function(self.datastream_handle)
            if retval != self._error_codes.OK[0]:
                return self._error_description_helper(retval)
        
        return self._retval_helper(self._error_codes.OK[0]) 
        

    def _start_acquisition(self, stream_type: int = _ds.CSI_ACQUISITION_CONTINUOUS) -> (int, type(None), str):
        """
        _start_acquisition(self, stream_type)
        Starts the image acquisition of the camera.  
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            stream_type (int): Select if a single image stream or a continious stream is initialized.
                               Supported Values = [CSI_ACQUISITION_CONTINUOUS, CSI_ACQUISITION_SINGLE_FRAME]
   
        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """
        
        #check if the image size of format have changed
        function = self.dll.csiCheckAndReallocBuffers
        function.argtypes = [ctypes.c_uint64]
        retval = function(self.device_handle)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)
        
        #csiReadMemory

        function = self.dll.csiStartAcquisition
        function.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
        
        retval = function(self.device_handle, stream_type)
        if retval != self._error_codes.OK[0]:
            return self._error_description_helper(retval)

        self.camera_is_streaming = True
        self.stream_image_counter = None
        
        return self._retval_helper(self._error_codes.OK[0])


    def _convert_pointer_to_ndarray(self, p_img: ctypes.POINTER(ctypes.c_ubyte), info: _ds.csiImageInfo) -> (int, type(None), str):
        """
        _convert_pointer_to_ndarray(self, p_img, info)
        converts an image pointer that is returned by the CS-API  to a np.ndarray
        For more details regarding the Error Codes, please have a look at :class:`ERROR_CODES`.

        Args:
            p_img (ctypes.POINTER(ctypes.c_ubyte)): pointer to the image data
            info (_ds.csiImageInfo): struct with image information data

        Returns:
            tuple (int, type(None), str): (0, None, 'OK') or (Error Code, None, 'Error Message')
        """

        # check, if we can handle the format
        if info.format not in _ds.SUPPORTED_PIX_FORMATS:
            return self._retval_helper(self._error_codes.NOK_IMAGE_FORMAT)
        
        bytes_per_pixel = self.dll.csiBitsPerPixelFromFormat(info.format) // 8
        width = info.width
        height = info.height
        
        # special formats
        if info.format == _ds.CSI_PIX_FORMAT_RGB10_PACKED:
            bytes_per_pixel = 1
            width = int(info.width * 4) # 1 pixel in 4 bytes
        elif info.format == _ds.CSI_PIX_FORMAT_MONO12_PACKED:
            bytes_per_pixel = 1
            width = int(info.width * 3/2) # 2 pixel in 3 bytes
        elif info.format == _ds.CSI_PIX_FORMAT_MONO10_PACKED:
            bytes_per_pixel = 1
            width = int(info.width * 5/4) # 4 pixel in 5 bytes

        # convert pointer to numpy array
        # 8 bit rgb, bgr or rgba
        if bytes_per_pixel in range(3,5):
            img = np.ctypeslib.as_array(p_img, (height, width, bytes_per_pixel)).copy()
        # 10, 12 and 16 bit rgb, bgr, bgra or rgba
        elif bytes_per_pixel in [6,8]:
            img = np.ctypeslib.as_array(ctypes.cast(p_img, ctypes.POINTER(ctypes.c_uint16)), (height, width, int(bytes_per_pixel/2))).copy()
        # 8 bit mono or special formats
        elif bytes_per_pixel == 1:
            img = np.ctypeslib.as_array(p_img, (height, width)).copy()
        # 10, 12 and 16 bit mono or special formats
        elif bytes_per_pixel == 2:
            img = np.ctypeslib.as_array(ctypes.cast(p_img, ctypes.POINTER(ctypes.c_uint16)), (height, width)).copy()
        else:
            return self._retval_helper(self._error_codes.NOK_IMAGE_FORMAT)
            
        return self._retval_helper(self._error_codes.OK[0], img)
    
    
    def _convert_pixel_format(self, img: np.ndarray, img_info: _ds.csiImageInfo) -> (int, np.ndarray, str):
        """
        _convert_pixel_format(self)
        Helper to convert special pixel formats.
        
        Args:
            img_info (_ds.csiImageInfo): Image info

        Returns:
            tuple (int, np.ndarray, str): (0, image, 'OK') or (Error Code, '', 'Error Message')
        """
        
        # CSI_PIX_FORMAT_RGB8, CSI_PIX_FORMAT_RGB16, CSI_PIX_FORMAT_BGR8
        # CSI_PIX_FORMAT_RGBA8, CSI_PIX_FORMAT_MONO8, CSI_PIX_FORMAT_MONO16
        _img = img

        if (img_info.format == _ds.CSI_PIX_FORMAT_MONO10 or img_info.format == _ds.CSI_PIX_FORMAT_RGB10
            or img_info.format == _ds.CSI_PIX_FORMAT_RGBA10):
            _img = img << 6
        elif (img_info.format == _ds.CSI_PIX_FORMAT_MONO12 or img_info.format == _ds.CSI_PIX_FORMAT_RGB12
            or img_info.format == _ds.CSI_PIX_FORMAT_RGBA12):
            _img = img << 4
        elif img_info.format == _ds.CSI_PIX_FORMAT_RGB10_PACKED: # rgb10p32msb
            img_work = np.uint16(img)
            _img = np.zeros((img_info.height, img_info.width, 3), dtype=np.uint16)
            _img[:,:,0] = ((img_work[:,0::4] & 0x00FF) << 2) | ((img_work[:,1::4] & 0x00C0) >> 6) # red
            _img[:,:,1] = ((img_work[:,1::4] & 0x003F) << 4) | ((img_work[:,2::4] & 0x00F0) >> 4) # green
            _img[:,:,2] = ((img_work[:,2::4] & 0x000F) << 6) | ((img_work[:,3::4] & 0x00FC) >> 2) # blue
            _img = _img << 8
        elif img_info.format == _ds.CSI_PIX_FORMAT_MONO12_PACKED:
            img_work = np.uint16(img)
            _img = np.zeros((img_info.height, img_info.width), dtype=np.uint16)
            _img[:,0::2] = (img_work[:,0::3] & 0x00FF) | ((img_work[:,1::3] & 0x000F) << 8)
            _img[:,1::2] = ((img_work[:,1::3] & 0x00F0) >> 4) | ((img_work[:,2::3] & 0x00FF) << 4)
            _img = _img << 4
        elif img_info.format == _ds.CSI_PIX_FORMAT_MONO10_PACKED:
            img_work = np.uint16(img)
            _img = np.zeros((img_info.height, img_info.width), dtype=np.uint16)
            _img[:,0::4] = (img_work[:,0::5] & 0x00FF) | ((img_work[:,1::5] & 0x0003) << 8)
            _img[:,1::4] = ((img_work[:,1::5] & 0x00FC) >> 2) | ((img_work[:,2::5] & 0x000F) << 6)
            _img[:,2::4] = ((img_work[:,2::5] & 0x00F0) >> 4) | ((img_work[:,3::5] & 0x003F) << 4)
            _img[:,3::4] = ((img_work[:,3::5] & 0x00C0) >> 6) | ((img_work[:,4::5] & 0x00FF) << 2)
            _img = _img << 6
        elif img_info.format in _ds.BAYER_PIX_FORMATS:    
            
            # rggb pattern
            if img_info.format in _ds.BAYER_RG_PIX_FORMATS:
                _img = cv2.cvtColor(img, cv2.COLOR_BayerRG2BGR)
            
            # grbg pattern
            elif img_info.format in _ds.BAYER_GR_PIX_FORMATS:
                _img = cv2.cvtColor(img, cv2.COLOR_BayerGR2BGR)
            
            # gbrg pattern
            elif img_info.format in _ds.BAYER_GB_PIX_FORMATS:
                _img = cv2.cvtColor(img, cv2.COLOR_BayerGB2BGR)
            
            # bggr pattern
            elif img_info.format in _ds.BAYER_BG_PIX_FORMATS:
                _img = cv2.cvtColor(img, cv2.COLOR_BayerBG2BGR)
                
            # shift
            if img_info.format in _ds.BAYER_10_PIX_FORMATS:
                _img = _img << 6
            elif img_info.format in _ds.BAYER_12_PIX_FORMATS:
                _img = _img << 4
                
        return self._retval_helper(self._error_codes.OK[0], _img)
    
    

def camera_communication(cam_list: list) -> (int, type(None), str):
    '''
    Example programm how to set and get features and how to download and upload
    files from the camera. 

    Parameters
    ----------
    cam_list : list
        list with at least one opened (open_connection) instance(s) of the 
        GenICamStreamable class.

    Returns
    -------
    (int, type(None), str)
        Returns a tuple with (Error Code, None, 'Error Message').
    '''
    
    #print string represenation of the device with the basic infos
    for cam in cam_list:
        print(f'{cam}\n')

    #Downloads UserSet1 of the camera to the PC
    for i, cam in enumerate(cam_list):
        file_name = rf'C:\Users\Public\Documents\Chromasens\UserSet1_cam{i:0<2}.txt'
        file_type = 'UserSet1'
        print(f'Download {file_type} to {file_name}')
        retval = cam.download_file(file_name, file_type)
        if retval[0] != 0:
            return retval 
      
    #Uploads the saved UserSet to UserSet1 to the camera
    for i, cam in enumerate(cam_list):
        
        file_name = rf'C:\Users\Public\Documents\Chromasens\UserSet1_cam{i:0<2}.txt'
        file_type = 'UserSet1'
        print(f'Uploads the file {file_name} to {file_type} to the camera\n')
        retval = cam.upload_file(file_name, file_type)
        if retval[0] != 0:
            return retval 
        
        
    command_dict = dict()
    command_dict['AcquisitionLineTime'] = '200'
    command_dict['ExposureTime'] = '100'
    command_dict['Height'] = '2000'
    
    #write parameters in the camera
    for i, cam in enumerate(cam_list):
        for key, value in command_dict.items():
            print(f'Cam: {i:<2} -> Set parameter {key} to value {value}')
            retval = cam.set_feature(key, value)
            if retval[0] != 0:
                return retval 
    
    print('')
    
    #read parameters from the camera
    for i, cam in enumerate(cam_list):
        for key in command_dict.keys():
            
            retval = cam.get_feature(key)
            if retval[0] != 0:
                return retval 
            
            value = retval[1]
            print(f'Cam: {i:<2} -> Get (readout) parameter {key} to value {value}')
            
            
    return (0, None, 'OK')


def example_grab_images_sync(cam_list: list) -> (int, type(None), str):
    '''
    Example programm for synchon image acquisition. With synchronous image 
    acquisition, a single image is acquired in series with the program flow.

    The function configures the camera grabs 3 images, prints the imageID, 
    the image counter, and the (BGR) value of the first pixel for each image.

    Parameters
    ----------
    cam_list : list
        list with at least one opened (open_connection) instance(s) of the 
        GenICamStreamable class.

    Returns
    -------
    (int, type(None), str)
        Returns a tuple with (Error Code, None, 'Error Message').
    '''
    
    #configure the camera
    #load the default user set, activate GreyRamp (FPGA generated image output,
    #not sensor image), set the LineTime and the image height
    command_dict = dict()
    command_dict['UserSetSelector'] = 'Default'
    command_dict['UserSetLoad'] = '1'
    command_dict['TestPattern'] = 'GreyHorizontalRamp'
    command_dict['AcquisitionLineTime'] = '200'
    command_dict['Height'] = '2000'
    
    for cam in cam_list:
        for key, value in command_dict.items():
            retval = cam.set_feature(key, value)
            if retval[0] != 0:
                return retval 
    
    #acquires 3 single images synchon to the image processing
    x = 3
    for i in range(x):
        for cam in cam_list:
            retval = cam.grab_image_sync(timeout_ms = 5000)
            if retval[0] != 0:
                return retval
                
            img, img_info_dict = retval[1]
            
            # do img processing here
            #...
            #...
            print(f'cam: {i} | stream img nr.: {img_info_dict["streamImageNr"]:0>5} | img nr.: {img_info_dict["imageNr"]:0>5} |  first px. value: {img[0,0]}')
            
        
    return (0, None, 'OK')



def example_grab_images_async(cam_list: list) -> (int, type(None), str):
    '''
    Example programm for asynchon image acquisition. For asynchronous image 
    acquisition the API writes in a seperate thread asynchon to the image 
    processing the camera images in a FIFO buffer. 
    The images in the buffer can be acessed with the function 'grab_image_async'.
    
    The function configures the camera grabs 10 images, prints the imageID, 
    the image counter, and the (BGR) value of the first pixel for each image.

    Parameters
    ----------
    cam_list : list
        list with at least one opened (open_connection) instance(s) of the 
        GenICamStreamable class.

    Returns
    -------
    (int, type(None), str)
        Returns a tuple with (Error Code, None, 'Error Message').
    '''
    
    #configure the camera
    #load the default user set, activate GreyRamp (FPGA generated image output,
    #not sensor image), set the LineTime and the image height
    command_dict = dict()
    command_dict['UserSetSelector'] = 'Default'
    command_dict['UserSetLoad'] = '1'
    command_dict['TestPattern'] = 'GreyHorizontalRampMoving'
    command_dict['AcquisitionLineTime'] = '200'
    command_dict['Height'] = '2000'
    
    for cam in cam_list:

        for key, value in command_dict.items():
            retval = cam.set_feature(key, value)
            if retval[0] != 0:
                return retval 
            
    for cam in cam_list:
        #start the stream (Not necessary to explicitly start the stream)
        #"grab_image_async" automatically starts the stream if it is not already started.
        retval = cam.start_grab_image_async()
        if retval[0] != 0:
            return retval
    
    #acquires 10 images asynchron to the image processing
    x = 10
    for i in range(x):
        for i, cam in enumerate(cam_list):
            retval = cam.grab_image_async(timeout_ms = 5000, raise_buffer_overflow_error = False)

            if retval[0] != 0:
                return retval
        
            img, img_info_dict = retval[1]
            
            # do img processing here
            #...
            #...
            print(f'cam: {i} | stream img nr.: {img_info_dict["streamImageNr"]:0>5} | img nr.: {img_info_dict["imageNr"]:0>5} |  first px. value: {img[0,0]}')

    for cam in cam_list:
        retval = cam.stop_grab_image_async()
        if retval[0] != 0:
            return retval
        
    return (0, None, 'OK')
    


def main(tl_path: str, function: object, n_cam: int = 1):
    '''
    This function creates one or multiple instances of the GenICamStreamable class,
    establishs a connection to the camera(s), executes the input function and closes 
    the camera(s) afterwards.

    Parameters
    ----------
    tl_path : str
        Path the the transport layer file.
        The transport layer file (.cti) is provided by Chromasens in case 
        of a system without a framegrabber.
        --> S2I     - r'C:\Program Files\Chromasens\GCT2\GenTL\s2i\GEVTLS2I.cti'
        --> Kithara - r'C:\Program Files\Chromasens\GCT2\GenTL\Kithara\tkh_tl_gev_kithara.cti'
        
        For systems with a framegrabber the .cti file is provided by the framegrabber
        manufacturer. The following is an example of an Euresys CXP12 grabber.
        
        --> Euresys CXP12 - r'C:\Program Files\Euresys\eGrabber\cti\x86_64\coaxlink.cti'
        
        Example paths valid for default installation.
        
    function : object
        Python function that is executed after the connection to the camera is estabished.
        The function input argument must be list with (opened) genicam instances.
        
    n_cam : int
        Number of cams. 1 for a single camera system
    

    Returns
    -------
    (int, type(None), str)
        Returns a tuple with (Error Code, None, 'Error Message').

    '''
    
    txt = f'  START Example: {function.__name__}  '
    print(f'{txt:#^80}\n')
    
    cam_list = []
    for i in range (n_cam):
        cam_list.append(GenICamStreamable())
         

    for i, cam in enumerate(cam_list):
        retval = cam.open_connection(tl_path, num_buffers = 15, device_number = i+1)
        if retval[0] != 0:
            return retval 
        

    #++++++++++++++ function ++++++++++++++++++

    retval_func = function(cam_list)
    
    #++++++++++++ function end ++++++++++++++++
    
    for cam in cam_list:
        retval = cam.close_connection()
        if retval[0] != 0:
            return retval 
        

    return retval_func

    

# def test_restart():
#     #open and close camera - bug for neo
#     #remove "sleep(2)" in the "close_connection" function to reproduce the bug. 
    
#     cam = GenICamBase()
    
#     tl_path = None
    
#     for i in range(3):
        
#         print(cam)
        
#         retval = cam.open_connection(tl_path, device_number = 1)
#         if retval[0] != cam._error_codes.OK[0]:
#             return retval
        
#         print(cam)
        
#         retval = cam.set_feature('Height', 2000)
#         if retval[0] != 0:
#             return retval 
        
#         #sleep(2)
#         retval = cam.close_connection()
#         if retval[0] != 0:
#             return retval 
        
        
#         print(f'run {i} completed')

        
#     return (0, None, 'OK')


if __name__ == '__main__':
    
    tl_path = None

    # tl_path = [
    #            r'C:\Program Files\Chromasens\GCT2\GenTL\s2i\GEVTLS2I.cti',
    #            r'C:\Program Files\Chromasens\GCT2\GenTL\Kithara\tkh_tl_gev_kithara.cti',
    #            r'C:\Program Files\Euresys\eGrabber\cti\x86_64\coaxlink.cti'
    #            ]
    
    
    n_cams = 1
    
    retval = main(tl_path, camera_communication, n_cams)
    print(f'{retval}\n\n')
    
    retval = main(tl_path, example_grab_images_sync, n_cams)
    print(f'{retval}\n\n')
    
    retval = main(tl_path, example_grab_images_async, n_cams)
    print(f'{retval}\n\n')
    