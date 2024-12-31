from swarms import SequentialWorkflow
from .agents.navigator import NavigatorAgent
from .agents.chart_analyzer import ChartAnalyzerAgent
from .agents.data_collector import DataCollectorAgent
from .agents.risk_assessor import RiskAssessorAgent
import logging

class ScanOrchestrator:
    def __init__(self, browser_manager):
        self.logger = logging.getLogger(__name__)
        
        # Initialize agents
        self.navigator = NavigatorAgent(browser_manager)
        self.analyzer = ChartAnalyzerAgent()
        self.collector = DataCollectorAgent()
        self.risk_assessor = RiskAssessorAgent()
        
        # Create sequential workflow
        self.workflow = SequentialWorkflow(
            name="CryptoScanner",
            description="Scans and analyzes crypto trading opportunities",
            agents=[self.navigator, self.analyzer, self.collector, self.risk_assessor]
        )
    
    async def execute(self, target_url: str):
        """Execute the full scanning workflow"""
        try:
            self.logger.info(f"Starting scan orchestration for {target_url}")
            
            # 1. Navigate and get screenshot
            nav_result = await self.navigator.run(target_url)
            if not nav_result:
                raise Exception("Navigation failed")
                
            # 2. Analyze chart
            chart_result = await self.analyzer.run({
                "chart_image": nav_result["data"]["screenshot"],
                "token_address": target_url
            })
            
            # 3. Collect market data
            market_data = await self.collector.run(target_url)
            
            # 4. Assess risks
            risk_assessment = await self.risk_assessor.run({
                "chart_analysis": chart_result["data"],
                "market_data": market_data["data"]
            })
            
            self.logger.info("Scan orchestration completed successfully")
            return {
                "navigation": nav_result,
                "chart_analysis": chart_result,
                "market_data": market_data,
                "risk_assessment": risk_assessment
            }
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {str(e)}")
            return None 