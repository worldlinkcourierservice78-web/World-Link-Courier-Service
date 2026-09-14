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
    # 1. Create the base table structure if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcels (
            tracking_number TEXT PRIMARY KEY,
            customer_name TEXT,
            parcel_details TEXT,
            status TEXT,
            date_created TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    # 2. AUTOMATIC MIGRATION: Safely inject the new column if it is missing
    try:
        cursor.execute("ALTER TABLE parcels ADD COLUMN current_location_text TEXT DEFAULT 'Main Hub'")
    except sqlite3.OperationalError:
        pass # The column already exists, do nothing
        
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
            <b>STATUS:</b> {status}<br>
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
            df = fetch_local_data()
            if not df.empty:
                result = df[df["tracking_number"] == search_id]
                if not result.empty:
                    st.success("Shipment Located!")
                    status = result.iloc[0]["status"]
                    cust_name = result.iloc[0]["customer_name"]
                    details = result.iloc[0]["parcel_details"]
                    date_created = result.iloc[0]["date_created"]
                    
                    curr_loc_text = result.iloc[0]["current_location_text"] if "current_location_text" in df.columns else "Main Hub"
                    if not curr_loc_text or pd.isna(curr_loc_text):
                        curr_loc_text = "Main Hub"
                    
                    st.info(f"📍 **Current Location:** {curr_loc_text}")
                    st.warning(f"📊 **Delivery Status:** {status}")
                    
                    lat_val = result.iloc[0]["latitude"]
                    lon_val = result.iloc[0]["longitude"]
                    if pd.notna(lat_val) and pd.notna(lon_val) and lat_val != 0.0 and lon_val != 0.0:
                        st.markdown("### 🗺️ Current Pinned Location Map")
                        map_df = pd.DataFrame({"latitude": [float(lat_val)], "longitude": [float(lon_val)]})
                        st.map(map_df, zoom=14)
                    
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
        
        cust_name = st.text_input("Customer Full Name")
        parcel_info = st.text_area("Parcel Details & Delivery Address")
        
        st.markdown("##### 📍 Initial Sorting Location Info")
        init_loc_name = st.text_input("Initial Location Name", value="Main Sorting Hub")
        lat_input = st.text_input("Initial Latitude (Optional)", value="-1.2841")
        lon_input = st.text_input("Initial Longitude (Optional)", value="36.8155")
        
        if st.button("Generate World Link Tracking & Save"):
            if cust_name and parcel_info:
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
                    INSERT INTO parcels (tracking_number, customer_name, parcel_details, status, date_created, latitude, longitude, current_location_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (new_track_id, cust_name, parcel_info, initial_status, current_time, lat_val, lon_val, init_loc_name))
                conn.commit()
                conn.close()
                
                st.session_state["last_added_parcel"] = {
                    "id": new_track_id, "name": cust_name, "details": parcel_info, "time": current_time, "status": initial_status
                }
                st.success(f"Tracking Number Generated Successfully!")
                st.rerun()
            else:
                st.warning("Please complete both Customer Name and Parcel Details fields.")

        if "last_added_parcel" in st.session_state:
            p = st.session_state["last_added_parcel"]
            st.markdown("---")
            st.info(f"👉 **Tracking Number Created:** `{p['id']}` (Give this to your customer)")
            st.markdown("### 🧾 Generated Dispatch Receipt")
            receipt_code = build_receipt_html(p['id'], p['name'], p['details'], p['time'], p['status'])
            st.components.v1.html(receipt_code, height=420, scrolling=True)
            if st.button("Clear Dashboard Registration Preview"):
                del st.session_state["last_added_parcel"]
                st.rerun()

        # Update Parcel Status Section
        st.markdown("### 🔄 Update Live Parcel Location Pin & Status")
        all_parcels = fetch_local_data()
        
        if not all_parcels.empty:
            selected_track = st.selectbox("Select Tracking Number to Update Location/Status", all_parcels["tracking_number"].values)
            current_row = all_parcels[all_parcels["tracking_number"] == selected_track]
            
            new_status = st.selectbox("Update Status To:", [
                "Manifest Created / Awaiting Dispatch", 
                "Picked Up by Courier - In Transit to Hub", 
                "Arrived at Distribution Facility Hub", 
                "Out for Delivery with Transit Rider", 
                "Delivered Successfully"
            ])
            
            existing_loc_str = str(current_row.iloc[0]["current_location_text"]) if "current_location_text" in all_parcels.columns else "Main Hub"
