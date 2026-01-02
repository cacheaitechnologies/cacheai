"""Logging configuration for Cache AI."""

import logging

# Create logger for cacheai package
logger = logging.getLogger("cacheai")

# Do not propagate to root logger by default
# This allows external programs to configure cacheai logging independently
logger.propagate = True

# Do not add handlers by default
# External programs should configure their own handlers
# logger.addHandler(logging.NullHandler())


def get_logger(name: str = "cacheai") -> logging.Logger:
    """
    Get a logger instance for cacheai.
    
    Args:
        name: Logger name (default: "cacheai")
        
    Returns:
        Logger instance
        
    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.DEBUG)
        >>> from cacheai.logging import get_logger
        >>> logger = get_logger()
        >>> logger.info("Cache AI initialized")
    """
    return logging.getLogger(name)
