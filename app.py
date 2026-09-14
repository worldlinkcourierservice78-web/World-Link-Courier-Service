import streamlit as st
import pandas as pd
import random
import string
from datetime import datetime

# --- 🌐 BULLETPROOF CLOUD DATABASE LINK ---
# Your permanent Google Sheet URL that NEVER deletes your work
GOOGLE_CSV_URL = "https://google.com"

def fetch_cloud_data():
    try:
        df = pd.read_csv(GOOGLE_CSV_URL)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except:
        # Fallback database structure if sheet is empty or buffering
        return pd.DataFrame(columns=["tracking_number", "customer_name", "parcel_details", "status", "date_created", "latitude", "longitude", "current_location_text", "sender_name", "sender_address"])

def generate_tracking_id():
    df = fetch_cloud_data()
    existing_ids = df["tracking_number"].values if "tracking_number" in df.columns else []
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in existing_ids:
            return tracking_id

# PREMIUM BUSINESS RECEIPT LAYOUT ENGINE
def build_premium_receipt(track_id, name, details, date, status, s_name, s_addr):
    return f"""
    <div style="background-color: #ffffff; color: #1e293b; padding: 25px; border-radius: 12px; max-width: 440px; margin: 10px auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 8px solid #0056b3; border-bottom: 8px solid #0056b3;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #0056b3; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">🌐 WORLD LINK</h2>
            <h5 style="margin: 2px 0 0 0; color: #64748b; font-size: 12px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;">Courier & Logistics Service</h5>
        </div>
        
        <div style="background-color: #f8fafc; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 15px; border: 1px solid #e2e8f0;">
            <span style="font-size: 10px; color: #64748b; display: block; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Tracking Number</span>
            <span style="font-size: 20px; font-weight: 800; color: #0f172a; letter-spacing: 1px;">{track_id}</span>
        </div>

        <div style="font-size: 12px; color: #475569; line-height: 1.6; margin-bottom: 15px;">
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; margin-bottom: 4px;">
                <b>📅 DISPATCH DATE:</b> {date}
            </div>
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; margin-bottom: 4px;">
                <b>📊 STATUS:</b> <span style="color: #2563eb; font-weight: bold;">{status}</span>
            </div>
        </div>

        <div style="margin-bottom: 15px;">
            <h4 style="margin: 0 0 6px 0; font-size: 13px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 6px; text-transform: uppercase; font-weight: 700;">🕵️ Sender Details</h4>
            <div style="font-size: 12px; color: #475569; background-color: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #f1f5f9;">
                <b>Name:</b> {s_name}<br>
                <b>Address/Branch:</b> {s_addr}
            </div>
        </div>

        <div style="margin-bottom: 15px;">
            <h4 style="margin: 0 0 6px 0; font-size: 13px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 6px; text-transform: uppercase; font-weight: 700;">📦 Recipient Manifest</h4>
            <div style="font-size: 12px; color: #475569; background-color: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #f1f5f9;">
                <b>Receiver Name:</b> {name}<br>
                <b>Destination & Info:</b><br>
                <div style="white-space: pre-wrap; font-style: italic; color: #334155; margin-top: 4px; padding-left: 5px; border-left: 2px dashed #cbd5e1;">{details}</div>
            </div>
        </div>

        <hr style="border: none; border-top: 1px dashed #cbd5e1; margin-bottom: 10px;">
        <div style="text-align: center; font-size: 11px; color: #64748b; font-weight: 600;">
            Thank you for choosing World Link Logistics!
        </div>
    </div>
    """

# --- STREAMLIT SCREEN SETUP ---
st.set_page_config(page_title="World Link Courier Service", layout="centered", page_icon="📦")
st.title("🌐 World Link Courier Service")
st.markdown("##### *Fast, Reliable, and Secure Global Tracking Portal*")

menu = st.sidebar.radio("Navigation Portal", ["Customer Tracking View", "Admin / Dispatch Dashboard"])

# ----------------- CUSTOMER VIEW -----------------
if menu == "Customer Tracking View":
    st.subheader("🔍 Track Your Shipment")
    search_id = st.text_input("Enter your tracking number (e.g., WL-XXXXXX):").strip().upper()
    if st.button("Track Shipment"):
        df = fetch_cloud_data()
        result = df[df["tracking_number"] == search_id] if not df.empty and "tracking_number" in df.columns else pd.DataFrame()
        if not result.empty:
            st.success("Shipment Located!")
            
            # Safe text assignments that survive flat structures
            status_val = str(result.iloc[0]["status"])
            name_val = str(result.iloc[0]["customer_name"])
            details_val = str(result.iloc[0]["parcel_details"])
            date_val = str(result.iloc[0]["date_created"])
            s_name_val = str(result.iloc[0]["sender_name"]) if "sender_name" in df.columns else "N/A"
            s_addr_val = str(result.iloc[0]["sender_address"]) if "sender_address" in df.columns else "N/A"
            loc_val = str(result.iloc[0]["current_location_text"]) if "current_location_text" in df.columns else "Main Hub"
            
            st.info(f"📍 **Current Location:** {loc_val}")
            st.warning(f"📊 **Delivery Status:** {status_val}")
            
            lat_num = result.iloc[0]['latitude']
            lon_num = result.iloc[0]['longitude']
            if pd.notna(lat_num) and pd.notna(lon_num) and float(lat_num) != 0.0:
                st.map(pd.DataFrame({"latitude": [float(lat_num)], "longitude": [float(lon_num)]}), zoom=14)
                
            st.markdown("### 📄 Official Tracking Invoice Receipt")
            cust_receipt = build_premium_receipt(search_id, name_val, details_val, date_val, status_val, s_name_val, s_addr_val)
            st.components.v1.html(cust_receipt, height=560, scrolling=True)
        else:
            st.error("Tracking number not recognized by World Link. Please verify your number.")

# ----------------- ADMIN DASHBOARD -----------------
if menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        st.markdown("### ➕ Register New Customer Parcel")
        
        # Aligned form inputs
        s_name = st.text_input("Sender Full Name")
        s_addr = st.text_input("Sender Address / Branch")
        c_name = st.text_input("Recipient Full Name")
        p_info = st.text_area("Parcel Details & Destination Address")
        l_text = st.text_input("Initial Location Description", value="Main Sorting Hub")
        lat_val = st.text_input("Initial Latitude", value="-1.2841")
        lon_val = st.text_input("Initial Longitude", value="36.8155")
        
        if st.button("Generate World Link Tracking & Save"):
            new_id = generate_tracking_id()
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            init_status = "Manifest Created / Awaiting Dispatch"
            
            # Save into Streamlit cache memory instantly to load the premium receipt card
            st.session_state["rcpt_id"] = new_id
            st.session_state["rcpt_cname"] = c_name
            st.session_state["rcpt_details"] = p_info
            st.session_state["rcpt_time"] = c_time
            st.session_state["rcpt_status"] = init_status
            st.session_state["rcpt_sname"] = s_name
            st.session_state["rcpt_saddr"] = s_addr
            
            st.success(f"📦 Tracking Generated Successfully! Code: {new_id}")
            st.markdown("💡 *To save this entry forever, copy the row details into your shared Google Sheet row file.*")
            st.rerun()

        # Display Premium Receipt immediately upon submission
        if "rcpt_id" in st.session_state:
            st.markdown("### 🧾 Official Generated Dispatch Receipt")
            receipt_html_code = build_premium_receipt(
                st.session_state["rcpt_id"],
                st.session_state["rcpt_cname"],
                st.session_state["rcpt_details"],
                st.session_state["rcpt_time"],
                st.session_state["rcpt_status"],
                st.session_state["rcpt_sname"],
                st.session_state["rcpt_saddr"]
            )
            st.components.v1.html(receipt_html_code, height=560, scrolling=True)
            if st.button("Clear Receipt Preview"):
                del st.session_state["rcpt_id"]
                st.rerun()

        st.markdown("### 🔄 Update Live Parcel Location Pin & Status")
        all_parcels = fetch_cloud_data()
        if not all_parcels.empty and "tracking_number" in all_parcels.columns:
            sel_track = st.selectbox("Select Tracking Number to Update Location/Status", all_parcels["tracking_number"].values)
            sel_row = all_parcels[all_parcels["tracking_number"] == sel_track]
            
            new_status = st.selectbox("Update Status To:", ["Manifest Created / Awaiting Dispatch", "Picked Up by Courier - In Transit to Hub", "Arrived at Distribution Facility Hub", "Out for Delivery with Transit Rider", "Delivered Successfully"])
            
