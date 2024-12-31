import asyncio
import logging
from pathlib import Path
from src.agents.navigator import NavigatorAgent
from src.agents.chart_analyzer import ChartAnalyzerAgent
from src.utils.browser import BrowserManager
from src.config import Config

def setup_logging():
    """Setup logging configuration"""
    config = Config()
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT,
        filename=config.LOG_FILE
    )

async def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting SwarmScan...")
    
    try:
        # Initialize components
        browser_manager = BrowserManager()
        await browser_manager.initialize()
        
        # Create analysis queue
        analysis_queue = asyncio.Queue()
        
        # Initialize agents
        navigator = NavigatorAgent(browser_manager, analysis_queue)
        analyzer = ChartAnalyzerAgent()
        
        # Create tasks
        navigator_task = asyncio.create_task(navigator.monitor_homepage())
        analyzer_task = asyncio.create_task(process_analysis_queue(analysis_queue, analyzer))
        
        # Wait for tasks
        await asyncio.gather(navigator_task, analyzer_task)
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise
    finally:
        await browser_manager.close()
        logger.info("Shutting down SwarmScan...")

async def process_analysis_queue(queue: asyncio.Queue, analyzer: ChartAnalyzerAgent):
    """Process items in the analysis queue"""
    logger = logging.getLogger(__name__)
    
    while True:
        try:
            # Get item from queue
            analysis_data = await queue.get()
            
            # Analyze chart
            result = await analyzer.analyze_chart(analysis_data)
            
            if result:
                logger.info(f"Analysis complete for {analysis_data['token_address']}: {result['confidence']}")
            
            # Mark task as done
            queue.task_done()
            
        except Exception as e:
            logger.error(f"Queue processing error: {str(e)}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
