from selenium import webdriver
from selenium.common.exceptions import WebDriverException,TimeoutException
import requests
import os
import time
import re
import socket

class Bpix:



    def __init__(self, file_path, time_out):

        self.file_path = file_path
        self.time_out = time_out




    def s_shot(self):
        # Pattern for getting domain 
        pattern = r"^https?://"
        # Set up browser options
        options = webdriver.FirefoxOptions()
        # Run Chrome in headless mode (no GUI)
        options.add_argument("--headless") 

        # Start with a clean browsing session 
        options.add_argument("--incognito") 

        # Initialize Chrome WebDriver
        browser = webdriver.Firefox(options=options)
        

        target_domains = []

        # Read the file and append each domain to the target_domains list
        try:
            with open(self.file_path, "r") as file:
                target_domains = file.read().split()
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            browser.quit()
            return

        # Make screenshot path 
        if os.path.isdir("screenshots"):
            pass
        else :
            os.mkdir("screenshots")
        
        # Iterate through each domain and take a screenshot
        for domain in target_domains:
            
             # Make screenshot path 
            if os.path.isdir("D2ip"):
                pass
            else :
                os.mkdir("D2ip")

            if domain.startswith("https") or domain.startswith("http"):
                url = domain
            else:
                print("It does not start with http or https")
                print("example: https://abc.com/")
                quit()
                        


            # File name for save each images 
            file_name = re.sub(pattern,' ', url)

            try:
                response = requests.get(url)
                browser.get(url)
                time.sleep(self.time_out)
                browser.save_screenshot(f"screenshots/{file_name}.png")
                print(f"Screenshot saved {file_name} ")
            except (requests.exceptions.RequestException, WebDriverException) as e:
                print(f"Error accessing {url}: {e}")
            except TimeoutException:
                print(f"Timeout accessing {url}")
            
        

        # Close the browser after taking all screenshots
        browser.quit()


class DNS:
    def __init__(self, file_path, output_folder):
        self.file_path = file_path
        self.output_folder = output_folder

    def get_ip(self, domain):
        """Convert a domain to its IP address."""
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            print(f"Unable to get IP address for {domain}.")
            return None

    def process_domains(self):
        """Process domains from the file and convert them to IP addresses."""
        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Define the output file path
        output_file = os.path.join(self.output_folder, 'ip_addresses.txt')
        
        try:
            with open(self.file_path, "r") as file:
                target_domains = file.read().split()
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            return
        
        # Open the output file for writing
        with open(output_file, 'w') as out_file:
            for domain in target_domains:
                domain = domain.strip()
                if not domain.startswith(("http://", "https://")):
                    ip = self.get_ip(domain)
                    if ip:
                        out_file.write(f"Domain: {domain}, IP Address: {ip}\n")
                        print(f"Domain: {domain}, IP Address: {ip}")
                else:
                    print("It seems the domain starts with http or https. Please provide only the domain name.")
                    print("Example: google.com")


