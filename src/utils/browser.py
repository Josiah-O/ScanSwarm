from playwright.async_api import async_playwright, Browser, Page
from ..config import Config
import logging
import base64
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self, headless=True, proxy=None):
        self.browser = None
        self.config = Config()
        self.context = None
        self.headless = headless
        self.proxy = proxy
        
    async def initialize(self):
        """Initialize browser instance"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox']
            )
            
            # Create context with existing config
            context_options = {
                "viewport": self.config.VIEWPORT_SIZE,
                "user_agent": self.config.USER_AGENT,
            }
            
            # Add proxy only if provided
            if self.proxy:
                context_options["proxy"] = self.proxy
                
            self.context = await self.browser.new_context(**context_options)
            logger.info("Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            return False

    async def new_page(self) -> Page:
        """Create new page with error handling"""
        if not self.context:
            success = await self.initialize()
            if not success:
                return None
        return await self.context.new_page()

    async def capture_screenshot(self, page: Page, token_address: str, element_selector: str = None) -> str:
        """Capture screenshot of full page or specific element"""
        try:
            screenshot_path = self.config.SCREENSHOT_DIR / f"{token_address}_{asyncio.get_event_loop().time()}.png"
            Path(screenshot_path.parent).mkdir(parents=True, exist_ok=True)
            
            if element_selector:
                element = await page.wait_for_selector(element_selector)
                await element.screenshot(path=screenshot_path)
            else:
                await page.screenshot(path=screenshot_path, full_page=True)

            # Convert to base64 for storage/transmission
            with open(screenshot_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            return encoded_string

        except Exception as e:
            logger.error(f"Screenshot capture failed for {token_address}: {str(e)}")
            return None

    async def close(self):
        """Clean up browser resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Failed to close browser: {str(e)}")
