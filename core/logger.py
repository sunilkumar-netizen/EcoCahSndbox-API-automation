"""
Logger Module
Provides centralized logging configuration for the framework.
Supports console and file logging with color-coded output.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
import colorlog


class Logger:
    """
    Singleton Logger class for centralized logging.
    Provides colored console output and file logging.
    """
    
    _loggers = {}
    _log_dir = None
    
    @classmethod
    def setup_logging(cls, log_level: str = 'INFO', 
                     console: bool = True, 
                     file_logging: bool = True,
                     log_file_path: str = None) -> None:
        """
        Setup global logging configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console: Enable console logging
            file_logging: Enable file logging
            log_file_path: Custom log file path
        """
        # Create logs directory
        if file_logging:
            cls._log_dir = Path(log_file_path).parent if log_file_path else Path('logs')
            cls._log_dir.mkdir(exist_ok=True)
        
        # Set root logger level
        logging.root.setLevel(getattr(logging, log_level.upper()))
    
    @classmethod
    def get_logger(cls, name: str, log_level: str = 'INFO') -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name (usually __name__)
            log_level: Logging level
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        logger.propagate = False
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        if cls._log_dir:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = cls._log_dir / f'automation_{timestamp}.log'
            
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """
        Get current log file path.
        
        Returns:
            Path to current log file
        """
        if cls._log_dir:
            log_files = sorted(cls._log_dir.glob('automation_*.log'))
            if log_files:
                return str(log_files[-1])
        return None
