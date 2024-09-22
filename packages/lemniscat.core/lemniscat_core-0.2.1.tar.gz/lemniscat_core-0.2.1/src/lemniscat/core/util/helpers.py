import logging
import os
import re
import sys
from logging import Logger, StreamHandler, DEBUG
from typing import Union, Optional
import yaml

from lemniscat.core.model import VariableValue

_REGEX_CAPTURE_VARIABLE = r"(?:\${{(?P<var>[^}]+)}})"

class Interpreter:
    _logger: Logger
    _variables: dict
    
    def __init__(self, logger: Logger, variables: dict) -> None:
        self._logger = logger
        self._variables = variables
    
    def __interpretDict(self, value: dict, type: str = "variable") -> VariableValue:
        isSensitive = False
        for key in value:
            if(isinstance(value[key], str)):
                tmp = self.__intepretString(value[key], type)
            elif(isinstance(value[key], dict)):
                tmp = self.__interpretDict(value[key], type)
            elif(isinstance(value[key], list)):
                tmp = self.__interpretList(value[key], type)
            else:
                tmp = VariableValue(value[key])
            if(tmp.sensitive):
                isSensitive = True
            value[key] = tmp.value
        return VariableValue(value, isSensitive)

    def __interpretList(self, value: list, type: str = "variable") -> VariableValue:
        isSensitive = False
        for val in value:
            if(isinstance(val, str)):
                tmp = self.__intepretString(val, type)
            elif(isinstance(val, dict)):
                tmp = self.__interpretDict(val, type)
            elif(isinstance(val, list)):
                tmp = self.__interpretList(val, type)
            else:
                tmp = VariableValue(val)
            if(tmp.sensitive):
                isSensitive = True
            val = tmp.value
        return VariableValue(value, isSensitive)    

    def __intepretString(self, value: str, type: str = "variable") -> VariableValue:
        isSensitive = False
        matches = re.findall(_REGEX_CAPTURE_VARIABLE, value)
        if(len(matches) > 0):
            for match in matches:
                var = str.strip(match)
                if(var in self._variables):
                    if(self._variables[var].sensitive):
                        isSensitive = True
                    if(value == f'${{{{{match}}}}}'):
                        value = self._variables[var].value
                    else:
                        value = value.replace(f'${{{{{match}}}}}', self._variables[var].value)
                    self._logger.debug(f"Interpreting {type}: {var} -> {self._variables[var]}")
        return VariableValue(value, isSensitive)        
                           
    def __interpret(self, variable: VariableValue, type: str = "variable") -> VariableValue:
        isSensitive = variable.sensitive
        if(variable is None):
            return None
        if(isinstance(variable.value, str)):
            tmp = self.__intepretString(variable.value, type)
        elif(isinstance(variable.value, dict)):
            tmp = self.__interpretDict(variable.value, type)
        elif(isinstance(variable.value, list)):
            tmp = self.__interpretList(variable.value, type)
        else:
            tmp = variable
        if(tmp.sensitive):
            isSensitive = True
        variable.value = tmp.value
        return VariableValue(variable.value, isSensitive)    
        
    def interpret(self) -> None:
        for key in self._variables:
            self._variables[key] = self.__interpret(self._variables[key])
            
    def interpretParameters(self, parameters: dict) -> dict:
        for key in parameters:
            parameters[key] = self.__interpret(VariableValue(parameters[key]), "parameter").value
        return parameters
            
    def interpretDict(self, data: dict, type: str="undefined") -> dict:
        return self.__interpretDict(data, type).value
            
    def interpretString(self, data: str, type: str="undefined") -> str:
        return self.__intepretString(data, type).value
            
    def interpretList(self, data: list, type: str="undefined") -> list:
        return self.__interpretList(data, type).value
    
class FileSystem:

    @staticmethod
    def __get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '../..')

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'settings')

    @staticmethod
    def get_plugins_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'plugins')

    @staticmethod
    def load_configuration(name: str = 'configuration.yaml', config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
    
    @staticmethod
    def load_configuration_path(path: str = None) -> dict:
        with open(path) as file:
            input_data = yaml.safe_load(file)
        return input_data

class CustomFormatter(logging.Formatter):
    purple = "\x1b[35;20m"
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    grey = "\x1b[38;20m"
    orange = "\x1b[33;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _FORMATTER = "%(asctime)s [%(name)s][%(levelname)s] %(message)s"
    _FORMATTER_PLUGIN = "%(asctime)s    [%(name)s][%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: blue + _FORMATTER + reset,
        logging.INFO: grey + _FORMATTER + reset,
        logging.WARNING: orange + _FORMATTER + reset,
        logging.ERROR: red + _FORMATTER + reset,
        logging.CRITICAL: bold_red + _FORMATTER + reset,
        70: green + _FORMATTER + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if("plugin." in record.name and (record.levelno == logging.INFO or record.levelno == logging.DEBUG)):
            log_fmt = self.purple + self._FORMATTER_PLUGIN + self.reset
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LogUtil(Logger):
    
    def __init__(
            self,
            name: str,
            level: Union[int, str] = DEBUG,
            *args,
            **kwargs
    ) -> None:
        super().__init__(name, level)
        logging.SUCCESS = 70
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        self.addHandler(self.__get_stream_handler())

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        return handler    
    
    @staticmethod
    def create(log_level: str = 'DEBUG') -> Logger:
        # create logger with 'spam_application'
        logging.setLoggerClass(LogUtil)
        logger = logging.getLogger("lemniscat")
        logger.setLevel(log_level)
        return logger