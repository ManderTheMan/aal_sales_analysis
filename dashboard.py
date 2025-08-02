import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import base64
from io import BytesIO

# Configure the page
st.set_page_config(
    page_title="AAL Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .tab-header {
        font-size: 2rem;
        font-weight: bold;
        color: #A23B72;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Function to generate PDF report
def generate_pdf_report(include_summary=False, include_analytics=False, include_charts=False):
    """Generate a PDF report based on selected options"""
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'AAL Sales Analysis Report', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # For now, just add dummy content
    pdf.cell(0, 10, 'Test dummy content for PDF generation', 0, 1)
    pdf.ln(10)
    pdf.cell(0, 10, f'Report generated with the following options:', 0, 1)
    pdf.cell(0, 10, f'- Include Summary: {include_summary}', 0, 1)
    pdf.cell(0, 10, f'- Include Analytics: {include_analytics}', 0, 1)
    pdf.cell(0, 10, f'- Include Charts: {include_charts}', 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# Function to create download link for PDF
def create_download_link(pdf_data, filename):
    """Create a download link for the PDF"""
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download PDF Report</a>'
    return href

# Initialize session state for navigation
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'Home'

# Main title
st.markdown('<div class="main-header">AAL Sales Analytics Dashboard</div>', unsafe_allow_html=True)

# Navigation dropdown in sidebar
st.sidebar.markdown("## Navigation")
tab_options = ['Home', 'Analytics', 'Appendix']
selected_tab = st.sidebar.selectbox(
    "Select Tab:",
    tab_options,
    index=tab_options.index(st.session_state.current_tab)
)

# Update session state when dropdown changes
if selected_tab != st.session_state.current_tab:
    st.session_state.current_tab = selected_tab

# Generate Report Button (always visible at top)
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔧 Generate Report", type="primary", use_container_width=True):
        st.session_state.show_report_modal = True

# Report Generation Modal
if st.session_state.get('show_report_modal', False):
    with st.container():
        st.markdown("### 📋 Select what to include in report")
        
        # Create a form for the modal
        with st.form("report_options"):
            st.markdown("**Report Options:**")
            
            col1, col2 = st.columns(2)
            with col1:
                include_summary = st.checkbox("Executive Summary", value=True)
                include_analytics = st.checkbox("Analytics Data", value=True)
            
            with col2:
                include_charts = st.checkbox("Charts & Visualizations", value=True)
                include_appendix = st.checkbox("Appendix", value=False)
            
            # Form submit button
            submitted = st.form_submit_button("📄 Generate PDF", type="primary", use_container_width=True)
            
            if submitted:
                # Generate the PDF
                pdf_data = generate_pdf_report(include_summary, include_analytics, include_charts)
                
                # Show success message
                st.success("✅ Report generated successfully!")
                
                # Create download link
                st.markdown(
                    create_download_link(pdf_data, "AAL_Sales_Report.pdf"),
                    unsafe_allow_html=True
                )
                
                # Close modal after generation
                st.session_state.show_report_modal = False
                st.rerun()

        # Close modal button
        if st.button("❌ Close", key="close_modal"):
            st.session_state.show_report_modal = False
            st.rerun()

st.markdown("---")

# TAB CONTENT BASED ON SELECTION
if st.session_state.current_tab == 'Home':
    st.markdown('<div class="tab-header">🏠 Executive Summary</div>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value="$X.XX M",
            delta="XX% vs Q3"
        )
    
    with col2:
        st.metric(
            label="Total Transactions", 
            value="X,XXX",
            delta="XXX transactions"
        )
    
    with col3:
        st.metric(
            label="Avg Transaction",
            value="$XXX",
            delta="$XX increase"
        )
    
    with col4:
        st.metric(
            label="States Analyzed",
            value="X",
            delta="All major markets"
        )
    
    # Executive Summary Content
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Key Findings")
        st.markdown("""
        **Top Performance Highlights:**
        - 🏆 **[State Name]** leads with $X.XX million in revenue
        - 👥 **[Group Name]** shows strongest demographic performance  
        - ⏰ **[Time Period]** identified as peak sales window
        - 🎯 **XX%** revenue growth opportunity identified
        """)
        
        st.markdown("### 🎯 Strategic Recommendations")
        st.markdown("""
        1. **Immediate Expansion** in top-performing states
        2. **Targeted Programs** for underperforming demographics
        3. **Operational Optimization** based on time patterns
        4. **Investment Priority** allocation for maximum ROI
        """)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.info("**Peak Performance Day:** [Day Name]")
        st.info("**Best Customer Segment:** [Group Name]")
        st.info("**Growth Opportunity:** $X.XX M")
        st.warning("**Action Required:** Underperforming states need attention")
    
    # Navigation to Analytics
    st.markdown("---")
    st.markdown("### 🔍 Dive Deeper")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 View Detailed Analytics", type="secondary", use_container_width=True):
            st.session_state.current_tab = 'Analytics'
            st.rerun()

elif st.session_state.current_tab == 'Analytics':
    st.markdown('<div class="tab-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Placeholder for analytics content
    st.info("🚧 Analytics content will be added here. This section will include:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Performance Analysis:**
        - State-wise revenue breakdown
        - Demographic group performance
        - Time-based sales patterns
        - Trend analysis & forecasting
        """)
    
    with col2:
        st.markdown("""
        **📋 Interactive Features:**
        - Filterable data tables
        - Dynamic chart selection
        - Date range pickers
        - Export capabilities
        """)
    
    # Placeholder sections for future content
    st.markdown("---")
    st.markdown("### 🏢 State Performance Analysis")
    st.empty()  # Placeholder for state charts
    
    st.markdown("---")
    st.markdown("### 👥 Demographic Analysis") 
    st.empty()  # Placeholder for demographic charts
    
    st.markdown("---")
    st.markdown("### ⏰ Time-based Analysis")
    st.empty()  # Placeholder for time charts

elif st.session_state.current_tab == 'Appendix':
    st.markdown('<div class="tab-header">📎 Appendix</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 File Upload")
        st.markdown("Upload additional files for analysis or reference:")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['csv', 'xlsx', 'pdf', 'png', 'jpg', 'txt']
        )
        
        if uploaded_files:
            st.markdown("**Uploaded Files:**")
            for file in uploaded_files:
                st.success(f"✅ {file.name} ({file.type})")
                
                # Show file preview for certain types
                if file.type == "text/csv":
                    df_preview = pd.read_csv(file)
                    st.markdown(f"**Preview of {file.name}:**")
                    st.dataframe(df_preview.head())
                elif file.type in ["image/png", "image/jpeg"]:
                    st.image(file, caption=file.name, width=300)
    
    with col2:
        st.markdown("### 💬 Comments & Notes")
        st.markdown("Add your observations, questions, or additional insights:")
        
        # Comments text area
        comments = st.text_area(
            "Your comments:",
            placeholder="Add any additional notes, observations, or questions about the analysis...",
            height=200
        )
        
        # Save comments button
        if st.button("💾 Save Comments"):
            if comments:
                # In a real app, you'd save this to a database
                st.success("✅ Comments saved successfully!")
                st.session_state.saved_comments = comments
            else:
                st.warning("⚠️ Please enter some comments before saving.")
        
        # Display saved comments
        if st.session_state.get('saved_comments'):
            st.markdown("**Previously Saved Comments:**")
            st.info(st.session_state.saved_comments)
    
    # Technical specifications section
    st.markdown("---")
    st.markdown("### 🔧 Technical Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Data Sources:**
        - AusApparalSales4thQrt2020.csv
        - 7,560 transactions
        - 6 variables analyzed
        """)
    
    with col2:
        st.markdown("""
        **Analysis Tools:**
        - Python 3.x
        - Pandas, NumPy
        - Matplotlib, Seaborn
        - Streamlit Dashboard
        """)
    
    with col3:
        st.markdown("""
        **Report Features:**
        - Interactive visualizations  
        - PDF export capability
        - Real-time data filtering
        - Multi-format file support
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
    AAL Sales Analytics Dashboard | Built with Streamlit | © 2024
    </div>
    """, 
    unsafe_allow_html=True
)

