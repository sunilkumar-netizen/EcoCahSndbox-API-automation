"""
Behave Environment Configuration
Setup and teardown hooks for test execution.
"""

import os
from core.base_test import BaseTest
from core.logger import Logger
from utils.config_loader import ConfigLoader
import allure


def before_all(context):
    """
    Executed once before all tests.
    Setup global configuration and logging.
    """
    # Get environment from command line: behave -D env=qa
    environment = context.config.userdata.get('env', 'qa')
    
    # Load configuration
    context.config_loader = ConfigLoader(environment)
    
    # Setup logging
    log_level = context.config_loader.get('logging.level', 'INFO')
    console_logging = context.config_loader.get('logging.console', True)
    file_logging = context.config_loader.get('logging.file', True)
    log_file_path = context.config_loader.get('logging.file_path', 'logs/automation.log')
    
    Logger.setup_logging(
        log_level=log_level,
        console=console_logging,
        file_logging=file_logging,
        log_file_path=log_file_path
    )
    
    logger = Logger.get_logger(__name__)
    logger.info("="*80)
    logger.info(f"🚀 Starting Test Execution - Environment: {environment.upper()}")
    logger.info(f"📍 Base URL: {context.config_loader.get('api.base_url')}")
    logger.info("="*80)


def before_feature(context, feature):
    """
    Executed before each feature.
    """
    logger = Logger.get_logger(__name__)
    logger.info(f"\n{'='*80}")
    logger.info(f"📋 Feature: {feature.name}")
    logger.info(f"{'='*80}\n")


def before_scenario(context, scenario):
    """
    Executed before each scenario.
    Initialize test context and API client.
    """
    logger = Logger.get_logger(__name__)
    logger.info(f"\n{'─'*80}")
    logger.info(f"🧪 Scenario: {scenario.name}")
    logger.info(f"{'─'*80}")
    
    # Initialize base test for each scenario
    context.base_test = BaseTest(context.config_loader)
    
    # Add scenario tags to Allure report
    if hasattr(scenario, 'tags'):
        for tag in scenario.tags:
            allure.dynamic.tag(tag)


def after_scenario(context, scenario):
    """
    Executed after each scenario.
    Cleanup resources and log results.
    """
    logger = Logger.get_logger(__name__)
    
    # Cleanup
    if hasattr(context, 'base_test'):
        context.base_test.cleanup()
    
    # Log scenario result
    if scenario.status == 'passed':
        logger.info(f"✅ Scenario PASSED: {scenario.name}")
    elif scenario.status == 'failed':
        logger.error(f"❌ Scenario FAILED: {scenario.name}")
        
        # Attach response to Allure report if available
        if hasattr(context, 'response'):
            try:
                allure.attach(
                    context.response.text,
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON
                )
            except:
                pass
    elif scenario.status == 'skipped':
        logger.warning(f"⏭️  Scenario SKIPPED: {scenario.name}")
    
    logger.info(f"{'─'*80}\n")


def after_feature(context, feature):
    """
    Executed after each feature.
    """
    logger = Logger.get_logger(__name__)
    logger.info(f"\n{'='*80}")
    logger.info(f"✅ Feature Completed: {feature.name}")
    logger.info(f"{'='*80}\n")


def after_all(context):
    """
    Executed once after all tests.
    Final cleanup and reporting.
    """
    logger = Logger.get_logger(__name__)
    logger.info("\n" + "="*80)
    logger.info("🏁 Test Execution Completed")
    logger.info("="*80)
    
    # Log summary statistics
    if hasattr(context, '_runner'):
        logger.info(f"📊 Total Features: {len(context._runner.features)}")
    
    log_file = Logger.get_log_file_path()
    if log_file:
        logger.info(f"📄 Log File: {log_file}")


def before_step(context, step):
    """
    Executed before each step (optional).
    """
    pass


def after_step(context, step):
    """
    Executed after each step.
    Log step results for better debugging.
    """
    logger = Logger.get_logger(__name__)
    
    if step.status == 'passed':
        logger.debug(f"  ✓ {step.keyword} {step.name}")
    elif step.status == 'failed':
        logger.error(f"  ✗ {step.keyword} {step.name}")
        logger.error(f"    Error: {step.exception}")
    elif step.status == 'undefined':
        logger.warning(f"  ? {step.keyword} {step.name} (undefined)")
