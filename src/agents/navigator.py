from swarms import Agent
import logging

class NavigatorAgent(Agent):
    def __init__(self, browser_manager):
        super().__init__(
            agent_name="Navigator",
            system_prompt="""You are a web navigation agent that:
            1. Navigates to pump.fun
            2. Captures token charts and data
            3. Identifies new listings
            4. Monitors token movements""",
            model_name="gpt-4"
        )
        self.browser_manager = browser_manager
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://pump.fun"

    async def run(self, token_address: str):
        """Navigate and capture token data from pump.fun"""
        self.logger.info(f"Starting navigation for token: {token_address}")
        page = await self.browser_manager.new_page()
        
        try:
            # Build and navigate to URL
            token_url = f"{self.base_url}/token/{token_address}"
            self.logger.info(f"Navigating to: {token_url}")
            
            # Navigate with longer timeout
            await page.goto(token_url, timeout=30000)
            self.logger.info("Page loaded successfully")
            
            # Wait for chart with explicit logging
            self.logger.info("Waiting for chart container...")
            await page.wait_for_selector('.chart-container', timeout=10000)
            self.logger.info("Chart container found")
            
            # Take screenshot
            self.logger.info("Capturing screenshot...")
            screenshot = await self.browser_manager.capture_screenshot(
                page=page,
                token_address=token_address,
                element_selector='.chart-container'
            )
            
            if screenshot:
                self.logger.info("Screenshot captured successfully")
                return {
                    "type": "navigation",
                    "data": {
                        "url": token_url,
                        "screenshot": screenshot,
                        "token_address": token_address
                    }
                }
            else:
                self.logger.error("Screenshot capture failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Navigation failed: {str(e)}")
            return None
        finally:
            await page.close()
