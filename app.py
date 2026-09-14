import streamlit as st
import pandas as pd
import random
import string
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("world_link_local.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcels (
            tracking_number TEXT PRIMARY KEY,
            customer_name TEXT,
            parcel_details TEXT,
            status TEXT,
            date_created TEXT,
            latitude REAL,
            longitude REAL,
            current_location_text TEXT,
            sender_name TEXT,
            sender_address TEXT
        )
    """)
    try:
        cursor.execute("ALTER TABLE parcels ADD COLUMN current_location_text TEXT DEFAULT 'Main Hub'")
    except sqlite3.OperationalError:
        pass 
    try:
        cursor.execute("ALTER TABLE parcels ADD COLUMN sender_name TEXT DEFAULT 'N/A'")
    except sqlite3.OperationalError:
        pass 
    try:
        cursor.execute("ALTER TABLE parcels ADD COLUMN sender_address TEXT DEFAULT 'N/A'")
    except sqlite3.OperationalError:
        pass 
        
    conn.commit()
    conn.close()

init_db()

def fetch_local_data():
    conn = sqlite3.connect("world_link_local.db")
    df = pd.read_sql_query("SELECT * FROM parcels", conn)
    conn.close()
    return df

def generate_tracking_id():
    df = fetch_local_data()
    existing_ids = df["tracking_number"].values if not df.empty else []
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in existing_ids:
            return tracking_id

def build_receipt_html(track_id, name, details, date, status, s_name, s_addr):
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
            <b>STATUS:</b> {status}<br>
        </div>
        <hr style="border-top:1px dashed #333; margin:10px 0;">
        <div style="font-size:13px; line-height:1.6;">
            <b style="font-size:14px;">🕵️ SENDER DETAILS</b><br>
            <div style="margin-top:5px; padding-left:10px; margin-bottom:10px;">
                <b>SENDER NAME:</b> {s_name}<br>
                <b>SENDER ADDRESS:</b> {s_addr}<br>
            </div>
            <b style="font-size:14px;">📦 RECIPIENT MANIFEST</b><br>
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
            df = fetch_local_data()
            if not df.empty:
                result = df[df["tracking_number"] == search_id]
                if not result.empty:
                    st.success("Shipment Located!")
                    
                    # Safe item extraction from matching dataframe row
                    status = str(result.iloc[0]["status"])
                    cust_name = str(result.iloc[0]["customer_name"])
                    details = str(result.iloc[0]["parcel_details"])
                    date_created = str(result.iloc[0]["date_created"])
                    
                    s_name = str(result.iloc[0]["sender_name"]) if "sender_name" in df.columns else "N/A"
                    s_addr = str(result.iloc[0]["sender_address"]) if "sender_address" in df.columns else "N/A"
                    curr_loc_text = str(result.iloc[0]["current_location_text"]) if "current_location_text" in df.columns else "Main Hub"
                    
                    st.info(f"📍 **Current Location:** {curr_loc_text}")
                    st.warning(f"📊 **Delivery Status:** {status}")
                    
                    lat_val = result.iloc[0]["latitude"]
                    lon_val = result.iloc[0]["longitude"]
                    if pd.notna(lat_val) and pd.notna(lon_val) and lat_val != 0.0 and lon_val != 0.0:
                        st.markdown("### 🗺️ Current Pinned Location Map")
                        map_df = pd.DataFrame({"latitude": [float(lat_val)], "longitude": [float(lon_val)]})
                        st.map(map_df, zoom=14)
                    
                    with st.expander("📄 View Shipment Manifest Details", expanded=True):
                        st.write(f"**Sender:** {s_name} ({s_addr})")
                        st.write(f"**Recipient/Customer:** {cust_name}")
                        st.write(f"**Description & Destination:** {details}")
                        st.write(f"**Dispatch Date:** {date_created}")
                        
                    st.markdown("---")
                    st.markdown("### 🖨️ Customer Copy Receipt")
                    receipt_html = build_receipt_html(search_id, cust_name, details, date_created, status, s_name, s_addr)
                    st.components.v1.html(receipt_html, height=480, scrolling=True)
                else:
                    st.error("Tracking number not recognized by World Link. Please verify your number.")
            else:
                st.error("No database records found. Please log a parcel first.")
        else:
            st.warning("Please type in a tracking number first.")

# ----------------- ADMIN DASHBOARD -----------------
elif menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        st.markdown("### ➕ Register New Customer Parcel")
        
        with st.form("add_parcel_form", clear_on_submit=True):
            st.markdown("##### 🕵️ Sender Information")
            sender_name_in = st.text_input("Sender Full Name")
            sender_addr_in = st.text_input("Sender Address / Branch Location")
            
            st.markdown("##### 📦 Recipient Information")
            cust_name = st.text_input("Recipient Full Name")
            parcel_info = st.text_area("Parcel Details & Delivery Destination Address")
            
            st.markdown("##### 📍 Initial Sorting Location Info")
            init_loc_name = st.text_input("Initial Location Name", value="Main Sorting Hub")
            lat_input = st.text_input("Initial Latitude (Optional)", value="-1.2841")
            lon_input = st.text_input("Initial Longitude (Optional)", value="36.8155")
            
            submitted = st.form_submit_button("Generate World Link Tracking & Save")
            
            if submitted:
                if cust_name and parcel_info and sender_name_in:
                    new_track_id = generate_tracking_id()
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    initial_status = "Manifest Created / Awaiting Dispatch"
                    try:
                        lat_val = float(lat_input)
                        lon_val = float(lon_input)
                    except:
                        lat_val, lon_val = 0.0, 0.0
                    
                    conn = sqlite3.connect("world_link_local.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO parcels (tracking_number, customer_name, parcel_details, status, date_created, latitude, longitude, current_location_text, sender_name, sender_address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (new_track_id, cust_name, parcel_info, initial_status, current_time, lat_val, lon_val, init_loc_name, sender_name_in, sender_addr_in))
                    conn.commit()
                    conn.close()
                    
                    # RESTORED: Saved generated references directly inside session token keys to display the receipt box instantly
                    st.session_state["active_receipt"] = {
                        "id": new_track_id, "name": cust_name, "details": parcel_info, "time": current_time, "status": initial_status, "s_name": sender_name_in, "s_addr": sender_addr_in
                    }
                    st.success(f"Tracking Number Generated Successfully!")
                    st.rerun()
                else:
