import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import cssutils
import logging
from urllib.parse import urljoin, urlparse
import time
import re
from lighthouse import Lighthouse
from playwright.sync_api import sync_playwright
import pandas as pd

class WebsiteAnalyzer:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.driver = None
        self.soup = None
        self.analysis_results = {
            'view_layer': {},
            'model_layer': {},
            'controller_layer': {},
            'performance': {},
            'security': {},
            'accessibility': {}
        }

    def setup_selenium(self):
        """Initialize Selenium WebDriver with performance logging"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)

    def analyze_view_layer(self):
        """Analyze DOM structure and styling"""
        response = self.session.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')

        # Analyze DOM structure
        self.analysis_results['view_layer']['dom_structure'] = {
            'total_elements': len(self.soup.find_all()),
            'semantic_elements': self._count_semantic_elements(),
            'component_hierarchy': self._analyze_component_hierarchy()
        }

        # Analyze CSS
        self.analysis_results['view_layer']['styling'] = {
            'stylesheets': self._analyze_stylesheets(),
            'design_system': self._analyze_design_system()
        }

    def analyze_model_layer(self):
        """Analyze data flow and state management"""
        if not self.driver:
            self.setup_selenium()

        self.driver.get(self.url)
        
        # Analyze API endpoints
        network_data = self._capture_network_data()
        self.analysis_results['model_layer']['api_endpoints'] = network_data

        # Analyze state management
        self.analysis_results['model_layer']['state_management'] = {
            'local_storage': self._analyze_storage('localStorage'),
            'session_storage': self._analyze_storage('sessionStorage'),
            'cookies': self._analyze_cookies()
        }

    def analyze_controller_layer(self):
        """Analyze JavaScript and event handling"""
        if not self.driver:
            self.setup_selenium()

        # Analyze JavaScript files
        self.analysis_results['controller_layer']['javascript'] = {
            'frameworks': self._detect_frameworks(),
            'event_handlers': self._analyze_event_handlers(),
            'routing': self._analyze_routing()
        }

    def analyze_performance(self):
        """Analyze website performance metrics"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            
            # Navigate and collect performance metrics
            page.goto(self.url)
            performance_metrics = page.evaluate("""
                () => {
                    const timing = window.performance.timing;
                    const navigation = performance.getEntriesByType('navigation')[0];
                    return {
                        loadTime: timing.loadEventEnd - timing.navigationStart,
                        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                        firstPaint: performance.getEntriesByType('paint')[0].startTime,
                        resourceCount: performance.getEntriesByType('resource').length
                    }
                }
            """)
            
            self.analysis_results['performance'] = performance_metrics
            browser.close()

    def analyze_security(self):
        """Analyze security implementations"""
        response = requests.get(self.url)
        headers = response.headers

        self.analysis_results['security'] = {
            'https': self.url.startswith('https'),
            'content_security_policy': headers.get('Content-Security-Policy'),
            'x_frame_options': headers.get('X-Frame-Options'),
            'x_xss_protection': headers.get('X-XSS-Protection')
        }

    def analyze_accessibility(self):
        """Analyze accessibility compliance"""
        if not self.driver:
            self.setup_selenium()

        # Run accessibility checks using axe-core or similar tools
        self.analysis_results['accessibility'] = {
            'aria_roles': self._check_aria_roles(),
            'color_contrast': self._check_color_contrast(),
            'keyboard_navigation': self._check_keyboard_navigation()
        }

    def generate_report(self, output_format='json'):
        """Generate analysis report in specified format"""
        if output_format == 'json':
            with open('analysis_report.json', 'w') as f:
                json.dump(self.analysis_results, f, indent=4)
        elif output_format == 'html':
            self._generate_html_report()
        elif output_format == 'excel':
            self._generate_excel_report()

    def _count_semantic_elements(self):
        """Count usage of semantic HTML elements"""
        semantic_elements = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        return {elem: len(self.soup.find_all(elem)) for elem in semantic_elements}

    def _analyze_component_hierarchy(self):
        """Analyze and map component hierarchy"""
        def get_component_tree(element, depth=0):
            if depth > 5:  # Limit depth to prevent infinite recursion
                return None
            
            children = element.find_all(recursive=False)
            component_info = {
                'tag': element.name,
                'classes': element.get('class', []),
                'id': element.get('id', ''),
                'children': [get_component_tree(child, depth + 1) for child in children if child.name is not None]
            }
            return component_info

        return get_component_tree(self.soup.body)

    def _analyze_stylesheets(self):
        """Analyze CSS stylesheets"""
        stylesheets = []
        for css in self.soup.find_all('link', rel='stylesheet'):
            try:
                css_url = urljoin(self.url, css['href'])
                response = self.session.get(css_url)
                if response.status_code == 200:
                    stylesheet = cssutils.parseString(response.text)
                    stylesheets.append({
                        'url': css_url,
                        'rules_count': len(stylesheet.cssRules),
                        'selectors': self._analyze_css_selectors(stylesheet)
                    })
            except Exception as e:
                logging.error(f"Error analyzing stylesheet {css_url}: {str(e)}")
        return stylesheets

    def _analyze_design_system(self):
        """Analyze design system patterns"""
        colors = set()
        font_families = set()
        spacing_values = set()

        # Extract inline styles and CSS rules
        for elem in self.soup.find_all(style=True):
            style = elem['style']
            colors.update(re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', style))
            font_families.update(re.findall(r'font-family:\s*([^;]+)', style))
            spacing_values.update(re.findall(r'margin|padding]:\s*([^;]+)', style))

        return {
            'colors': list(colors),
            'typography': list(font_families),
            'spacing': list(spacing_values)
        }

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        self.session.close()

def main():
    # Example usage
    analyzer = WebsiteAnalyzer('https://example.com')
    
    try:
        # Run analysis
        analyzer.analyze_view_layer()
        analyzer.analyze_model_layer()
        analyzer.analyze_controller_layer()
        analyzer.analyze_performance()
        analyzer.analyze_security()
        analyzer.analyze_accessibility()
        
        # Generate report
        analyzer.generate_report(output_format='json')
        
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    main()
