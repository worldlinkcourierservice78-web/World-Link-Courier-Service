import streamlit as st
import pandas as pd
import random
import string
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from st_files_connection import FilesConnection

# --- GOOGLE SHEETS CONFIGURATION ---
GOOGLE_SHEET_URL = "https://google.com"

# --- 📧 SECURE AUTOMATED EMAIL SYSTEM SETUP (CONFIGURED) ---
SENDER_EMAIL = "worldlinkcourierservice78@gmail.com"
SENDER_PASSWORD = "hagi qvsv ebro klvv"

conn = st.connection("gsheets", type=FilesConnection)

def fetch_data():
    try:
        return conn.read(GOOGLE_SHEET_URL, input_format="csv", ttl="0s")
    except:
        return pd.DataFrame(columns=["tracking_number", "customer_name", "customer_phone", "customer_email", "parcel_details", "status", "date_created", "latitude", "longitude"])

def generate_tracking_id():
    df = fetch_data()
    existing_ids = df["tracking_number"].values if not df.empty else []
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in existing_ids:
            return tracking_id

# SILENT BACKGROUND EMAIL SYSTEM
def send_tracking_email(receiver_email, customer_name, tracking_number, parcel_details, initial_status):
    try:
        msg = MIMEMultipart()
        msg["From"] = f"World Link Courier Service <{SENDER_EMAIL}>"
        msg["To"] = receiver_email
        msg["Subject"] = f"📦 Shipment Registered - {tracking_number} (World Link)"
        
        # Professional Courier HTML layout design for inbox views
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; border-top: 5px solid #0056b3; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #0056b3; text-align: center; margin-top: 0;">🌐 WORLD LINK COURIER SERVICE</h2>
                <p>Hello <b>{customer_name}</b>,</p>
                <p>Your package has been successfully processed and registered into our logistics network for dispatch.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #28a745; margin: 20px 0; border-radius: 4px;">
                    <h3 style="margin-top: 0; color: #28a745;">📋 Shipment Information</h3>
                    <table style="width: 100%; font-size: 14px; line-height: 1.6;">
                        <tr><td><b>Tracking Number:</b></td><td style="font-size: 16px; font-weight: bold; color: #0056b3;">{tracking_number}</td></tr>
                        <tr><td><b>Current Status:</b></td><td>{initial_status}</td></tr>
                        <tr><td><b>Details / Destination Address:</b></td><td>{parcel_details}</td></tr>
                    </table>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="https://streamlit.app" style="background-color: #0056b3; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Track Shipment Live</a>
                </p>
                <hr style="border: none; border-top: 1px solid #eeeeee; margin-top: 4px;">
                <p style="font-size: 11px; color: #777; text-align: center;">Thank you for trusting World Link Logistics. This is an automated business notification.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))
        
        # Connect to secure Gmail SMTP Server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Mail delivery subsystem error: {e}")
        return False

def build_receipt_html(track_id, name, details, date, status):
    return f"""
    <div id="receipt-print-area" style="padding:20px; border:2px dashed #333; max-width:450px; margin:0 auto; font-family:monospace; background-color:#fff; color:#000;">
        <div style="text-align:center; margin-bottom:10px;">
            <h2 style="margin:0; font-size:22px;">🌐 WORLD LINK</h2>
            <h4 style="margin:0; font-size:14px; letter-spacing:1px;">COURIER SERVICE</h4>
            <p style="margin:5px 0 0 0; font-size:11px;">Fast, Reliable & Secure Global Logistics</p>
        </div>
        <hr style="border-top:1px dashed #333; margin:10px 0;">
        <div style="font-size:13px; line-height:1.6;">
            <b>DATE/TIME:</b> {date}<br>
            <b>TRACKING NO:</b> <span style="font-size:16px; font-weight:bold;">{track_id}</span><br>
            <b>INITIAL STATUS:</b> {status}<br>
        </div>
        <hr style="border-top:1px dashed #333; margin:10px 0;">
        <div style="font-size:13px; line-height:1.6;">
            <b style="font-size:14px;">SHIPMENT MANIFEST</b><br>
            <div style="margin-top:5px; padding-left:10px;">
                <b>CUSTOMER:</b> {name}<br>
                <b>DETAILS & DESTINATION:</b><br>
                <div style="white-space: pre-wrap; padding-left:10px; font-style:italic;">{details}</div>
            </div>
        </div>
        <hr style="border-top:1px dashed #333; margin:15px 0 10px 0;">
        <div style="text-align:center; font-size:12px; font-weight:bold;">
            Thank you for choosing World Link!<br>
            Tracking Live via World Link Portal
        </div>
    </div>
    """

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="World Link Courier Service", layout="centered", page_icon="📦")
st.title("🌐 World Link Courier Service")
st.markdown("##### *Fast, Reliable, and Secure Global Tracking Portal*")

menu = st.sidebar.radio("Navigation Portal", ["Customer Tracking View", "Admin / Dispatch Dashboard"])

# ----------------- CUSTOMER VIEW -----------------
if menu == "Customer Tracking View":
    st.subheader("🔍 Track Your Shipment")
    search_id = st.text_input("Enter your tracking number (e.g., WL-XXXXXX):").strip().upper()
    
    if st.button("Track Shipment"):
        if search_id:
            df = fetch_data()
            result = df[df["tracking_number"] == search_id] if not df.empty else pd.DataFrame()
            
            if not result.empty:
                st.success("Shipment Located!")
                status = result.iloc[0]["status"]
                cust_name = result.iloc[0]["customer_name"]
                details = result.iloc[0]["parcel_details"]
                date_created = result.iloc[0]["date_created"]
                
                st.info(f"📍 **Current Location Status:** {status}")
                
                try:
                    lat = float(result.iloc[0]["latitude"])
                    lon = float(result.iloc[0]["longitude"])
                    if lat != 0.0 and lon != 0.0:
                        st.markdown("### 🗺️ Current Pinned Location Map")
                        map_df = pd.DataFrame({"latitude": [lat], "longitude": [lon]})
                        st.map(map_df, zoom=14)
                    else:
                        st.warning("📍 Parcel is at sorting hub. Live coordinate mapping will update upon transit.")
                except Exception:
                    st.warning("⚠️ No coordinate data registered for this status location yet.")
                
                with st.expander("📄 View Shipment Manifest Details", expanded=True):
                    st.write(f"**Recipient/Customer:** {cust_name}")
                    st.write(f"**Description & Destination:** {details}")
                    st.write(f"**Dispatch Date:** {date_created}")
                    
                st.markdown("---")
                st.markdown("### 🖨️ Customer Copy Receipt")
                receipt_html = build_receipt_html(search_id, cust_name, details, date_created, status)
                st.components.v1.html(receipt_html, height=420, scrolling=True)
            else:
                st.error("Tracking number not recognized by World Link. Please verify your number.")
        else:
            st.warning("Please type in a tracking number first.")

# ----------------- ADMIN DASHBOARD (SECURE ACCESS) -----------------
elif menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        
        st.markdown("### ➕ Register New Customer Parcel")
        with st.form("add_parcel_form", clear_on_submit=True):
            cust_name = st.text_input("Customer Full Name")
            cust_phone = st.text_input("Customer WhatsApp Phone (e.g., +254712345678)")
            cust_email = st.text_input("Customer Email Address (e.g., customer@email.com)")
            parcel_info = st.text_area("Parcel Details & Delivery Address")
            
            st.markdown("##### 📍 Initial Sorting Location Coordinates")
            col1, col2 = st.columns(2)
            with col1:
                lat_input = st.text_input("Initial Latitude (Optional)", value="0.0")
            with col2:
                lon_input = st.text_input("Initial Longitude (Optional)", value="0.0")
                
            submitted = st.form_submit_button("Generate World Link Tracking & Save")
            
            if submitted:
                if cust_name and parcel_info and cust_phone and cust_email:
                    new_track_id = generate_tracking_id()
