import os
import warnings
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
# from we_src import WE_code_implementation

# ✅ Must be the first Streamlit command
st.set_page_config(
    page_title="Workforce Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Environment config to prevent Streamlit file watch errors
os.environ["STREAMLIT_WATCH_FILE_SYSTEM"] = "false"

# Initialize session state flags
if "title_matching" not in st.session_state:
    st.session_state.title_matching = False

if "task_extraction" not in st.session_state:
    st.session_state.task_extraction = False

if "final_scoring" not in st.session_state:
    st.session_state.final_scoring = False
if "title_data" not in st.session_state:
    st.session_state["title_data"] = None


st.session_state["authenticated"] = True
# Inject custom CSS to widen sidebar and resize logo
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 320px;
        }
        .sidebar-logo {
            width: 120px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# # Streamlit app configuration
# st.set_page_config(
#     page_title="Workforce Explorer",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
if st.session_state["authenticated"]:



        
    # Sidebar - Logo Upload
    # st.sidebar.title("Settings")
    st.sidebar.markdown("## 🔧 App Configuration")
    # Upload API key
    api_key = st.sidebar.text_input("🔑 Enter your API Key", type="password")
    
    # logo = st.sidebar.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    
    logo_url = "https://images.yourstory.com/cs/images/companies/2918934977141538632595807537701905017402663n-1658594922244.jpg?fm=auto&ar=1%3A1&mode=fill&fill=solid&fill-color=fff&format=auto&w=384&q=75"  # 🔁 Replace with your actual logo URL

    
#ffffff
#E3FCFC
    #f0f0f0
    # Inject CSS to control layout and logo
    st.markdown(
        """
        <style>
            /* Set background color for the entire app */
            body, .stApp {
                background-color: 	#ffffff;  /* Light gray */
                color: black; 
            }
            /* 🔷 Top title bar (Streamlit header) */
            [data-testid="stHeader"] {
                background-color: #ffffff;  /* Replace with your desired color */
                border-bottom: 1px solid #ccc;
                color: black; 
            }
    
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #E4F2F9;
                color: black;
                width: 300px;
            }

    
            .logo-container {
                display: flex;
                align-items: center;
            }
            .logo-img {
                width: 120px;
                margin-right: 10px;
            }
            .app-title {
                font-size: 32px;
                font-weight: 700;
                margin-top: 10px;
            }
            [data-testid="stSidebar"] {
                width: 300px;
            }
    
             /* Label and input text color */
            label, .stTextInput label, .stFileUploader label, .stSelectbox label {
                color: black !important;
            }
    
            /* Button text color */
            .stButton>button {
                color: black !important;
            }
            /* Custom title style */
            .custom-title {
                font-size: 30px;
                color: black;
                font-weight: 600;
                margin-top: 50px;  /* Space below logo */
                margin-left: 5px;
            }
    
    
              /* 🟢 Input components background and font color */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div > div,
            .stFileUploader > div > div {
                background-color: #f5f5f5 !important;
                color: black !important;
                border-radius: 6px;
            }
    
            /* 🔴 Download and regular button styling */
            .stButton > button,
            .stDownloadButton > button {
                background-color: #e0e0e0;
                color: black;
                border-radius: 6px;
                border: 1px solid #ccc;
                padding: 0.4em 1em;
            }
    
            /* 🔴 Button hover effect */
            .stButton > button:hover,
            .stDownloadButton > button:hover {
                background-color: #d0d0d0;
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(f'<img class="logo-img" src="{logo_url}">', unsafe_allow_html=True)

    # ✅ Custom title
    #st.markdown('<div class="custom-title">Workforce Explorer - LLM Impacts on Job Role</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-title">🤖 Workforce Explorer – LLM Impacts on Job Role</div>', unsafe_allow_html=True)



    # ✅ Step 1: Define the folder path
    data_folder = "Data/Demo_data"  # Replace with your actual folder path (relative or absolute)

    # ✅ Step 2: List all Excel files in the folder
    excel_files = [f for f in os.listdir(data_folder) if f.endswith(".xlsx")]

    options = ["-- Select a file --"] + excel_files

    # ✅ Step 3: Show dropdown to select one of the files
    uploaded_file = st.selectbox("📂 Choose an Excel file containing job titles", options)

    # ✅ Step 4: Load the selected file when user selects
    if uploaded_file and uploaded_file != "-- Select a file --":
        file_path = os.path.join(data_folder, uploaded_file)
        client_title_data = pd.read_excel(file_path)
        st.success(f"✅ Loaded file: {uploaded_file}")
        st.dataframe(client_title_data.head())  # Optional preview
    
    # # File upload
    # uploaded_file = st.file_uploader("Upload Excel File with Titles", type=["xlsx"])
    # if uploaded_file is not None:
    #     client_title_data = pd.read_excel(uploaded_file)
        st.session_state["title_data"] = client_title_data
    
        # Select company name
        company_to_query = st.text_input("Enter Company Name")
    
        # Select title column
        column_options = client_title_data.columns.tolist()
        column_options_final = ["-- Select Title Column --"] + column_options
        title_column_name = st.selectbox("Select Title Column", column_options_final)
    
        # Load Sentence Transformer Model
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        warnings.filterwarnings("ignore")

        
    # Show uploaded file preview (after upload)
    if uploaded_file and uploaded_file != "-- Select a file --" and title_column_name != "-- Select Title Column --":
    # if uploaded_file is not None:
        st.sidebar.markdown("### 📄 Uploaded Titles Preview")
        
        # Show first 5 rows
        st.sidebar.dataframe(client_title_data[[title_column_name]].head(), use_container_width=True)
        
        # Show number of unique titles
        unique_titles = client_title_data[title_column_name].nunique()
        st.sidebar.markdown(f"**🧠 Unique Titles:** `{unique_titles}`")
        
        # Download uploaded titles (optional)
        uploaded_csv = client_title_data[[title_column_name]].drop_duplicates().to_csv(index=False).encode("utf-8")
        st.sidebar.download_button("📥 Download Uploaded Titles", uploaded_csv, "uploaded_titles.csv", "text/csv")

    # Step 1: Task Extraction
    if st.session_state["title_data"] is not None:
        if st.button("🔍 Run Title Matching"):
            # title_matching_data, validated_matches, non_matched_df = WE_code_implementation.title_matching_to_database(
            #         company_to_query,
            #         client_title_data,
            #         title_column_name,
            #         model,
            #         headcount_column=None,
            #         hc_column_available=0
            #     )
            title_matching_data = pd.read_excel('Data/test_data.xlsx', sheet_name = 0)
            st.session_state["title_matching_data"] = title_matching_data
            st.session_state.title_matching = True
            st.session_state.task_extraction = False  # reset later steps
            st.session_state.final_scoring = False
        
    if st.session_state.get("title_matching", False):
        st.subheader("✅ Title Matching Results")
        # st.write(st.session_state["title_matching_data"])
        st.dataframe(st.session_state["title_matching_data"])
        csv = st.session_state["title_matching_data"].to_csv(index=False).encode("utf-8")
        st.download_button("Download Title Matching Results", csv, "title_matching.csv", "text/csv")
    # Step 2: Task Extraction
    if st.session_state.get("title_matching", False):
        if st.button("📝 Run Task Extraction"):
            task_extracted_data = pd.read_excel('Data/test_data.xlsx', sheet_name=1)
            #task_extracted_data = WE_code_implementation.task_extraction(st.session_state["title_matching_data"])
            st.session_state["task_extracted_data"] = task_extracted_data
            st.session_state.task_extraction = True
            st.session_state.final_scoring = False  # reset final scoring if re-run
    
    if st.session_state.get("task_extraction", False):
        st.subheader("✅ Extracted Tasks")
        # st.write(st.session_state["task_extracted_data"])
        st.dataframe(st.session_state["task_extracted_data"])
        task_csv = st.session_state["task_extracted_data"].to_csv(index=False).encode("utf-8")
        st.download_button("Download Extracted Tasks", task_csv, "extracted_tasks.csv", "text/csv")
    
    # Step 3: Final Scoring
    if st.session_state.get("task_extraction", False):
        if st.button("📊 Run Task Scoring"):
            final_exposure_score_table = pd.read_excel('Data/test_data.xlsx', sheet_name=2)
            #final_exposure_score_table = WE_code_implementation.task_scoring(st.session_state["task_extracted_data"], company_to_query)
            st.session_state["final_score_data"] = final_exposure_score_table
            st.session_state.final_scoring = True
    
    if st.session_state.get("final_scoring", False):
        st.subheader("✅ Final Exposure Score Table")
        # st.write(st.session_state["final_score_data"])
        st.dataframe(st.session_state["final_score_data"])
        score_csv = st.session_state["final_score_data"].to_csv(index=False).encode("utf-8")
        st.download_button("Download Exposure Score Table", score_csv, "exposure_score.csv", "text/csv")

