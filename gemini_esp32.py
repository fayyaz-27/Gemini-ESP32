# Author: Fayyaz Shaikh
# Program Name: Gemini ESP32 Bot
# Date: 20th August 2025
# LinkedIn: https://www.linkedin.com/in/fayyaz-shaikh-7646312a3/

from machine import Pin
import network
import urequests
import time

# Wi-Fi Credentials
WIFI_SSID = "fayyaz\'s realme 8"
WIFI_PASSWORD = '89ghn62s'

# 🔹 Google Gemini API Key
GEMINI_API_KEY = "AIzaSyCW36i8-dwGoRPf54BIuETGGAk_g680MLg"
#GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"


# Connect ESP32 to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected! IP:", wlan.ifconfig()[0])

# Function to Send Request to Gemini
def get_gemini_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}  # Gemini API format

    try:
        response = urequests.post(GEMINI_URL, json=data, headers=headers)
        result = response.json()
        response.close()
        #print("Raw API Response:", result)  # Debugging: Print full response
        
        # Extract and return the response text
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error: {result}"  # Return full error message if failure
    except Exception as e:
        return f"Request Error: {e}"

# Main Execution
connect_wifi()

#while True:
#   user_input = "Hi I am Fayyaz"  # Change this prompt as needed
#    print("Sending request to Gemini...")
#    gemini_response = get_gemini_response(user_input)
#    print("Gemini:", gemini_response)   
#    time.sleep(10)  # Delay before next query

import os

# 🔹 Function to Save Chat
def save_chat(user_input, gemini_response):
    with open("chat_history.txt", "a") as file:  # Open file in append mode
        file.write(f"You: {user_input}\nGemini: {gemini_response}\n\n")

# Function to Read Past Chats
#def load_chat():
#    if "chat_history.txt" in os.listdir():  # Check if file exists
#        with open("chat_history.txt", "r") as file:
#            return file.read()
#    return ""

# Function to Load Past Chats
def load_chat():
    try:
        with open("chat_history.txt", "r") as file:
            return file.read()
    except OSError:
        return ""  # Return empty string if file doesn't exist

def load_recent_chats():
    try:
        with open("chat_history.txt", "r") as file:
            lines = file.readlines()
            return "".join(lines[-10:])  # Load only last 10 lines
    except OSError:
        return "error"



while True:
    
    user_input = input("You: ")  # Ask user for input
    if user_input.lower() in ["exit", "quit"]:  # Allow exit
        print("Exiting...")
        break

    #print("Sending request to Gemini...")
    gemini_response = get_gemini_response(user_input)
    print("Gemini:", gemini_response)

    time.sleep(1)  # Delay before asking again



