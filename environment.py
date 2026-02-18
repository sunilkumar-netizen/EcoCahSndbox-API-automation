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
    
    # Initialize global authentication cache for smoke/regression tests
    # This prevents repeated authentication calls in Background sections
    context.global_auth_cache = {
        'app_token': None,
        'user_token': None,
        'authenticated': False
    }
    
    # Check if running smoke or regression (@sasai) tests by checking command line args
    import sys
    cmd_args = ' '.join(sys.argv)
    is_smoke_or_regression = ('smoke' in cmd_args.lower() or 'sasai' in cmd_args.lower() or 'regression' in cmd_args.lower())
    
    if is_smoke_or_regression:
        logger.info("\n🔐 Initializing global authentication for smoke/regression (@sasai) tests...")
        try:
            # Create a temporary base_test instance for authentication
            temp_base_test = BaseTest(context.config_loader)
            api_client = temp_base_test.api_client
            config = context.config_loader
            
            # Step 1: Get app token
            logger.info("  📱 Getting app token...")
            auth_data = {
                'username': config.get('auth.username'),
                'password': config.get('auth.password'),
                'tenantId': config.get('auth.tenant_id'),
                'clientId': config.get('auth.client_id')
            }
            
            auth_response = api_client.post(
                endpoint='/bff/v1/auth/token',
                json_data=auth_data
            )
            
            if auth_response.status_code != 200:
                raise Exception(f"App token request failed with status {auth_response.status_code}")
            
            token_data = auth_response.json()
            app_token = token_data.get('accessToken')
            context.global_auth_cache['app_token'] = app_token
            logger.info(f"  ✅ App token obtained: {app_token[:50]}...")
            
            # Step 2: Request OTP
            logger.info("  📱 Requesting OTP...")
            sender_id = config.get('otp.sender_id')
            otp_request_data = {
                'senderId': sender_id,
                'countryCode': config.get('otp.country_code'),
                'purpose': config.get('otp.default_purpose'),
                'otpMode': config.get('otp.default_mode')
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {app_token}'
            }
            
            otp_response = api_client.post(
                endpoint='/bff/v2/auth/otp/request',
                json_data=otp_request_data,
                headers=headers
            )
            
            if otp_response.status_code != 200:
                raise Exception(f"OTP request failed with status {otp_response.status_code}")
            
            otp_data = otp_response.json()
            user_reference_id = otp_data.get('userReferenceId')
            logger.info(f"  ✅ OTP requested, userReferenceId: {user_reference_id}")
            
            # Step 3: PIN verification to get user token
            logger.info("  🔑 Performing PIN verification...")
            pin_verify_data = {
                'pin': config.get('pin_verify.sample_encrypted_pin'),
                'userReferenceId': user_reference_id
            }
            
            query_params = {
                'tenantId': config.get('pin_verify.default_tenant_id'),
                'azp': config.get('pin_verify.default_azp')
            }
            
            pin_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {app_token}',
                'model': config.get('pin_verify.default_device_model'),
                'deviceid': config.get('pin_verify.default_device_id')
            }
            
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            url = f"/bff/v4/auth/pin/verify?{query_string}"
            
            pin_response = api_client.post(
                endpoint=url,
                json_data=pin_verify_data,
                headers=pin_headers
            )
            
            if pin_response.status_code != 200:
                raise Exception(f"PIN verification failed with status {pin_response.status_code}")
            
            pin_data = pin_response.json()
            user_token = pin_data.get('accessToken')
            context.global_auth_cache['user_token'] = user_token
            context.global_auth_cache['authenticated'] = True
            logger.info(f"  ✅ User token obtained: {user_token[:50]}...")
            logger.info("  🎉 Global authentication completed - tokens will be reused for all scenarios\n")
            
            # Cleanup temporary instance
            temp_base_test.cleanup()
        except Exception as e:
            logger.warning(f"  ⚠️  Global authentication failed: {e}")
            logger.warning("  ℹ️  Falling back to per-scenario authentication\n")


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
    
    # Use cached authentication tokens if available (for smoke/regression tests)
    if hasattr(context, 'global_auth_cache') and context.global_auth_cache.get('authenticated'):
        logger.debug("  ♻️  Using cached authentication tokens")
        context.base_test.app_token = context.global_auth_cache.get('app_token')
        context.base_test.user_token = context.global_auth_cache.get('user_token')
        # Set the tokens in context for step definitions
        context.app_token = context.global_auth_cache.get('app_token')
        context.user_token = context.global_auth_cache.get('user_token')
    
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
