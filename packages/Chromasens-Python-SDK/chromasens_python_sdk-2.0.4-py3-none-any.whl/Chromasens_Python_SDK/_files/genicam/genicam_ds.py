
"""
This module contains defines and ctypes.Structures for the genicam module.
This file was mainly automatically generated with ctypesgen and GCC and manually cleaned from artifacts.
Some parts were inherited from gige_ds.
"""
# Author: Nicolas Luhn / Chromasens GmbH
# Date: 26.02.2021

import ctypes

# ------------------------------------------------------------------------------
# Manually defined (inherited from gige_ds)
# ------------------------------------------------------------------------------

# feature
MAX_FEATURE_VALUE_LENGTH = 300
MAX_FEATURE_ENUM_NAMES_LENGTH = 2000
MAX_FEATURE = 500

CSI_SCAN_IMG_NUMBER = 0x1
CSI_SCAN_IMG_MINUTES = 0x2
CSI_SCAN_IMG_MOVING_TEST_RAMP = 0x4

# compatibility with customer version
MAX_CHANNEL = 4

(CHECK_IF_ALL_IMG_VALID, CHECK_IF_EXPECTED_NUMBER_OF_IMG_VALID, RETURN_VALID_IMG_NR) = (0,1,2)





class IMG_DATA_STRUCT(ctypes.Structure): 
    """
    IGNORE_STRUCT_SIZE_TEST
    
    width: Linkable Value = True
    height: Linkable Value = True
    """

    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("scanTimeout", ctypes.c_int)]

    def __init__(self):
        self.width = 15360
        self.height = 2000
        self.scanTimeout = 2000



class IMG_PARAM_STRUCT(ctypes.Structure): 
    """
    IGNORE_STRUCT_SIZE_TEST
    
    width: Linkable Value = True
    height: Linkable Value = True
    """

    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("scanTimeout", ctypes.c_int)]

    def __init__(self):
        self.width = 15360
        self.height = 2000
        self.scanTimeout = 2000
        
        
(UserSet1, UserSet2, UserSet3, UserSet4, UserSet5, UserSet6, UserSet7, 
 UserSet8, GammaLUT, DSNULUT1, DSNULUT2, PRNULUT1, PRNULUT2,  Application, Bitstream, 
 Xml, PackageDescriptionFile) = ('UserSet1',
' UserSet2', 'UserSet3', 'UserSet4', 'UserSet5', 'UserSet6', 'UserSet7', 
 'UserSet8', 'GammaLUT', 'DSNULUT1', 'DSNULUT2', 'PRNULUT1', 'PRNULUT2', 'Application', 'Bitstream', 
 'Xml', 'PackageDescriptionFile')

# ------------------------------------------------------------------------------
# End manually defined
# ------------------------------------------------------------------------------

CSI_ACQUISITION_SINGLE_FRAME = 0x00000001
CSI_ACQUISITION_CONTINUOUS = 0xFFFFFFFF

csiHandle = ctypes.c_uint64# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 25

enum_csiPixelFormat = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_UNKNOWN = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO8 = 17301505# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO10 = 17825795# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO10_PACKED = 17432646# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO12 = 17825797# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO12_PACKED = 17563719# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_MONO16 = 17825799# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_RGB8 = 35127316# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_RGB10_PACKED = 35651613# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_RGBA8 = 35651606# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_BGR8 = 35127317# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

CSI_PIX_FORMAT_RGB16 = 36700211

CSI_PIX_FORMAT_BAYER_RG8 = 'not supported from csi.dll 1' # 30.07.2021

CSI_PIX_FORMAT_BAYER_RG10 = 'not supported from csi.dll 2' # 30.07.2021

CSI_PIX_FORMAT_BAYER_RG12 = 'not supported from csi.dll 3' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GR8 = 'not supported from csi.dll 4' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GR10 = 'not supported from csi.dll 5' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GR12 = 'not supported from csi.dll 6' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GB8 = 'not supported from csi.dll 7' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GB10 = 'not supported from csi.dll 8' # 30.07.2021

CSI_PIX_FORMAT_BAYER_GB12 = 'not supported from csi.dll 9' # 30.07.2021

CSI_PIX_FORMAT_BAYER_BG8 = 'not supported from csi.dll 10' # 30.07.2021

CSI_PIX_FORMAT_BAYER_BG10 = 'not supported from csi.dll 11' # 30.07.2021

CSI_PIX_FORMAT_BAYER_BG12 = 'not supported from csi.dll 12' # 30.07.2021

CSI_PIX_FORMAT_RGB10 = 36700184

CSI_PIX_FORMAT_RGB12 = 36700186

CSI_PIX_FORMAT_RGBA10 = 37748831

CSI_PIX_FORMAT_RGBA12 = 37748833

csiPixelFormat = enum_csiPixelFormat# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 47

enum_csiDeviceAccessMode = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

CSI_DEV_MODE_UNKNOWN = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

CSI_DEV_MODE_NONE = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

CSI_DEV_MODE_EXCLUSIVE = (CSI_DEV_MODE_NONE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

CSI_DEV_MODE_READ = (CSI_DEV_MODE_EXCLUSIVE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

CSI_DEV_MODE_CONTROL = (CSI_DEV_MODE_READ + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

csiDeviceAccessMode = enum_csiDeviceAccessMode# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 56

enum_csiDeviceAccessStatus = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_UNKNOWN = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_READWRITE = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_READONLY = 2# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_NOACCESS = 3# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_BUSY = 4# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_OPEN_READWRITE = 5# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

CSI_DEV_ACCESS_STATUS_OPEN_READ = 6# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

csiDeviceAccessStatus = enum_csiDeviceAccessStatus# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 67

enum_csiFeatureType = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_UNKNOWN_TYPE = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_BOOLEAN_TYPE = (CSI_UNKNOWN_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_INT_TYPE = (CSI_BOOLEAN_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_FLOAT_TYPE = (CSI_INT_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_STRING_TYPE = (CSI_FLOAT_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_ENUMERATION_TYPE = (CSI_STRING_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_ENUMENTRY_TYPE = (CSI_ENUMERATION_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_CATEGORY = (CSI_ENUMENTRY_TYPE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_COMMAND = (CSI_CATEGORY + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_REGISTER = (CSI_COMMAND + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

CSI_PORT = (CSI_REGISTER + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

csiFeatureType = enum_csiFeatureType# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 81

enum_csiAccessMode = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

CSI_ACCESS_UNKNOWN = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

CSI_ACCESS_NOT_AVAILABLE = (CSI_ACCESS_UNKNOWN + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

CSI_ACCESS_READ_ONLY = (CSI_ACCESS_NOT_AVAILABLE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

CSI_ACCESS_READ_WRITE = (CSI_ACCESS_READ_ONLY + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

CSI_ACCESS_WRITE_ONLY = (CSI_ACCESS_READ_WRITE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

csiAccessMode = enum_csiAccessMode# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 90

enum_csiFeatureVisibility = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

CSI_VISIBILITY_BEGINNER = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

CSI_VISIBILITY_EXPERT = (CSI_VISIBILITY_BEGINNER + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

CSI_VISIBILITY_GURU = (CSI_VISIBILITY_EXPERT + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

CSI_VISIBILITY_DEVELOPER = (CSI_VISIBILITY_GURU + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

CSI_VISIBILITY_INVISIBLE = (CSI_VISIBILITY_DEVELOPER + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

csiFeatureVisibility = enum_csiFeatureVisibility# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 99

enum_csiModuleLevel = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_UNKNOWN_MODULE = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_TRANSPORTLAYER_MODULE = (CSI_UNKNOWN_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_INTERFACE_MODULE = (CSI_TRANSPORTLAYER_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_DEVICE_MODULE = (CSI_INTERFACE_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_LOCAL_DEVICE_MODULE = (CSI_DEVICE_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_STREAM_MODULE = (CSI_LOCAL_DEVICE_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

CSI_BUFFER_MODULE = (CSI_STREAM_MODULE + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

csiModuleLevel = enum_csiModuleLevel# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 110

enum_csiDisplayNotation = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 117

CSI_NOTATION_AUTOMATIC = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 117

CSI_NOTATION_FIXED = (CSI_NOTATION_AUTOMATIC + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 117

CSI_NOTATION_SCIENTIFIC = (CSI_NOTATION_FIXED + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 117

csiDisplayNotation = enum_csiDisplayNotation# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 117

enum_csiRepresentation = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_LINEAR = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_LOGARITHMIC = (CSI_REPRESENTATION_LINEAR + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_BOOLEAN = (CSI_REPRESENTATION_LOGARITHMIC + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_PURENUMBER = (CSI_REPRESENTATION_BOOLEAN + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_HEX = (CSI_REPRESENTATION_PURENUMBER + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_IP = (CSI_REPRESENTATION_HEX + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_MAC = (CSI_REPRESENTATION_IP + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

CSI_REPRESENTATION_UNDEFINED = (CSI_REPRESENTATION_MAC + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

csiRepresentation = enum_csiRepresentation# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 129

enum_csiLogLevel = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

CSI_LOGLEVEL_NONE = 0

CSI_LOGLEVEL_ERROR = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

CSI_LOGLEVEL_WARN = 2# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

CSI_LOGLEVEL_INFO = 4# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

CSI_LOGLEVEL_DEBUG = 8# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

CSI_LOGLEVEL_TRACE = 16# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

csiLogLevel = enum_csiLogLevel# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 176

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 167
class csiFeatureParameter(ctypes.Structure):
    """"
    """
    pass

csiFeatureParameter._fields_ = [
    ('type', csiFeatureType),
    ('visibility', csiFeatureVisibility),
    ('access', csiAccessMode),
    ('displayNotation', csiDisplayNotation),
    ('representation', csiRepresentation),
    ('displayPrecision', ctypes.c_char),
    ('valueInt', ctypes.c_int64),
    ('incrementInt', ctypes.c_int64),
    ('minimumInt', ctypes.c_int64),
    ('maximumInt', ctypes.c_int64),
    ('validValueSetInt', ctypes.c_int64 * int(512)),
    ('validValueSetSizeInt', ctypes.c_size_t),
    ('valueFlt', ctypes.c_double),
    ('incrementFlt', ctypes.c_double),
    ('minimumFlt', ctypes.c_double),
    ('maximumFlt', ctypes.c_double),
    ('valueStr', ctypes.c_char * int(512)),
    ('maximumStringLength', ctypes.c_size_t),
    ('level', ctypes.c_int64),
    ('enumCounter', ctypes.c_uint32),
    ('enumIndex', ctypes.c_char),
    ('displayName', ctypes.c_char * int(512)),
    ('name', ctypes.c_char * int(512)),
    ('tooltip', ctypes.c_char * int(512)),
    ('valueUnit', ctypes.c_char * int(512)),
    ('featureRegLength', ctypes.c_size_t),
    ('featureRegAddress', ctypes.c_int64),
    ('isFeature', ctypes.c_bool),
    ('isLittleEndian', ctypes.c_bool),
]

# ------------------------------------------------------------------------------
# Manually defined (inherited from gige_ds)
# ------------------------------------------------------------------------------
SUPPORTED_PIX_FORMATS = [CSI_PIX_FORMAT_MONO8, CSI_PIX_FORMAT_MONO10, CSI_PIX_FORMAT_MONO12,
                         CSI_PIX_FORMAT_MONO16, CSI_PIX_FORMAT_MONO10_PACKED, CSI_PIX_FORMAT_MONO12_PACKED,
                         CSI_PIX_FORMAT_RGB8, CSI_PIX_FORMAT_RGB10, CSI_PIX_FORMAT_RGB12, CSI_PIX_FORMAT_RGB16, CSI_PIX_FORMAT_RGBA8,
                         CSI_PIX_FORMAT_BGR8, CSI_PIX_FORMAT_RGB10_PACKED, CSI_PIX_FORMAT_RGBA10, CSI_PIX_FORMAT_RGBA12]

SWAP_RED_BLUE_PIX_FORMATS = [CSI_PIX_FORMAT_RGB8, CSI_PIX_FORMAT_RGB10, CSI_PIX_FORMAT_RGB12,
                             CSI_PIX_FORMAT_RGB16, CSI_PIX_FORMAT_RGBA8,
                             CSI_PIX_FORMAT_RGB10_PACKED, CSI_PIX_FORMAT_RGBA10,
                             CSI_PIX_FORMAT_RGBA12]

BAYER_8_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_RG8, CSI_PIX_FORMAT_BAYER_GR8,
                       CSI_PIX_FORMAT_BAYER_GB8, CSI_PIX_FORMAT_BAYER_BG8]

BAYER_10_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_RG10, CSI_PIX_FORMAT_BAYER_GR10,
                        CSI_PIX_FORMAT_BAYER_GB10, CSI_PIX_FORMAT_BAYER_BG10]

BAYER_12_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_RG12, CSI_PIX_FORMAT_BAYER_GR12,
                        CSI_PIX_FORMAT_BAYER_GB12, CSI_PIX_FORMAT_BAYER_BG12]

BAYER_PIX_FORMATS = BAYER_8_PIX_FORMATS + BAYER_10_PIX_FORMATS + BAYER_12_PIX_FORMATS

BAYER_RG_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_RG8, CSI_PIX_FORMAT_BAYER_RG10, CSI_PIX_FORMAT_BAYER_RG12]

BAYER_GR_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_GR8, CSI_PIX_FORMAT_BAYER_GR10, CSI_PIX_FORMAT_BAYER_GR12]

BAYER_GB_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_GB8, CSI_PIX_FORMAT_BAYER_GB10, CSI_PIX_FORMAT_BAYER_GB12]

BAYER_BG_PIX_FORMATS = [CSI_PIX_FORMAT_BAYER_BG8, CSI_PIX_FORMAT_BAYER_BG10, CSI_PIX_FORMAT_BAYER_BG12]

class FEATURE_PARAM_LIST_STRUCT(ctypes.Structure):
    """
    IGNORE_STRUCT_SIZE_TEST
    """
    _fields_ = [("count", ctypes.c_int),
                ("maxLevel", ctypes.c_ubyte),
                ("feature", ctypes.POINTER(csiFeatureParameter))]

    def __init__(self):
        ctypes.memset(ctypes.addressof(self), 0, ctypes.sizeof(self))

class DOWNLOAD_FILE_STRUCT(ctypes.Structure):
    """
    IGNORE_STRUCT_SIZE_TEST
    GUI Arrangement = [file_type timeout file_name, userDefined S]
    """
    _fields_ = [("file_name", ctypes.c_char_p),
                ("file_type", ctypes.c_char_p),
                ("timeout", ctypes.c_int),
                ("userDefined", ctypes.c_bool)]

    def __init__(self):
        ctypes.memset(ctypes.addressof(self), 0, ctypes.sizeof(self))
        self.timeout = 90000




# ------------------------------------------------------------------------------
# End manually defined
# ------------------------------------------------------------------------------


enum_csiErr = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiSuccess = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNotInitialized = (-100)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiInvalidState = (-101)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNotOpened = (-102)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNoImageDataAvailable = (-103)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNotFound = (-104)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiInvalidParameter = (-105)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNotAvailable = (-106)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiFunctionNotAvailable = (-107)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiTimeout = (-108)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiAborted = (-109)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiFileOperationFailure = (-110)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiFileOperationFatalError = (-111)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNoAccess = (-112)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiWrongBufferSize = (-113)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiInvalidBuffer = (-114)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiResourceInUse = (-115)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiNotImplemented = (-116)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiInvalidHandle = (-117)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiIOError = (-118)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiParsingError = (-119)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiInvalidValue = (-120)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiResourceExhausted = (-121)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiOutOfMemory = (-122)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiBusy = (-123)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiUnknown = (-200)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

csiCustomErr = (-10000)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207




csiErr = enum_csiErr# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 207

enum_csiEventType = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_NEWIMAGEDATA = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_ERROR = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_MODULE = 2# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_FEATURE_INVALIDATE = 3# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_FEATURE_CHANGE = 4# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_REMOTE_DEVICE = 5# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

CSI_EVT_CUSTOM = 4096# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

csiEventType = enum_csiEventType# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 218

enum_csiAcquisitionMode = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 224

CSI_ACQUISITION_SINGLE_FRAME = 1# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 224

CSI_ACQUISITION_CONTINUOUS = 4294967295# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 224

csiAcquisitionMode = enum_csiAcquisitionMode# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 224

enum_csiMemTransferStatus = ctypes.c_int# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiTransferStatusInit = 0# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiTransferStatusInProgress = (csiTransferStatusInit + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiTransferStatusFinishSucess = (csiTransferStatusInProgress + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiTransferStatusFinishError = (csiTransferStatusFinishSucess + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiTransferStatusCancelOnError = (csiTransferStatusFinishError + 1)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

csiMemTransferStatus = enum_csiMemTransferStatus# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 233

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 243
class csiMemTransferInfo(ctypes.Structure):
    """
    """
    pass

csiMemTransferInfo._fields_ = [
    ('device', csiHandle),
    ('totalBytesToTransfer', ctypes.c_size_t),
    ('bytesTransferred', ctypes.c_size_t),
    ('status', csiMemTransferStatus),
    ('errorCode', csiErr),
    ('progressText', ctypes.c_char_p),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 245
#class struct_csiEventUserData(ctypes.c_void_p):
#    pass

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 246
#class struct_csiMemTransferUserData(ctypes.c_void_p):
#    pass

class csiTLProducerInfos(ctypes.Structure):
    """
    """
    pass

csiTLProducerInfos._fields_ = [
    ('transportLayerName', ctypes.c_char * int(512)),
    ('transportLayerDisplayName', ctypes.c_char * int(512)),
    ('transportLayerType', ctypes.c_char * int(512)),
    ('transportLayerPath', ctypes.c_char * int(512)),
    ('transportLayerID', ctypes.c_char * int(512)),
    ('pathSizeInBytes', ctypes.c_size_t),
]


class csiTLInterfaceInfo(ctypes.Structure):
    """
    """
    pass

csiTLInterfaceInfo._fields_ = [
    ('interfaceDescription', ctypes.c_char * int(512)),
    ('interfaceID', ctypes.c_char * int(512)),
    ('tlProducerInfos', csiTLProducerInfos),
]



class csiTLInterfaceDiscoveryInfo(ctypes.Structure):
    """
    """
    pass

csiTLInterfaceDiscoveryInfo._fields_ = [
    ('numInterfaces', ctypes.c_uint32),
    ('progress', ctypes.c_double),
    ('discoveryRunning', ctypes.c_bool),
    ('interfaces', csiTLInterfaceInfo),
]




# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 255
class csiTLProducerInfos(ctypes.Structure):
    """
    """
    pass

csiTLProducerInfos._fields_ = [
    ('transportLayerName', ctypes.c_char * int(512)),
    ('transportLayerDisplayName', ctypes.c_char * int(512)),
    ('transportLayerType', ctypes.c_char * int(512)),
    ('transportLayerPath', ctypes.c_char * int(512)),
    ('transportLayerID', ctypes.c_char * int(512)),
    ('pathSizeInBytes', ctypes.c_size_t),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 272
class csiDeviceInfo(ctypes.Structure):
    """
    """
    pass

csiDeviceInfo._fields_ = [
    ('deviceIdentifier', ctypes.c_char * int(512)),
    ('name', ctypes.c_char * int(512)),
    ('model', ctypes.c_char * int(512)),
    ('vendor', ctypes.c_char * int(512)),
    ('serialNumber', ctypes.c_char * int(512)),
    ('interfaceDescription', ctypes.c_char * int(512)),
    ('interfaceID', ctypes.c_char * int(512)),
    ('userName', ctypes.c_char * int(512)),
    ('version', ctypes.c_char * int(512)),
    ('cameraSwPackageIsConsistent', ctypes.c_int64),
    ('tlProducerInfos', csiTLProducerInfos),
    ('accessStatus', csiDeviceAccessStatus),
    ('timestampFrequency', ctypes.c_uint64),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 280
class csiDiscoveryInfo(ctypes.Structure):
    """
    """
    pass

csiDiscoveryInfo._fields_ = [
    ('numDevices', ctypes.c_uint32),
    ('progress', ctypes.c_double),
    ('discoveryRunning', ctypes.c_bool),
    ('devices', csiDeviceInfo * int(16)),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 287
class csiDataStreamInfo(ctypes.Structure):
    """
    """
    pass

csiDataStreamInfo._fields_ = [
    ('identifier', ctypes.c_char * int(512)),
    ('displayName', ctypes.c_char * int(512)),
    ('index', ctypes.c_uint32),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 297
class csiImageInfo(ctypes.Structure):
    """
    """
    pass

csiImageInfo._fields_ = [
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
    ('linePitch', ctypes.c_uint32),
    ('numChannels', ctypes.c_uint32),
    ('format', csiPixelFormat),
]


# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 309
class csiEventData(ctypes.Structure):
    """
    """
    pass

csiEventData._fields_ = [
    ('type', csiEventType),
    ('sender', csiHandle),
    ('senderType', csiModuleLevel),
    ('eventData', ctypes.c_char_p),
    ('eventDataSizeBytes', ctypes.c_size_t),
    ('eventValue', ctypes.c_char_p),
    ('eventValueSizeBytes', ctypes.c_size_t),
    ('eventIdentifier', ctypes.c_uint64),
]

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 327
class csiNewBufferEventData(ctypes.Structure):
    """
    """
    pass

csiNewBufferEventData._fields_ = [
    ('type', csiEventType),
    ('sender', csiHandle),
    ('senderType', csiModuleLevel),
    ('tl_rawEventData', ctypes.c_char_p),
    ('tl_rawEventDataSizeBytes', ctypes.c_size_t),
    ('eventValue', ctypes.POINTER(ctypes.c_ubyte)),
    ('eventValueSizeBytes', ctypes.c_size_t),
    ('eventIdentifier', ctypes.c_uint64),
    ('bufferHandle', csiHandle),
    ('imageNr', ctypes.c_uint64),
    ('bufferIdentifier', ctypes.c_uint64),
    ('timestampMS', ctypes.c_uint64),
    ('timestampRaw', ctypes.c_uint64),
    ('imageInfo', csiImageInfo),
]



# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 336
class csiAcquistionStatistics(ctypes.Structure):
    """
    """
    pass

csiAcquistionStatistics._fields_ = [
    ('framesUnderrun', ctypes.c_int64),
    ('framesDropped', ctypes.c_int64),
    ('framesAcquired', ctypes.c_int64),
    ('networkPacketsOK', ctypes.c_int64),
    ('networkPacketsError', ctypes.c_int64),
]




CB_OBJECT = ctypes.c_void_p # C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 338

CB_FEATURE_INVALIDATED_PFN = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 339

csiDiscoveryInfoCallbackFunc = ctypes.CFUNCTYPE(None, ctypes.POINTER(csiDiscoveryInfo))# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 341


CSI_INFO_STRING_BUFFER_SIZE = 512

CSI_INFO_INT_BUFFER_SIZE = 512

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 21
CSI_INFO_BUFFER_SIZE = 512

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 22
CSI_DISCOVERY_INFO_DEVICE_COUNT = 16

CSI_TL_INTERFACE_COUNT = 16

# C:\\Projects\\CATE\\Branch\\genicam\\model\\camera\\dll\\cs_genicam\\bin\\csi.h: 23
CSI_INFITIE_TIME = 4294967295




CSI_MODULE_LIST = [CSI_TRANSPORTLAYER_MODULE, CSI_INTERFACE_MODULE, 
                  CSI_DEVICE_MODULE, CSI_LOCAL_DEVICE_MODULE,
                  CSI_STREAM_MODULE, CSI_BUFFER_MODULE]


