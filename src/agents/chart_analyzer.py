from swarms import Agent
import cv2
import numpy as np
import logging
import base64
from pathlib import Path

class ChartAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="ChartAnalyzer",
            system_prompt="""You are a specialized chart analysis agent that:
            1. Processes cryptocurrency chart images
            2. Detects technical patterns and indicators
            3. Analyzes volume profiles
            4. Identifies early-stage opportunities
            5. Calculates opportunity scores""",
            model_name="gpt-4"
        )
        self.logger = logging.getLogger(__name__)
        self.pattern_templates = self.load_pattern_templates()
        
    def load_pattern_templates(self):
        """Load pattern templates for matching"""
        return {
            'accumulation': cv2.imread('patterns/accumulation.png'),
            'breakout': cv2.imread('patterns/breakout.png'),
            'early_stage': cv2.imread('patterns/early_stage.png')
        }

    def decode_image(self, base64_string: str) -> np.ndarray:
        """Convert base64 string to OpenCV image"""
        try:
            img_data = base64.b64decode(base64_string)
            nparr = np.frombuffer(img_data, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            self.logger.error(f"Failed to decode image: {str(e)}")
            return None

    async def analyze_chart(self, chart_data: dict) -> dict:
        """Analyze chart patterns and indicators"""
        try:
            # Decode base64 image
            full_image = self.decode_image(chart_data['chart_image'])
            if full_image is None:
                raise ValueError("Failed to decode chart image")

            # Isolate chart area
            chart_area = self.isolate_chart_area(full_image)
            
            # Process image
            processed = self.preprocess_image(chart_area)
            
            # Early stage analysis
            early_stage_indicators = await self.detect_early_stage_patterns(processed)
            
            # Price movement analysis
            price_patterns = await self.analyze_price_movement(processed)
            
            # Volume analysis with more detail
            volume_profile = await self.analyze_volume(processed, detailed=True)

            return {
                'token_address': chart_data['token_address'],
                'early_stage_indicators': early_stage_indicators,
                'price_patterns': price_patterns,
                'volume_profile': volume_profile,
                'confidence': self.calculate_opportunity_score(
                    early_stage_indicators,
                    price_patterns,
                    volume_profile
                )
            }

        except Exception as e:
            self.logger.error(f"Chart analysis failed: {str(e)}")
            return None

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess chart image for analysis"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply threshold
            _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
            
            return thresh
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {str(e)}")
            return None

    def isolate_chart_area(self, image: np.ndarray) -> np.ndarray:
        """Isolate the chart area from the full screenshot"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Find edges
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest contour (likely the chart area)
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Extract chart area
                chart_area = image[y:y+h, x:x+w]
                return chart_area
                
            return image
        except Exception as e:
            self.logger.error(f"Chart area isolation failed: {str(e)}")
            return image

    async def detect_early_stage_patterns(self, image: np.ndarray) -> dict:
        """Detect early stage patterns"""
        return {
            'accumulation': self.detect_accumulation(image),
            'breakout_potential': self.detect_breakout_potential(image),
            'volume_buildup': self.detect_volume_buildup(image)
        }

    async def analyze_price_movement(self, image: np.ndarray) -> dict:
        """Analyze price movement patterns"""
        return {
            'trend': self.detect_trend(image),
            'support_levels': self.detect_support_levels(image),
            'resistance_levels': self.detect_resistance_levels(image),
            'price_action': self.analyze_price_action(image)
        }

    def detect_accumulation(self, image: np.ndarray) -> bool:
        """Detect accumulation patterns"""
        # Implementation for accumulation detection
        pass

    def detect_breakout_potential(self, image: np.ndarray) -> float:
        """Detect potential breakout patterns"""
        # Implementation for breakout potential
        pass

    def detect_volume_buildup(self, image: np.ndarray) -> dict:
        """Detect volume buildup patterns"""
        # Implementation for volume buildup
        pass
    async def analyze_volume(self, image: np.ndarray, detailed: bool = False) -> dict:
        """Analyze volume profile"""
        try:
            height, width = image.shape[:2]
            volume_region = image[int(height*0.8):, :]
            
            # Convert to grayscale
            gray_volume = cv2.cvtColor(volume_region, cv2.COLOR_BGR2GRAY)
            
            # Find volume bars using edge detection
            edges = cv2.Canny(gray_volume, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calculate volume metrics
            volumes = []
            for contour in contours:
                _, _, _, h = cv2.boundingRect(contour)
                volumes.append(h)
            
            if not volumes:
                return {'distribution': 'unknown', 'average': 0, 'spikes': []}
            
            avg_volume = sum(volumes) / len(volumes)
            volume_std = np.std(volumes) if len(volumes) > 1 else 0
            
            # Detect volume spikes
            spikes = [v for v in volumes if v > avg_volume + 2 * volume_std]
            
            return {
                'distribution': 'normal' if len(spikes) < 3 else 'suspicious',
                'average': float(avg_volume),
                'spikes': len(spikes)
            }
            
        except Exception as e:
            self.logger.error(f"Volume analysis failed: {str(e)}")
            return None

    def calculate_opportunity_score(self, early_stage_indicators: dict, price_patterns: dict, volume_profile: dict) -> float:
        """Calculate opportunity score for the analysis"""
        try:
            # Implement scoring logic based on early stage indicators, price patterns, and volume
            score = 0.0
            
            # Early stage indicators scoring
            if early_stage_indicators['accumulation']:
                score += 0.3
            if early_stage_indicators['breakout_potential']:
                score += 0.3
            
            # Price patterns scoring
            if price_patterns['trend']:
                score += 0.4
            
            # Volume scoring
            if volume_profile and volume_profile['distribution'] == 'normal':
                score += 0.3
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Opportunity score calculation failed: {str(e)}")
            return 0.0

    def stop(self):
        """Stop the analyzer agent"""
        self.running = False

    async def run(self, chart_data: dict):
        """Main agent loop using Swarms framework"""
        try:
            analysis_result = await self.analyze_chart(chart_data)
            return {
                "type": "chart_analysis",
                "data": analysis_result
            }
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return None

