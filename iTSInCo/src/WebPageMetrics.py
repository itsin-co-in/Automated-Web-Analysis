import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import concurrent.futures
import statistics
import subprocess
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn


class WebPageMetrics:
    def __init__(self, url, num_samples=3):
        self.url = url
        self.num_samples = num_samples
        self.console = Console()
        self.metrics = {}

    def measure_initial_response(self):
        try:
            start_time = time.time()
            response = requests.get(self.url)
            end_time = time.time()
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'content_size': len(response.content) / 1024,  # KB
                'headers': response.headers
            }
        except Exception as e:
            return {'error': str(e)}

    def get_resource_urls(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        resources = {
            'images': [urljoin(self.url, img.get('src', '')) for img in soup.find_all('img')],
            'scripts': [urljoin(self.url, script.get('src', '')) for script in soup.find_all('script', src=True)],
            'stylesheets': [urljoin(self.url, link.get('href', '')) for link in soup.find_all('link', rel='stylesheet')]
        }
        return resources

    def measure_resource_load_time(self, resource_url):
        try:
            start_time = time.time()
            response = requests.get(resource_url)
            end_time = time.time()
            return end_time - start_time
        except:
            return None

    def analyze(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # Collect multiple samples
            samples = []
            progress.add_task(description="Analyzing webpage...", total=None)

            for _ in range(self.num_samples):
                sample = self.measure_initial_response()
                if 'error' not in sample:
                    samples.append(sample)

            if not samples:
                self.console.print("[red]Failed to analyze webpage[/red]")
                return

            # Calculate average metrics
            self.metrics['avg_response_time'] = statistics.mean(s['response_time'] for s in samples)
            self.metrics['avg_content_size'] = statistics.mean(s['content_size'] for s in samples)

            # Get resource information from the last successful response
            response = requests.get(self.url)
            resources = self.get_resource_urls(response.content)

            # Measure resource load times
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for resource_type, urls in resources.items():
                    if urls:
                        load_times = list(filter(None, executor.map(self.measure_resource_load_time, urls)))
                        if load_times:
                            self.metrics[f'{resource_type}_count'] = len(urls)
                            self.metrics[f'{resource_type}_avg_load_time'] = statistics.mean(load_times)

            # Generate Lighthouse report using the CLI
            try:
                lighthouse_report = subprocess.check_output(["lighthouse", self.url, "--quiet", "--chrome-path=/usr/bin/chromium-browser"], universal_newlines=True)
                #lighthouse_report = subprocess.check_output(["lighthouse", self.url, "--quiet", "--chrome-flags='--headless'"], universal_newlines=True)
                lighthouse_data = json.loads(lighthouse_report)

                self.metrics['lighthouse_performance_score'] = lighthouse_data['categories']['performance']['score']
                self.metrics['lighthouse_accessibility_score'] = lighthouse_data['categories']['accessibility']['score']
                self.metrics['lighthouse_best_practices_score'] = lighthouse_data['categories']['best-practices']['score']
                self.metrics['lighthouse_seo_score'] = lighthouse_data['categories']['seo']['score']
                self.metrics['lighthouse_pwa_score'] = lighthouse_data['categories']['pwa']['score']
            except subprocess.CalledProcessError as e:
                self.console.print(f"[red]Error generating Lighthouse report: {e}[/red]")
                return

    def display_results(self):
        table = Table(title="Webpage Load Metrics")

        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        # Add rows for each metric
        table.add_row("Average Response Time", f"{self.metrics['avg_response_time']:.3f} seconds")
        table.add_row("Average Content Size", f"{self.metrics['avg_content_size']:.2f} KB")

        # Add resource metrics
        for metric, value in self.metrics.items():
            if metric.endswith('_count'):
                resource_type = metric.replace('_count', '')
                table.add_row(
                    f"{resource_type.capitalize()} Count",
                    str(value)
                )
                if f'{resource_type}_avg_load_time' in self.metrics:
                    table.add_row(
                        f"{resource_type.capitalize()} Avg Load Time",
                        f"{self.metrics[f'{resource_type}_avg_load_time']:.3f} seconds"
                    )

        # Add Lighthouse metrics
        table.add_row("Lighthouse Performance Score", f"{self.metrics['lighthouse_performance_score']:.2f}")
        table.add_row("Lighthouse Accessibility Score", f"{self.metrics['lighthouse_accessibility_score']:.2f}")
        table.add_row("Lighthouse Best Practices Score", f"{self.metrics['lighthouse_best_practices_score']:.2f}")
        table.add_row("Lighthouse SEO Score", f"{self.metrics['lighthouse_seo_score']:.2f}")
        table.add_row("Lighthouse PWA Score", f"{self.metrics['lighthouse_pwa_score']:.2f}")

        self.console.print(table)

def main():
    console = Console()

    try:
        url = input("Enter the webpage URL to analyze: ")
        num_samples = int(input("Enter the number of samples to collect (default is 3): ") or 3)

        analyzer = WebPageMetrics(url, num_samples)

        with console.status("[bold green]Analyzing webpage...") as status:
            analyzer.analyze()

        analyzer.display_results()

    except KeyboardInterrupt:
        console.print("\n[yellow]Analysis cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main()