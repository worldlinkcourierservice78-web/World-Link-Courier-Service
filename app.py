import streamlit as st
import pandas as pd
import random
import string
import urllib.parse
from datetime import datetime
from st_files_connection import FilesConnection

# --- GOOGLE SHEETS CONFIGURATION ---
GOOGLE_SHEET_URL = "https://google.com"

conn = st.connection("gsheets", type=FilesConnection)

def fetch_data():
    try:
        return conn.read(GOOGLE_SHEET_URL, input_format="csv", ttl="0s")
    except:
        return pd.DataFrame(columns=["tracking_number", "customer_name", "customer_phone", "parcel_details", "status", "date_created", "latitude", "longitude"])

def generate_tracking_id():
    df = fetch_data()
    existing_ids = df["tracking_number"].values if not df.empty else []
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in existing_ids:
            return tracking_id

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
                
                # Dynamic Location Mapping Pin
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
        
        # Section A: Create a New Parcel with WhatsApp Notification Hook
        st.markdown("### ➕ Register New Customer Parcel")
        with st.form("add_parcel_form", clear_on_submit=True):
            cust_name = st.text_input("Customer Full Name")
            cust_phone = st.text_input("Customer WhatsApp Phone (e.g., +254712345678)")
            parcel_info = st.text_area("Parcel Details & Delivery Address")
            
            st.markdown("##### 📍 Initial Sorting Location Coordinates")
            col1, col2 = st.columns(2)
            with col1:
                lat_input = st.text_input("Initial Latitude (Optional)", value="0.0")
            with col2:
                lon_input = st.text_input("Initial Longitude (Optional)", value="0.0")
                
            submitted = st.form_submit_button("Generate World Link Tracking & Save")
            
            if submitted:
                if cust_name and parcel_info and cust_phone:
                    new_track_id = generate_tracking_id()
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    initial_status = "Manifest Created / Awaiting Dispatch at Main Sorting Hub"
                    
                    df = fetch_data()
                    new_row = pd.DataFrame([{
                        "tracking_number": new_track_id,
                        "customer_name": cust_name,
                        "customer_phone": cust_phone,
                        "parcel_details": parcel_info,
                        "status": initial_status,
                        "date_created": current_time,
                        "latitude": lat_input,
                        "longitude": lon_input
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=GOOGLE_SHEET_URL, data=updated_df)
                    
                    # Generate an instant WhatsApp Message Template
                    msg_text = f"Hello {cust_name}, your World Link Courier Service parcel has been successfully registered! 📦\n\n📌 Tracking Number: {new_track_id}\n📍 Status: {initial_status}\n🌐 Track Live Here: https://streamlit.app"
                    encoded_msg = urllib.parse.quote(msg_text)
                    whatsapp_link = f"https://wa.me{cust_phone.replace('+', '')}?text={encoded_msg}"
                    
                    st.session_state["last_added_parcel"] = {
                        "id": new_track_id, "name": cust_name, "details": parcel_info, "time": current_time, "status": initial_status, "wa_link": whatsapp_link
                    }
                    st.success(f"Shipment Successfully Saved to Cloud Database!")
                else:
                    st.warning("Please complete Customer Name, WhatsApp Phone, and Parcel Details.")

        # Display WhatsApp notification trigger and receipt below form
        if "last_added_parcel" in st.session_state:
            p = st.session_state["last_added_parcel"]
            
            st.markdown("---")
            st.markdown("### 📲 Send Customer Cloud Alert Notification")
            st.info(f"Click the button below to instantly push the tracking manifest details to your customer via WhatsApp.")
            
            # Clickable Notification Link Button
            st.markdown(f'<a href="{p["wa_link"]}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:12px 24px; font-size:16px; font-weight:bold; border-radius:6px; cursor:pointer; width:100%;">💬 Send Notification via WhatsApp</button></a>', unsafe_view_html=True)
            
            st.markdown("### 🧾 Generated Dispatch Receipt")
            receipt_code = build_receipt_html(p['id'], p['name'], p['details'], p['time'], p['status'])
            st.components.v1.html(receipt_code, height=420, scrolling=True)
            
            if st.button("Clear Dashboard Registration Preview"):
                del st.session_state["last_added_parcel"]
                st.rerun()

        # Section B: Update Status AND Pin Location Live
        st.markdown("### 🔄 Update Live Parcel Location Pin & Status")
