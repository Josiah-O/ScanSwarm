import asyncio
import logging
import pytest
from pathlib import Path
from .orchestrator import ScanOrchestrator
from .utils.browser import BrowserManager

pytestmark = pytest.mark.asyncio(scope="function")

@pytest.mark.asyncio
async def test_scan():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
    logger = logging.getLogger(__name__)
    
    logger.info("=== Starting Pump.fun Scanner Test ===")
    browser_manager = None
    
    try:
        # 1. Browser Setup
        logger.info("1. Initializing Browser")
        browser_manager = BrowserManager(headless=False)
        success = await browser_manager.initialize()
        assert success, "Browser initialization failed"
        
        # 2. Test basic site access
        logger.info("2. Testing site accessibility")
        page = await browser_manager.new_page()
        try:
            logger.info("Attempting to access pump.fun...")
            response = await page.goto("https://pump.fun", timeout=30000)
            logger.info(f"Response status: {response.status if response else 'No response'}")
            
            # Take screenshot of what we see (even if it's an error page)
            await browser_manager.capture_screenshot(
                page=page,
                token_address="accessibility_test",
                element_selector="body"
            )
            
            # Add delay to see what happened
            logger.info("Waiting 10 seconds to inspect site access...")
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Site access error: {str(e)}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        if browser_manager:
            await browser_manager.close()
        logger.info("✓ Test completed")

if __name__ == "__main__":
    asyncio.run(test_scan()) 