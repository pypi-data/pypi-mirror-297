import requests
import socket
import ipaddress
import pkg_resources
import logging
import time
import os
import subprocess
import re
from bs4 import BeautifulSoup

# Set up logging with a more detailed format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IPFetcherError(Exception):
    """Base class for exceptions in this module."""
    pass

class PublicIPError(IPFetcherError):
    """Raised when fetching the public IP fails."""
    pass

class PrivateIPError(IPFetcherError):
    """Raised when fetching the private IP fails."""
    pass

class InvalidIPError(IPFetcherError):
    """Raised when an invalid IP address is provided."""
    pass

def log_message(message, level='info'):
    """Log messages with different levels."""
    level = level.lower()
    if level == 'debug':
        logging.debug(message)
    elif level == 'warn':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    else:
        logging.info(message)

def get_ip_location(ip_address):
    """Fetches location data for the given IP address using ipinfo.io."""
    try:
        # Define the URL for the API request
        url = f"https://ipinfo.io/{ip_address}/json"
        
        # Send a request to the ipinfo.io API
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the response JSON
        data = response.json()
        
        # Extract relevant location information
        location_info = {
            "IP": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country"),
            "Location": data.get("loc")  # This provides latitude and longitude
        }
        
        return location_info

    except requests.RequestException as e:
        return f"Error fetching location data: {e}"
              
def ping_ip(ip_address):
    """Ping an IP address and return the response time."""
    try:
        if os.name == 'nt':  # For Windows
            ping_command = f"ping {ip_address} -n 1"
        else:  # For Linux/Mac
            ping_command = f"ping -c 1 {ip_address}"

        response = subprocess.run(ping_command, capture_output=True, text=True, shell=True)

        if "time=" in response.stdout:
            # Extracting the ping time from the response
            ping_time = response.stdout.split("time=")[1].split("ms")[0]
            return f"Ping to {ip_address}: {ping_time} ms"
        else:
            return f"Failed to ping {ip_address}. No response."
    except Exception as e:
        log_message(f"Error pinging IP: {e}", 'error')
        return f"Error pinging {ip_address}: {e}"

def get_public_ip():
    """Fetches the public IP address of the user."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        log_message(f"Primary API failed: {e}", 'error')
        try:
            response = requests.get("https://api.my-ip.io/ip.json")
            response.raise_for_status()
            return response.json().get("ip", "No IP found")
        except requests.RequestException as e:
            raise PublicIPError(f"Unable to fetch public IP address: {e}")

def get_private_ip():
    """Fetches the private IP address of the user."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error as e:
        raise PrivateIPError(f"Unable to fetch private IP address: {e}")

def is_ipv4(ip):
    """Checks if the given IP address is an IPv4 address."""
    try:
        return ipaddress.ip_address(ip).version == 4
    except ValueError:
        return False

def is_ipv6(ip):
    """Checks if the given IP address is an IPv6 address."""
    try:
        return ipaddress.ip_address(ip).version == 6
    except ValueError:
        return False

def detect_proxy_or_vpn(ip_address):
    """Checks if an IP address is detected as a proxy or VPN."""
    try:
        log_message(f"Checking if {ip_address} is a proxy or VPN...", 'info')
        response = requests.get(f"https://proxycheck.io/v2/{ip_address}")
        response.raise_for_status()
        data = response.json()

        if data[ip_address]["proxy"] == "yes":
            return f"{ip_address} is detected as a proxy or VPN."
        else:
            return f"{ip_address} is not detected as a proxy or VPN."
    except requests.RequestException as e:
        log_message(f"Error checking proxy or VPN status: {e}", 'error')
        return f"Error checking proxy or VPN status: {e}"

def geolocation_lookup(ip_address):
    """Fetches geolocation data for the given IP address."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        data = response.json()

        location_info = {
            "IP": data["ip"],
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country", "N/A"),
            "Org": data.get("org", "N/A"),
            "Location": data.get("loc", "N/A")
        }

        return location_info
    except requests.RequestException as e:
        log_message(f"Error fetching geolocation: {e}", 'error')
        return f"Error fetching geolocation: {e}"

def store(ip_address, filename):
    """Store the IP address into a file."""
    try:
        with open(filename, "a") as file:
            file.write(ip_address + "\n")
        log_message(f"Stored IP address {ip_address} in {filename}.", 'info')
    except IOError as e:
        log_message(f"Error storing IP: {e}", 'error')

def read(filename):
    """Read all IP addresses from the file and return as a list."""
    try:
        with open(filename, "r") as file:
            ips = file.readlines()
        return [ip.strip() for ip in ips]  # Remove extra whitespaces
    except IOError as e:
        log_message(f"Error reading file {filename}: {e}", 'error')
        return []

def is_public_or_private(ip_address):
    """Determines if an IP is public or private."""
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        if ip_obj.is_private:
            log_message(f"Checked IP: {ip_address} is private.", 'info')
            return f"{ip_address} is Private."
        else:
            log_message(f"Checked IP: {ip_address} is public.", 'info')
            return f"{ip_address} is Public."
    except ValueError:
        log_message(f"Invalid IP address provided: {ip_address}", 'error')
        return f"{ip_address} is not a valid IP address."
        
def scrape_ip_data(website_url):
    """Scrapes IP addresses from a given website."""
    try:
        # Send a request to the website
        response = requests.get(website_url)
        response.raise_for_status()

        # Parse the website content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all text that matches an IP address pattern (IPv4)
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        ip_addresses = re.findall(ip_pattern, soup.text)

        if ip_addresses:
            return f"IP addresses found: {', '.join(ip_addresses)}"
        else:
            return "No IP addresses found on the website."
    except requests.RequestException as e:
        return f"Error retrieving data from {website_url}: {e}"
    except Exception as e:
        return f"General error during scraping: {e}"

def monitor_ip(ip_address, interval=60):
    """Monitors the given IP address by pinging and fetching its location at a set interval."""
    while True:
        ping_result = ping_ip(ip_address)
        log_message(ping_result, 'info')
        print(ping_result)

        # Fetch and log additional IP info (e.g., location)
        location_data = get_ip_location(ip_address)
        if isinstance(location_data, dict):
            location_message = (f"Location data for {ip_address}: "
                                f"City: {location_data['City']}, "
                                f"Region: {location_data['Region']}, "
                                f"Country: {location_data['Country']}, "
                                f"Location (lat,long): {location_data['Location']}")
            log_message(location_message, 'info')
            print(location_message)
        else:
            print(location_data)  # Print the error message

        time.sleep(interval)  # Wait for the specified interval before checking again
        
def read_specific(filename, ip_address):
    """Reads a specific IP address from the file."""
    try:
        with open(filename, "r") as file:
            ips = file.readlines()
        for ip in ips:
            if ip.strip() == ip_address:
                return ip_address
        return None  # If the IP is not found
    except IOError as e:
        log_message(f"Error reading file {filename}: {e}", 'error')
        return None
        
