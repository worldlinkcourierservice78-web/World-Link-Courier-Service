import streamlit as st
import pandas as pd
import random
import string
from datetime import datetime
from st_files_connection import FilesConnection

# --- GOOGLE SHEETS CONFIGURATION ---
GOOGLE_SHEET_URL = "https://google.com"

conn = st.connection("gsheets", type=FilesConnection)

def fetch_data():
    try:
        return conn.read(GOOGLE_SHEET_URL, input_format="csv", ttl="0s")
    except:
        return pd.DataFrame(columns=["tracking_number", "customer_name", "parcel_details", "status", "date_created", "latitude", "longitude"])

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

# Navigation Menu Options
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
                status = result.iloc["status"]
                cust_name = result.iloc["customer_name"]
                details = result.iloc["parcel_details"]
                date_created = result.iloc["date_created"]
                
                st.info(f"**Current Status:** {status}")
                
                try:
                    lat = float(result.iloc["latitude"])
                    lon = float(result.iloc["longitude"])
                    st.markdown("### 🗺️ Live Delivery Destination Map")
                    map_df = pd.DataFrame({"latitude": [lat], "longitude": [lon]})
                    st.map(map_df, zoom=12)
                except Exception:
                    st.warning("⚠️ No map coordinates registered for this shipment address yet.")
                
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
    # Secret Password Field in Sidebar
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    
    # 🔑 NEW SECURE PASSWORD APPLIED BELOW:
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        
        st.markdown("### ➕ Register New Customer Parcel")
        with st.form("add_parcel_form", clear_on_submit=True):
            cust_name = st.text_input("Customer/Recipient Full Name")
            parcel_info = st.text_area("Parcel Description & Delivery Address")
            
            st.markdown("##### 📍 Destination Coordinates (Optional)")
            col1, col2 = st.columns(2)
            with col1:
                lat_input = st.text_input("Latitude (e.g., -1.2921)", value="0.0")
            with col2:
                lon_input = st.text_input("Longitude (e.g., 36.8219)", value="0.0")
                
            submitted = st.form_submit_button("Generate World Link Tracking & Save")
            
            if submitted:
                if cust_name and parcel_info:
                    new_track_id = generate_tracking_id()
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    initial_status = "Manifest Created / Awaiting Dispatch"
                    
                    df = fetch_data()
                    new_row = pd.DataFrame([{
                        "tracking_number": new_track_id,
                        "customer_name": cust_name,
                        "parcel_details": parcel_info,
                        "status": initial_status,
                        "date_created": current_time,
                        "latitude": lat_input,
                        "longitude": lon_input
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=GOOGLE_SHEET_URL, data=updated_df)
                    
                    st.session_state["last_added_parcel"] = {
                        "id": new_track_id, "name": cust_name, "details": parcel_info, "time": current_time, "status": initial_status
                    }
                    st.success(f"Shipment Successfully Saved to Cloud Database!")
                else:
                    st.warning("Please complete both fields to log a new shipment.")

        if "last_added_parcel" in st.session_state:
            p = st.session_state["last_added_parcel"]
            st.markdown("### 🧾 Generated Dispatch Receipt")
            st.info(f"**Tracking Number:** {p['id']}")
            receipt_code = build_receipt_html(p['id'], p['name'], p['details'], p['time'], p['status'])
            st.components.v1.html(receipt_code, height=420, scrolling=True)
            if st.button("Clear Receipt Preview"):
                del st.session_state["last_added_parcel"]
                st.rerun()

        st.markdown("### 🔄 Update Active Parcel Status")
        all_parcels = fetch_data()
        
        if not all_parcels.empty and len(all_parcels) > 0:
            selected_track = st.selectbox("Select Tracking Number to Update", all_parcels["tracking_number"].values)
            new_status = st.selectbox("Update Status To:", [
                "Manifest Created / Awaiting Dispatch", "Picked Up by Courier", "In Transit to Hub", "Out for Delivery", "Delivered Successfully"
            ])
            
            if st.button("Commit Status Update"):
                all_parcels.loc[all_parcels["tracking_number"] == selected_track, "status"] = new_status
                conn.update(spreadsheet=GOOGLE_SHEET_URL, data=all_parcels)
                st.success(f"Tracking ID {selected_track} updated successfully to: **{new_status}**")
                st.rerun() 
                
            st.markdown("### 📋 Live Cloud Shipment Logs")
            st.dataframe(all_parcels, use_container_width=True, hide_index=True)
        else:
            st.info("No active shipments registered in the system yet.")
            
    elif admin_password != "":
        st.error("🔒 Incorrect Admin Password. Access Denied.")
    else:
        st.warning("🔒 This portal is restricted. Please enter the Admin Password in the sidebar to access controls.")
