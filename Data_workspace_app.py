import numpy as np
import pandas as pd
import streamlit as st
import time
import io
from io import BytesIO
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chisquare
from scipy.stats import chi2_contingency as ch
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import anderson as ad
from scipy.stats import wilcoxon as wc
from scipy.stats import friedmanchisquare as fc
from scipy.stats import circmean as cm
from statsmodels.tsa.arima.model import ARIMA as AM
from statsmodels.tsa.statespace.sarimax import SARIMAX as SX
from statsmodels.tsa.statespace.varmax import VARMAX as VX
from statsmodels.duration.hazard_regression import PHReg


# page config
st.set_page_config(
  page_title="Data WorkSpace",
  page_icon="🧾",
  layout="centered"
)

#CSS Style
hide= """
  <style>
   .welcome{
    display: none;
   }
  </style>"""
hide2 ="""
  <style>
    .select_menu{
    display: none;
   }
   .list{
    display: none; 
   }
   .title{
    display: none;
   }
  </style>
"""
subtitle ="""
  <style>
   .subtitle{
    display: none;
   }
  </style>"""
btn = """
  <style>
   .st-key-btn{
    display: none;
   }
  </style>"""


# welcome page
welcome = st.markdown('<h2><marquee direction="left" class="welcome" style="background-color: skyblue");">Welcome To All-in-One Data Workspace and MY Official Portfolio. Turn Raw Data into Clear, Actionable Insight; Faster and Smarter. Let\'s Get Started!</marquee></h2>' \
'<p class="welcome" style="text-align: justify;">This app is built for professionals who work with data every day and need results without friction. Whether your data comes messy, incomplete, or in different formats, this platform helps you clean, analyse, visualise, and convert files seamlessly.</p>'
'<p class="welcome" style="text-align: justify;">From row data to meaningful stories, this app supports every step of your data journey. Click the <a href="https://selar.com/n461o6yn1l", class="welcome">Link</a> to learn more about Data Analysis.</p>'\
'<p style="text-align: justify;"><strong class="welcome">Upload your data and start transforming information into impact.</strong></p> ', unsafe_allow_html=True) 
image_placeholder = st.empty()
image_placeholder.image("book.jpg", caption="The Book that teaches you Data Analysis (Click the Link Above)")

# start button
if "started" not in st.session_state:
  st.session_state.started = False
if st.button("GET STARTED", key= 'btn'):
  st.session_state.started = True
if st.session_state.started:
  # Hide menu 
  st.markdown(hide, unsafe_allow_html=True)
  st.markdown(btn, unsafe_allow_html=True)
  image_placeholder.empty()
  st.markdown("<h3 class='title'>Process Your Data: Turn Your Data into Insight</h3>", unsafe_allow_html=True)

  menu = ['Choose Option', 'Data Analysis', 'Data Cleaning', 'Data Visualization', 'Convert Your Files', 'About App', 'My Portfolio']
  # menu to select from
  select_menu = st.selectbox("Select Menu to Talk to Your Data: ", menu)

  # Markdown note 
  st.markdown(
    '<div class ="select_menu">Select from the Menu above to Perform:</div>\n' \
    '<div class="list">1. Data Analysis</div>\n' \
    '<div class="list">2. Data Cleaning </div>\n' \
    '<div class="list">3. Data Visualization </div>\n' \
    '<div class="list">4. About the App & Portfolio</div>\n' \
    '<div class="list">5. Convert Your File To Excel or CSV </div>',
    unsafe_allow_html=True
  )
  
  # Data Cleaning 
  if select_menu == 'Data Cleaning':
    # hide2
    st.markdown(hide2, unsafe_allow_html=True)
    #title
    st.markdown("<h2 class='subtitle'>🧹 Clean Your Dataset</h2>", unsafe_allow_html=True)
    column1, column2 = st.columns(2)

    # upload file 
    st.sidebar.subheader("📂 Upload file to start cleaning")
    upload_file = st.sidebar.file_uploader("Upload a File", type=['csv', "xlsx"])
    
    # condition to upload file 
    if upload_file != None:

      # success message 
      st.sidebar.success('✅ File Upload successfully!')
      
      # read file 
      if upload_file.name.endswith(".csv"):
        df1 = pd.read_csv(upload_file)
      else:
        df1 = pd.read_excel(upload_file)

      # df1 = pd.read_csv(upload_file)
      cleaning = [ 'Select Option', 'Handle Duplicates', 'Handle Missing values', 'Covert Column Types']
      clean_option = st.sidebar.selectbox("cleaning option:", cleaning)

      # copy original data 
      cleaned_df = df1.copy()

      # show dataset
      if st.sidebar.checkbox('Show Dataset'):
        st.write(cleaned_df)

      
      if st.sidebar.checkbox("Check✅ Delete Row and Column"):
        try:
          # st.subheader('Your Dataset')
          # st.write(df1)
          # functin to ignore duplicate headers 
          def remove_duplicate_headers(headers):
            unique_headers = []
            seen = set()
            for col in headers:
              col = str(col).strip()

              # replace empty column names 
              if col == "" or col.lower() == "nan":
                col = "column"

              # ignore duplicate coulumn names 
              if col not in seen:
                unique_headers.append(col)
                seen.add(col)
            return unique_headers
          
          if "clean_df" not in st.session_state:
            if upload_file.name.endswith(".csv"):
              st.session_state.clean_df = pd.read_csv(upload_file)

            else:
              st.session_state.clean_df = pd.read_excel(upload_file)

          clean_df = st.session_state.clean_df

          st.subheader("Dataset Preview")
          st.dataframe(clean_df, use_container_width=True)
          st.write(f"Dataset Rows and Column{clean_df.shape}")

          st.markdown("-----")

          if st.sidebar.checkbox("Delete Header Row"):
            # Delete header 
            st.subheader("Delete header row")
            st.info(
              "This will remove the current column header and use the first data row as new headers"
            )
            if st.sidebar.button("Delete Header Row"):
              try:
                
                # Use first row as new header 
                new_header = clean_df.iloc[0].tolist()

                # remove dupcate headers
                unique_header = remove_duplicate_headers(new_header)

                # keep only unique columns 
                keep_indexes = []
                seen = set()

                for idx, col in enumerate(new_header):
                  col = str(col).strip()

                  if col == "" or col.lower() == "nan":
                    col = "column"

                  if col not in seen:
                    keep_indexes.append(idx)
                    seen.add(col)
                
                # remove first row 
                clean_df = clean_df.iloc[1:, keep_indexes].copy()

                # assign new header 
                clean_df.columns = unique_header

                # reset index 
                clean_df.reset_index(drop=True, inplace=True)

                # save updated dataframe
                st.session_state.clean_df = clean_df
                st.success("✅ Header row deleted successfully.")

              except Exception as e:
                st.error(f"Error: {e}")

            # Delete column 
          if st.sidebar.checkbox("Delete Column"):
            st.subheader("Delete Column")

            selected_columns = st.sidebar.multiselect(
              "Select columns to delete",
              clean_df.columns.tolist()
            )

            if st.sidebar.button("Delete selected Columns"):
              if selected_columns:
                st.session_state.clean_df = clean_df.drop(columns=selected_columns)
                st.success("✅ Selected columns delected successfully")

                # refresh dataframe variable 
                clean_df = st.session_state.clean_df
              
              else:
                st.warning("Please select column")

            # Delete Rows
          if st.sidebar.checkbox("Delete Row"):
            st.subheader("Delete Rows")

            st.sidebar.write("Select row indexes to delete")

            selected_rows = st.sidebar.multiselect(
              "choose row indexes",
              clean_df.index.tolist()
            )

            if st.sidebar.button("Delete Selected Rows"):

              if selected_rows:
                st.session_state.clean_df = clean_df.drop(index=selected_rows)

                # Reset index after deleting 
                st.session_state.clean_df.reset_index(drop=True, inplace=True)

                st.success("✅ Selected Rows delected Successfully.")

                # refresh dataframe variable  
                clean_df = st.session_state.clean_df

              else:
                st.warning("Please select rows")
          
          st.markdown("----")

          # updated dataset 

          st.subheader("Updated Dataset")
          st.dataframe(st.session_state.clean_df, use_container_width=True)
          st.info("Download updated dataset, upload back and start analysis")

          # Download clean Dataset 
          csv = st.session_state.clean_df.to_csv(index=False).encode("utf-8")

          st.download_button(
            label="Download Updated Dataset",
            data=csv,
            file_name="Updated_dataset.csv",
            mime="text/csv"
          )
        except Exception as e:
          st.error(f"❌ An error occured: {e}")

      # Handle mising values
      if clean_option == "Handle Missing values":
        st.markdown(subtitle, unsafe_allow_html=True)
        # check for missing value
        if st.sidebar.checkbox("Check Missing value"):
          st.subheader("Number of Missing Values")
          st.write(cleaned_df.isna().sum())
          
        # drop the missing value 
        if st.sidebar.button("Click To Drop the Missing Value"):
          cleaned_df = cleaned_df.dropna()
          with st.spinner("Droping Missing Values,please wait..."):
            time.sleep(10)
          st.toast('✅ You Successfully dropped all missing values!')
          st.subheader("✅ Cleaned Data")
          st.write(cleaned_df)
          st.write(f"Dataset New Rows and Column{cleaned_df.shape}")

          # download cleaned data 
          def convert_df_to_csv(dataframe):
            return dataframe.to_csv(index=False).encode('utf-8')

          csv_data = convert_df_to_csv(cleaned_df)

          st.download_button(
            label="📥 Download Cleaned Data as CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
          )


        # replace missing value 
        missing = ['Select Option', 'Replace with Mean value', 'Replace with Mannual input and all missing value']
        select_missing = st.sidebar.selectbox("Select Option to replace missing values:", missing)
        
        # replace with manual input 
        if select_missing == 'Replace with Mannual input and all missing value':
          input_value = st.sidebar.text_input("Input Value To Replace missing values:")
          if input_value == str():
            st.sidebar.warning('⚠️ Input Values and Press Enter Key to Replace')
          else:
            select_column_to_replace = st.sidebar.selectbox("Select Column To Replace Missing Value in the Specific Column:", cleaned_df.columns)
            if st.sidebar.button("Click Replace All Missing Values"):
              cleaned_df[select_column_to_replace] = cleaned_df[select_column_to_replace].fillna(input_value)
              st.toast('You Successfully replace All missing values!!', icon=':material/settings:')
              st.subheader("✅ Cleaned Data")
              st.write(cleaned_df)
              st.write(f"Dataset New Rows and Column{cleaned_df.shape}")
          
              # download cleaned data 
              def convert_df_to_csv(df):
                csv = df.to_csv(index=False)
                return BytesIO(csv.encode())
              
              csv_bytes = convert_df_to_csv(cleaned_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )

              # replace specific column 
            elif st.sidebar.button(f"Click To Replace Missing Value in {select_column_to_replace}"):
              cleaned_df[select_column_to_replace] = cleaned_df[select_column_to_replace].fillna(input_value)
              st.toast(f'You Successfully replace missing values in the Column {select_column_to_replace}!!', icon=':material/thumb_up:')
              st.subheader("✅ Cleaned Data")
              st.write(cleaned_df)
              st.write(f"Dataset New Rows and Column{cleaned_df.shape}")
          
              # download cleaned data 
              def convert_df_to_csv(dataframe):
                return dataframe.to_csv(index=False).encode('utf-8')

              csv_data = convert_df_to_csv(cleaned_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )

              

          # replace with mean 
        elif select_missing == 'Replace with Mean value':
          numeric_cols = df1.select_dtypes(include=['float64', 'int64']).columns.tolist()
          select_mean_column = st.sidebar.selectbox("Select Column To get the Mean value:", numeric_cols)
          select_column_for_mean_rep = st.sidebar.selectbox("Select Column To Replace Missing with the Mean value:", df1.columns)
          mean_cal = df1[select_mean_column].mean()
          

          # replace all
          try:
            if st.sidebar.button("Click Replace All Missing Values with Mean"):
              cleaned_df = cleaned_df.fillna(f'{mean_cal:.2f}')
              st.toast('You Successfully replace All missing values with Mean!!', icon=':material/settings:')
              st.subheader("✅ Cleaned Data")
              st.write(cleaned_df)

              # download cleaned data 
              def convert_df_to_csv(df):
                csv = df.to_csv(index=False)
                return BytesIO(csv.encode())
              
              csv_bytes = convert_df_to_csv(cleaned_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )

              # replace specific column 
            elif st.sidebar.button(f"Click To Replace Missing  with Mean in {select_column_for_mean_rep}"):
              cleaned_df[select_column_for_mean_rep] = cleaned_df[select_column_for_mean_rep].fillna( f'{mean_cal:.2f}')
              st.toast(f'You Successfully replace missing values with Mean in the Column {select_column_for_mean_rep}!!', icon=':material/thumb_up:')
              st.subheader("✅ Cleaned Data")
              st.write(cleaned_df)
              # download cleaned data 
              def convert_df_to_csv(df):
                csv = df.to_csv(index=False)
                return BytesIO(csv.encode())
              
              csv_bytes = convert_df_to_csv(cleaned_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )    
          except Exception as e:
            st.error(f"❌ An error occured: {e}")


        

      
        # Handle duplicated values 
      elif clean_option == "Handle Duplicates":
        st.markdown(subtitle, unsafe_allow_html=True)
        handle_dup = ['Choose Method','Handle Duplicate from the First Column','Handle Duplicate from the Select Column' ]
        handle_sel = st.sidebar.selectbox('Choose Method to Handle Duplicates', handle_dup)

        # from the first column 
        if handle_sel == 'Handle Duplicate from the First Column':
          duplicated = df1.duplicated().sum()
          st.metric(label="**Duplicate Value:**", value=f"{duplicated}")
          # drop duplicated values
          st.sidebar.subheader("The button below drop duplicates from the first column of the dataset")
          if st.sidebar.button("Drop Duplicated Values"):
            cleaned_df = cleaned_df.drop_duplicates()
            with st.spinner("Duplicates dropping, please wait..."):
              time.sleep(10)
              st.toast("Duplicates successfully dropped!", icon=':material/thumb_up:')
              st.write(cleaned_df)
              st.write(f"Dataset New Rows and Column{cleaned_df.shape}")
            
              # download cleaned data 
              def convert_df_to_csv(dataframe):
                return dataframe.to_csv(index=False).encode('utf-8')

              csv_data = convert_df_to_csv(cleaned_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )

        #  from the selected column 
        elif handle_sel == 'Handle Duplicate from the Select Column':
          #select column to check duplicate
          select_column = st.sidebar.selectbox("Select Column to check duplicate:", cleaned_df.columns)
          show_dupl = cleaned_df[select_column].duplicated().sum()
          st.metric(label=f"**Duplicate Values from {select_column}:**", value=f"{show_dupl}")
          # drop dupicate from the selected column 
          if st.sidebar.button(f"Drop Duplicated Values from {select_column}"):
            clean_df = cleaned_df.drop_duplicates(subset=[select_column])
            with st.spinner("Duplicates dropping, please wait..."):
              time.sleep(10)
              st.toast("Duplicates successfully dropped!", icon=':material/thumb_up:')
              st.write(clean_df)
              st.write(f"Dataset New Rows and Column{clean_df.shape}")
            
              # download cleaned data 
              def convert_df_to_csv(dataframe):
                return dataframe.to_csv(index=False).encode('utf-8')

              csv_data = convert_df_to_csv(clean_df)

              st.download_button(
                label="📥 Download Cleaned Data as CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
              )
        

        # convert types
      elif clean_option == 'Covert Column Types':
        st.markdown(subtitle, unsafe_allow_html=True)
        convert_type = ['Select Option', 'To Date Type', 'To Numeric Type']
        select_convert = st.sidebar.selectbox("Select Convert Type:", convert_type)
        # convert to date type 
        if select_convert == 'To Date Type':
          select_column_convert = st.sidebar.selectbox("Select Column to convert:", df1.columns)
          if st.sidebar.button("Convert To Date Type"):
            df1[select_column_convert] = pd.to_datetime(df1[select_column_convert], errors='coerce')
            st.toast('Successfully Change to Date Format', icon=':material/settings:')
            st.write(df1)

            # download cleaned data 
            def convert_df_to_csv(dataframe):
              return dataframe.to_csv(index=False).encode('utf-8')

            csv_data = convert_df_to_csv(df1)

            st.download_button(
              label="📥 Download Data as CSV",
              data=csv_data,
              file_name="My_data.csv",
              mime="text/csv"
            )

        # covert to numeric type 
        if select_convert == 'To Numeric Type':
          select_column_convert = st.sidebar.selectbox("Select Column to convert:", df1.columns)
          if st.sidebar.button("Convert To Numeric Type"):
            df1[select_column_convert] = pd.to_numeric(df1[select_column_convert], errors='coerce')
            st.toast('Successfully Change to Number Format', icon=':material/settings:')
            st.write(df1)
            # download cleaned data 
            def convert_df_to_csv(dataframe):
              return dataframe.to_csv(index=False).encode('utf-8')

            csv_data = convert_df_to_csv(df1)

            st.download_button(
              label="📥 Download Data as CSV",
              data=csv_data,
              file_name="My_data.csv",
              mime="text/csv"
            )

          
    # CONVERT YOUR FILES
  elif select_menu == 'Convert Your Files':
    # Hide menu  
    st.markdown(hide2, unsafe_allow_html=True)
    #title
    st.markdown("<h2 class='subtitle'>Convert Your Files</h2>", unsafe_allow_html=True)
    column1, column2 = st.columns(2)

    # select to file 
    Select_file = ['Select Option','Excel To CSV', 'CSV To Excel']
    select_files = st.sidebar.selectbox("Select File TO Convert:",  Select_file)


    # EXCEL TO CSV 
    if select_files == "Excel To CSV":
      # hide subtitle
      st.markdown(subtitle, unsafe_allow_html=True)
      # upload file 
      st.sidebar.subheader("📂Upload Excel file to Convert")
      upload_file = st.sidebar.file_uploader("Upload an Excel File", type=['xlsx'])

      if upload_file != None:
        st.sidebar.success("✅ File Uploaded Successfully!")

        # read file 
        df2 = pd.read_excel(upload_file)

        # show dataset
        if st.sidebar.checkbox('Show Dataset'):
          st.write(df2)
        
        # convert to CSV
        if st.sidebar.checkbox('Download To CSV'):
          @st.cache_data
          def convert_excel_to_csv(dataframe):
            return dataframe.to_csv(index=False)
          csv_data = convert_excel_to_csv(df2)
          st.download_button(
            label= "📥 Download data as CSV",
            data= csv_data,
            file_name= "my_csv.csv",
            mime='text/csv'
          )

        
    # CSV TO EXCEL 
    elif select_files == "CSV To Excel":
      # hide subtitle
      st.markdown(subtitle, unsafe_allow_html=True)

      # upload file 
      st.sidebar.subheader("📂 Upload CSV file to Convert")
      upload_file = st.sidebar.file_uploader("Upload a CSV File", type=['csv'])

      if upload_file != None:
        st.sidebar.success("✅ File Uploaded Successfully!")

        # read file 
        df3 = pd.read_csv(upload_file)

        # show dataset
        if st.sidebar.checkbox('Show Dataset'):
          st.write(df3)
        
        if st.sidebar.checkbox('Download to Excel'):
          def to_excel(df3):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df3.to_excel(writer, index=False, sheet_name = 'Sheet1')
            writer.close()
            processsed_data = output.getvalue()
            return processsed_data
          st.download_button(
            label='📥 Download data as Excel',
            data= to_excel(df3) ,
            file_name= 'My_excel.xlsx',
            mime='application/vnd.opnxmlformats-offcedocument.spreadsheetml.sheeet'
          )


    # DATA ANALYSIS 
  elif select_menu == 'Data Analysis':
    # Hide menu 
    st.markdown(hide2, unsafe_allow_html=True)
    #title
    st.markdown("<h2 class='subtitle'>Perform Data Analysis</h2>", unsafe_allow_html=True)
    # st.title("Perform Data Analysis")
    column1, column2 = st.columns(2)

    # upload file 
    st.sidebar.subheader("📂 Upload File to Start Analysis")
    upload_file = st.sidebar.file_uploader("Upload a File", type=['csv', "xlsx"])
    
    # condition to upload file 
    if upload_file != None:

      # success message 
      st.sidebar.success('✅ File Upload successfully!')
      
      # read file 
      if upload_file.name.endswith(".csv"):
        df4 = pd.read_csv(upload_file)
      else:
        df4 = pd.read_excel(upload_file)
      text = """"
        Descriptive statistics generally means describing the data with the help of some representative methods.
        Hypothesis testing involves using statistical tools to evaluate claims about a population based on sample data. 
      """
      analysis = [ 'Select Option', 'Descriptive Statistics', 'Hypothesis Testing', 'Confidence Intervals', 'Correlation and Regression', 'Circular Mean', 'Time Series Analysis', 'Survival Analysis']
      analy_option = st.sidebar.selectbox("Analysis option:", analysis, help=text)

      # show dataset  
      if st.sidebar.checkbox("Show Dataset"):
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        st.subheader('Your Dataset')
        st.write(df4)
        st.write(f'**Dateset Rows and Columns: {df4.shape}**')
      

      # descriptive statistics
      if analy_option == 'Descriptive Statistics':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        if st.sidebar.checkbox('Summary Statistic:'):
          st.write(df4.describe(include='all').T)
        descri = ['Select Option', 'Average/Mean', 'Median', 'Standard Deviation','Groupby']
        descri_menu = st.sidebar.selectbox("Select Option for Descriptive:", descri )

        # average/mean 
        if descri_menu == 'Average/Mean':
          aver_column = st.sidebar.selectbox("select Column for Average/Mean", df4.columns)
          # check if the column is numeric type
          if pd.api.types.is_numeric_dtype(df4[aver_column]):
            if st.sidebar.button('Get Average/Mean'):
              aver_mean = df4[aver_column].mean()
              st.metric(label=f"**The Average/Mean of {aver_column} is:**", value=f"{aver_mean :.2f}")
          else:
            st.warning("⚠️ Choose a Numerical Column To Get the Average/Mean")

          # find Median
        elif descri_menu == 'Median':
          median_column = st.sidebar.selectbox("select Column for Median", df4.columns)
          # check if the column is numeric type
          if pd.api.types.is_numeric_dtype(df4[median_column]):
            if st.sidebar.button('Get Median'):
              media = df4[median_column].median()
              st.metric(label=f"**The Average/Mean of {median_column} is:**", value=f"{media :.2f}")
          else:
            st.warning("⚠️ Choose a Numerical Column To Get Median")

          # standard deviation 
        elif descri_menu == 'Standard Deviation':
          std_column = st.sidebar.selectbox("select Column for Standard Deviation", df4.columns)
          # check if the column is numeric type
          if pd.api.types.is_numeric_dtype(df4[std_column]):
            if st.sidebar.button('Get STD'):
              std = df4[std_column].std()
              st.metric(label=f"**The Average/Mean of {std_column} is:**", value=f"{std :.2f}")
          else:
            st.warning("⚠️ Choose a Numerical Column To Get Standard Deviation")

          # groupby
        elif descri_menu == 'Groupby':
          group_op = ['Select Option', 'Groupby Total', 'Groupby Average']
          grp_option = st.sidebar.selectbox("Choose Grouping Options:", group_op)

          # Groupby sum
          if grp_option == 'Groupby Total':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            Gb_cat_column = st.sidebar.selectbox("select Categorical Column To Groupby:", categorical_cols)
            Gb_num_column = st.sidebar.selectbox("select Value Column For the Group:", numeric_cols)
            if st.sidebar.button("Groupby"):
              grpby = df4.groupby(Gb_cat_column)[Gb_num_column].sum().sort_values(ascending=False)
              # subheader
              st.subheader(f'Top {Gb_num_column} by {Gb_cat_column}')
              # show groupy
              st.dataframe(grpby)
              # visualization
              st.subheader(f'Chart Showing Top {Gb_num_column} by {Gb_cat_column}')
              st.bar_chart(grpby)
              
              # groupby average
          elif grp_option == 'Groupby Average':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            Gb_cat_column = st.sidebar.selectbox("select Categorical Column To Groupby:", categorical_cols)
            Gb_num_column = st.sidebar.selectbox("select Value Column For the Group:", numeric_cols)
            if st.sidebar.button("Groupby"):
              grpby_avg = df4.groupby(Gb_cat_column)[Gb_num_column].mean().sort_values(ascending=False)
              # subheader
              st.subheader(f'Average {Gb_num_column} by {Gb_cat_column}')
              # show groupy
              st.dataframe(grpby_avg)
              # visualization
              st.subheader(f'Chart Showing Average {Gb_num_column} by {Gb_cat_column}')
              st.bar_chart(grpby_avg)
          
          

        # Hypothesis testing
      elif analy_option == 'Hypothesis Testing':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        text_box = """
          \nT-tests: This comparing the means of one or two samples\n.
          \nANOVA Test: allows performing ANOVA (Analysis of Variance) tests.
          \n Chi-square Test: allows performing chi-square test.
          \n Normality Test: These determine whether a given dataset significantly deviates from a normal distribution.
        """
        hyp = ['Select Option', 'T-test', 'ANOVA-test','Chi-square test','Normality Test', 'Non-parametric Test']
        select_hyp = st.sidebar.selectbox("Select Option For H-Testing:", hyp, help=text_box)

        # T-test 
        if select_hyp == 'T-test':
          tt = ['Select Option','One-Sample T-test', 'Two-Sample T-test']
          select_tt = st.sidebar.selectbox("Select Option For T-testing:", tt)

          # One-sample t-test 
          if select_tt == 'One-Sample T-test':
            onesamp_column = st.sidebar.selectbox("select Column for One-sample T-test", df4.columns)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("0.05 is usual used for significant level")
            if pd.api.types.is_numeric_dtype(df4[onesamp_column]):
              try:
                if st.sidebar.button('Run One-sample T-test'):
                  if sign_levl == str():
                    st.warning("⚠️ Choose Significant Level (Numeric Values) and Press Enter Key to Proceed.")
                  else:
                    s_data = df4[onesamp_column]
                    s_mean = s_data.mean()
                    t_stat, p_value = stats.ttest_1samp(s_data, s_mean)
                    st.subheader('📊 **Results of One-sample T-test**')
                    # st.code(f'**T-statistics:** {t_stat}')
                    # st.code(f'**P-value:** {p_value}')
                    st.metric(label="**T-statistics:**", value=f"{t_stat}")
                    st.metric(label="**P-value:**", value=f"{p_value}")
                    # Decision and interpret result
                    st.subheader("🧾 Interpretation")
                    st.markdown(
                      f'•	If P-value < {sign_levl}, reject the null hypothesis. This suggests there is statistically significant evidence to reject the null hypothesis.\n' \
                      f'\n•	If P-value ≥ {sign_levl}, accept the null hypothesis. This means there is not enough evidence to reject the null hypothesis.'
                      '\n<a href="https://selar.com/n461o6yn1l">ReadMore on T-test</a>', unsafe_allow_html=True
                    )
                    if p_value < float(sign_levl):
                      st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: the difference is statistically significant.")
                    else:
                      st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: No significant difference.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")       
            else:
                st.warning("⚠️ Choose a Numerical Column For One-sample T-test")
          
            # two-sample t-test
          elif select_tt == 'Two-Sample T-test':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            select_val = st.sidebar.selectbox('Select Categorical Variable Column:', categorical_cols)
            select_cat1 = st.sidebar.selectbox('Select Variable One: ', df4[select_val].unique())
            select_cat2 = st.sidebar.selectbox('Select Variable Two: ', df4[select_val].unique())
            select_mean = st.sidebar.selectbox('Select Column for mean comparism:', numeric_cols)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level!")
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button('Run Two-sampe T-test'):
                  samp1 = df4[df4[select_val] == select_cat1] [select_mean]
                  samp2 = df4[df4[select_val] == select_cat2] [select_mean]
                  t_stat, p_value = stats.ttest_ind(samp1, samp2)
                  st.subheader("📊 **Results of Two-sample T-test**")
                  # st.code(f'T-statistics: {t_stat}')
                  st.metric(label="**T-statistics:**", value=f"{t_stat:.2f}")
                  st.metric(label="**P-value:**", value=f"{p_value:.2f}")
                  # st.code(f'P-value: {p_value}')
                  st.subheader("🧾 Interpretation")
                  st.markdown(
                    f'Significant Level Used = {sign_levl} \n'
                    f'\n•	If P-value < {sign_levl}, the difference is statistically significant in means.\n' \
                    f"\n•	If P-value ≥ {sign_levl}, this means there’s not much statistically significant difference in means.\n"
                    '\n <a href="https://selar.com/n461o6yn1l">ReadMore on T-test</a>', unsafe_allow_html=True
                  )
                  
                  if p_value < float(sign_levl):
                    st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: the difference is statistically significant in means.")
                  else:
                    st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: No significant difference in means.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")

          # ANOVA
        elif select_hyp == 'ANOVA-test':
          text_anv = '''
            \nOne-way ANOVA is used to compare the means of three or more independent groups based on one independent variable
            \nTwo-Way ANOVA is used when you have two independent variables and want to examine effect on a dependent variable.
          '''
          anv = ['Select Option','One-way ANOVA', 'Two-way ANOVA']
          select_anv = st.sidebar.selectbox('Select Option for ANOVA:', anv, help=text_anv)
          # one way anova 
          if select_anv == 'One-way ANOVA':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            if not numeric_cols:
              st.error("❌ No numerical found")
            elif not categorical_cols:
              st.error('❌ No Categorical found')
            else:
              dependent_var = st.sidebar.selectbox('select dependent Variable(Numeric):', numeric_cols)
              group_var = st.sidebar.selectbox('select the grouping Variable(Categorical):', categorical_cols)
            # step 3 perfrom one way anova 
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button('Run One-way ANOVA'):
                  groups =[]
                  for level in df4[group_var].dropna().unique():
                    group_data = df4[df4[group_var] == level][dependent_var].dropna()
                    groups.append(group_data)
                  if len(groups) <= 2:
                    st.warning('⚠️ You need at least three or more groups to perform One-way ANOVA')
                  else:
                    f_stat, p_val = stats.f_oneway(*groups)
                    st.subheader("📊 One-way ANOVA Results")
                    st.write(f'**Dependent Variable:** {dependent_var}')
                    st.write(f'**Groupping Variable:** {group_var}')
                    st.write(f'**Number of Groups:** {len(groups)}')

                    st.metric(label="**F-statistic:**", value=f"{f_stat: .4f}")
                    st.metric(label="**P-value:**", value=f"{p_val: .6f}")
                    st.subheader("🧾 Interpretation")
                    st.markdown( f'•	If <b>P-value < {sign_levl}</b>, the difference is statistically significant.\n' \
                    f'\n•	If <b>P-value ≥ {sign_levl}</b>, this means there\'s no much statistically significant difference.\n' \
                    '\n<a href="https://selar.com/n461o6yn1l">ReadMore On ANOVA</a>', unsafe_allow_html=True)
                    if p_val < float(sign_levl):
                      st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: the difference is statistically significant.")
                    else:
                      st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: No significant difference.")
                    # visualization to interprete the rusult 
                    # box plot for groups distribution 
                    st.subheader(f"📊 {group_var} Distributions")
                    fig1, ax1 = plt.subplots()
                    sns.boxplot(x=df4[group_var], y=df4[dependent_var], ax=ax1)
                    ax1.set_xlabel(group_var)
                    ax1.set_ylabel(dependent_var)
                    ax1.set_title(f"Distribution of {group_var}")
                    st.pyplot(fig1)

                    # bar chart 
                    st.subheader(f'📊 {group_var} Group Means')
                    group_means = df4.groupby(group_var)[dependent_var].mean()
                    fig2, ax2 = plt.subplots()
                    ax2.bar(group_means.index.astype(str), group_means.values)
                    ax2.set_xlabel(group_var)
                    ax2.set_ylabel(f'Mean of {dependent_var}')
                    ax2.set_title(f"Mean Camparison Across {group_var} Groups")
                    st.pyplot(fig2)
              except Exception as e:
                st.error(f"❌ An error occured: {e}")


            # Two-way ANOVA 
          elif select_anv == 'Two-way ANOVA': 
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            if len(numeric_cols)< 1:
              st.error("❌ No Numeric Column found for dependent variable")
              st.stop()
            elif len(categorical_cols)< 2:
              st.error("❌ At least Two categorical column are required for a two way Anova")
              st.stop()
            else:
              depend = st.sidebar.selectbox("dependent Variable:", numeric_cols)
              factor1 = st.sidebar.selectbox("Independent Variable-1", categorical_cols)
              remaining_cats = [col for col in categorical_cols if col != factor1]
              factor2 = st.sidebar.selectbox("Independent Variable-2", remaining_cats)
              if sign_levl == str():
                st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
              else:
                if st.sidebar.button("Run Two Way ANOVA"):
                  try:
                    # drop missing value 
                    clean_df = df4[[depend, factor1, factor2]].dropna()
                    if clean_df.shape[0]<3:
                      st.error("❌ Not enough Observations after removing missing values.")
                      st.stop()
                    # ensure categorical type 
                    clean_df[factor1] = clean_df[factor1].astype("category")
                    clean_df[factor2] = clean_df[factor2].astype("category")
                    # check level 
                    if clean_df[factor1].nunique()<2:
                      st.error(f"❌ {factor1} must have at least 2 levels.")
                      st.stop()
                    if clean_df[factor2].nunique()<2:
                      st.error(f"❌ {factor2} must have at least 2 levels.")
                      st.stop()
                    
                    # handle column name with spaces/special characters safely 
                    safe_df = clean_df.copy()
                    safe_df.columns = [col.replace(" ", "_") for col in safe_df.columns]
                    dep = depend.replace(" ","_")
                    f1 = factor1.replace(" ","_")
                    f2 = factor2.replace(" ","_")
                    # Build formula safely (with interaction)
                    formula = f'Q("{dep}") ~ C(Q("{f1}")) + C(Q("{f2}")) + C(Q("{f1}")):C(Q("{f2}"))'
                    model = ols(formula, data=safe_df).fit()
                    # anova table 
                    anova_table = sm.stats.anova_lm(model, typ=2)
                    st.subheader('📊 Two-way ANOVA Results Table')
                    st.write(f"Dependent Variable: **{depend}**")
                    st.write(f"Factors: **{factor1}**, **{factor2}**")
                    st.dataframe(anova_table)
                    st.subheader("🧾 Interpretation")
                    st.markdown('<strong>Interpretation of Results</strong>\n' \
                    f'\nCompare the <b>p-value</b> for each main effect and the interaction term to your chosen significant level {sign_levl}, if  <b>P-value < {sign_levl}</B> indicates a statistically significant effect, then focus on the interaction first; if it’s significant, the effects of your factors are dependent on each other, requiring a look at interaction simple main effects to understand the specific differences. If the interaction is not significant, interpret the main effects individually to see if each independent variable independently affects the dependent variable. <a href="https://selar.com/n461o6yn1l">Read More on ANOVA</a>.', unsafe_allow_html=True)
                  except ValueError as ve:
                    st.error(f"❌ Value error: {ve}")

                  except Exception as e:
                    st.error(f"❌ An error occured: {e}")
                

          # Chi-square test 
        elif select_hyp == 'Chi-square test':
          text_chi = '''
            \nChi-square Goodness-of-fit test: determines if the observed frequency distribution significantly differs from an expected distribution.
            \nChi-square test for independence: assesses whether there is a statistically significant association between two categorical variable, and it uses a contingency table to observed frequencies.
          '''
          chi = ['Select Option','Chi-square Goodness-of-fit test', 'Chi-square test for independence']
          select_chi = st.sidebar.selectbox('Select Option for Chi-square test:', chi, help=text_chi)

          # chi-square goodness-of-fit test 
          if select_chi == 'Chi-square Goodness-of-fit test':
            
            # Initialize observed and expected arrays
            observed, expected = None, None

            
            try:
              # select column
              numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
              cat_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
              obv = st.sidebar.selectbox('select Observed Frequency', numeric_cols)
              exp = st.sidebar.selectbox('select Expected Frequency', numeric_cols)
              category = st.sidebar.selectbox('select categories', cat_cols)
              sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
              st.sidebar.info("❎ 0.05 is usual used for significant level")

              # Validate column names
              if obv in df4.columns and exp in df4.columns:
                observed = df4[obv].values
                expected = df4[exp].values
                # st.success("✅ Successfully loaded data from CSV.")
              else:
                st.error("❌ CSV must contain columns named 'Observed' and 'Expected'.")
            except Exception as e:
              st.error(f"❌ Error reading file: {e}")


            # Button to run the test
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              if st.sidebar.button("Run Chi-Square Goodness-of-fit Test"):
                try:
                  # Perform Chi-square test
                  chi_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

                  # Display results
                  st.subheader("📊 Goodness-of-fit Test Results")
                  st.write(f"**Chi-Square Goodness-of-fit Statistic (χ²):** {chi_stat:.4f}")
                  st.write(f"**Degrees of Freedom (df):** {len(observed) - 1}")
                  st.write(f"**P-value:** {p_value:.4f}")

                  # Interpretation
                  st.subheader("🧾 Interpretation")
                  st.markdown(f'•	If <b>p-value < {sign_levl}</b>, the observed distribution is significantly different from the expected.\n'
                  f'\n•	If <b>p-value ≥ {sign_levl}</b>, there is no significant difference between observed and expected frequencies.\n'
                  '\n<a href="https://selar.com/n461o6yn1l">Read more on Chi-square Goodness-of-fit test</a>', unsafe_allow_html=True)
                  if p_value < float(sign_levl):
                    st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: Observed frequencies differ significantly from expected frequencies.")
                  else:
                    st.info("❎ In this case; Fail to reject the null hypothesis: No significant difference between observed and expected frequencies.")
                except ValueError:
                  st.error("⚠️ Please enter valid column for frequencies.")
                except Exception as e:
                  st.error(f"❌ An error occured: {e}")

            # chi-square independence 
          elif select_chi == 'Chi-square test for independence':
            # chisquare test for independence second way
            num_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            cat_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            cat = st.sidebar.selectbox('Select Categorical variables', cat_cols)
            nume = st.sidebar.selectbox('Select Observed Variable',num_cols)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button("Run Chi-square Independence"):
                  # contigency table
                  contigency_table = pd.crosstab(df4[cat], df4[nume])
                  # perform chi-sqaure
                  chi_stat, p_value,dof, expected_fre = ch(contigency_table)
                  st.subheader("📊 Result of Chi-square Independence")
                  st.write(f"**chi-square Independence statistics:** {chi_stat}")
                  st.write(f"**p_value:** {p_value}")
                  st.write(f"**Degree of freedom:** {dof}")
                  st.write(f"**expected frequency:** {expected_fre}")
                  

                  # Interpretation
                  st.subheader("🧾 Interpretation")
                  st.markdown(f'•	If <b>p-value < {sign_levl}</b>, there is a significant association between {cat}.\n'
                  f'\n•	If <b>p-value ≥ {sign_levl}</b>, there is no significant association between the {cat}.\n'
                  '\n<a href="https://selar.com/n461o6yn1l">Read more on Chi-square Independence test</a>', unsafe_allow_html=True)
                  if p_value < float(sign_levl):
                    st.success(f"✅ In this case; theres's enough evidence to  reject the null hypothesis: There is a significant association between {cat}.")
                  else:
                    st.info(f"❎ In this case; Fail to reject the null hypothesis: There is no significant association between the {cat}.") 
              except Exception as e:
                st.error(f"❌ An error occured: {e}")         

          # Normality Test 
        elif select_hyp == 'Normality Test':
          text_norm = '''
            \n Shapiro-Wilk test is a widely used and powerful test for normality.
            \n Kolmogorov-Smirnov (K-S) test compares the empirical cumulative distribution function of a theoretical normal distribution.
            \n Anderson-Darling test similar to the K-S test but gives more weight to the tails of the distribution.
          '''
          norm = ['Select Option','Shapiro-Wilk test', 'Kolmogorov-Smirnov (K-S) test','Anderson-Darling test']
          select_norm = st.sidebar.selectbox('Select Option for Chi-square test:', norm, help=text_norm)

          # Shapiro-Wilk test
          if select_norm == 'Shapiro-Wilk test':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            sw_test = st.sidebar.selectbox('Select Column for Shapiro-Wilk test', numeric_cols)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button("Run Shapiro-Wilk test"):
                  # shapiro wilk test
                  col = df4[sw_test]
                  # perform shapiro wilk test
                  stat, p_value = stats.shapiro(col)
                  st.subheader("📊 Result of Shapiro-Wilk Test")
                  st.write(f'**Shapiro-wilk Test Statistic:** {stat}')
                  st.write(f'**P-value:** {p_value :.4f}')
                  # Interpretation
                  st.subheader("🧾 Interpretation")
                  st.markdown(f'•	If <b>p-value < {sign_levl}</b>, data is not normally distributed.\n'
                  f'\n•	If <b>p-value ≥ {sign_levl}</b>, data is likely normally distributed.\n'
                  '\n<a href="https://selar.com/n461o6yn1l">Read more on Shapiro-wilk test</a>', unsafe_allow_html=True)
                  if p_value < float(sign_levl):
                    st.success(f"✅ In this case; theres's enough evidence to  reject the null hypothesis: data is not normally distributed.")
                  else:
                    st.info(f"❎ In this case; Fail to reject the null hypothesis: data is likely normally distributed.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")      

            # Kolmogorov-Smirnov (K-S) test
          elif select_norm == 'Kolmogorov-Smirnov (K-S) test':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            sample3_sel = st.sidebar.selectbox('Sample One (1)', numeric_cols)
            sample4_sel = st.sidebar.selectbox('Sample Two (2)', numeric_cols)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              # Kolmogorov smirnov test
              try:
                if st.sidebar.button("Run Kolmogorov-Smirnov"):
                  # samples
                  sample1 = df4[sample3_sel]
                  sample2 = df4[sample4_sel]
                  # perform shapiro wilk test
                  stat, p_value = stats.ks_2samp(sample1, sample2)
                  st.subheader("📊 Result of Kolmogorov-Smirnov Test")
                  st.write(f'**Kolmogorov-Smirnov Test Statistic:** {stat}')
                  st.write(f'**P-value:** {p_value :.4f}')
                  # Interpretation
                  st.subheader("🧾 Interpretation")
                  st.markdown(f'•	If <b>p-value < {sign_levl}</b>, samples are likely from different distributions.\n'
                  f'\n•	If <b>p-value ≥ {sign_levl}</b>, samples are likely from the same distribution.\n'
                  '\n<a href="https://selar.com/n461o6yn1l">Read more on Kolmogorov-Smirnov Test</a>', unsafe_allow_html=True)
                  if p_value < float(sign_levl):
                    st.success(f"✅ In this case; there's enough evidence to Reject the null hypothesis: samples are likely from different distributions.")
                  else:
                    st.info(f"❎ In this case; Fail to reject the null hypothesis: samples are likely from the same distribution.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")      

            # Aderson-Darling Test
          elif select_norm == 'Anderson-Darling test':
            ad_opt = ["Select Option", "Specific Column", "All Numeric Columns in Dataset"]
            ad_sel = st.sidebar.selectbox("Perform Anderson-Darling Test For:", ad_opt)
            if ad_sel == "Specific Column":
              numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
              sel_col = st.sidebar.selectbox('Select Column For Aderson-Darling Test', numeric_cols)
              try:
                if st.sidebar.button(f'Run Aderson-Darling Test For {sel_col}'):
                  # Anderson-Darling test
                  # perform Anderson-Darling test
                  result = ad(df4[sel_col], dist='norm')
                  st.subheader(f"📊 Result of Anderson-Darling Test for {sel_col}")
                  st.write(f'**Anderson-Darling test stat:** {result.statistic}')
                  st.write(f'**critical values:** {result.critical_values}')
                  st.write(f'**Significant level:** {result.significance_level}')
                  # Interpretation
                  st.subheader("🧾 Interpretation")
                  st.markdown(f'**•	Statistic:** it calculated Anderson-Darling test statistc.\n'
                  f'\n **•	Critical_values:** An array of critical values corresponding to different significance levels.\n'
                  f'\n **•	Significance_leval:** An array of significance levels (eg. 15%, 10%, 5%, 2.5%, 1%).\n'
                  '\n<a href="https://selar.com/n461o6yn1l">Read more on Anderson-Darling Test</a>', unsafe_allow_html=True)
              except Exception as e:
                st.error(f"❌ An error occured: {e}")    
            elif ad_sel == "All Numeric Columns in Dataset":
              if st.sidebar.checkbox("Perform Anderson-Darling for All Column"):
                try:
                  if st.sidebar.button(f'Run Anderson-Darling for {ad_sel}'):
                    numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
                    # perform Anderson-Darling test
                    for column in numeric_cols:
                      result = ad(df4[column], dist='norm')
                      st.subheader(f"📊 Result of Anderson-Darling Test for {column} Column")
                      st.write(f'**Anderson-Darling test stat:** {result.statistic}')
                      st.write(f'**critical values:** {result.critical_values}')
                      st.write(f'**Significant level:** {result.significance_level}')
                    # Interpretation
                    st.subheader("🧾 Interpretation")
                    st.markdown(f'**•	Statistic:** it calculated Anderson-Darling test statistc.\n'
                    f'\n **•	Critical_values:** An array of critical values corresponding to different significance levels.\n'
                    f'\n **•	Significance_leval:** An array of significance levels (eg. 15%, 10%, 5%, 2.5%, 1%).\n'
                    '\n<a href="https://selar.com/n461o6yn1l">Read more on Anderson-Darling Test</a>', unsafe_allow_html=True)
                except Exception as e:
                  st.error(f"❌ An error occured: {e}")    

          # Non-parametric Test
        elif select_hyp == 'Non-parametric Test':
          text_non = '''
            \n Mann-Whitney U Test: is a non-parametric statistical test used to compare two independent groups when the dependent variable is either ordinal or continuous but not normally distributed.
            \n Wilcoxon Signed-Rank Test: This is a non-parametric statistical test used to compare two related, paired samples to determine if their population means ranks differ.
            \n Kruskal-Wallis H Test: This a non-parametric statistical test used to determine if there are statistically significant differences between the medians of two or more independent groups.
            \n Friedman Test: Friedman test is a non-parametric alternative to repeated measures ANOVA.
          '''
          non = ['Select Option','Mann-Whitney U Test', 'Wilcoxon Signed-Rank Test', 'Kruskal Wallis H Test', 'Friedman Test']
          select_non = st.sidebar.selectbox('Select Option for Non-Parametric Test:', non, help=text_non)

          # mann-whitney U test 
          if select_non == 'Mann-Whitney U Test':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            dependent_var = st.sidebar.selectbox('Select dependent Variable(Numeric):', numeric_cols)
            group_var = st.sidebar.selectbox('Select the independent group Variable(Categorical):', categorical_cols)
            # perform mann-whitney U test 
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button('Run Mann-whitney U test'):
                  groups =[]
                  for level in df4[group_var].dropna().unique():
                    group_data = df4[df4[group_var] == level][dependent_var].dropna()
                    groups.append(group_data)
                  if len(groups) < 2:
                    st.warning('⚠️ You need at least two groups to perform Mann-whitney U Test')
                  else:
                    stat, p_val = stats.mannwhitneyu(*groups, True, alternative='two-sided')
                    st.subheader("📊 Result of Mann-whitney U Test")
                    st.write(f'**Dependent Variable:** {dependent_var}')
                    st.write(f'**Independent Group Variable:** {group_var}')
                    st.write(f'**Number of Groups:** {len(groups)}')
                    st.metric(label="**Mann-whitney U-statistic:**", value=f"{stat: .4f}")
                    st.metric(label="**P-value:**", value=f"{p_val: .6f}")

                    st.subheader("🧾 Interpretation")
                    st.markdown( f'•	If <b>P-value < {sign_levl}</b>, there is a significant different between the groups.\n' \
                    f'\n•	If <b>P-value ≥ {sign_levl}</b>, there no significant difference between the groups.\n' \
                    '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Mann-whitney U test</a>', unsafe_allow_html=True)
                    if p_val < float(sign_levl):
                      st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: there is a significant different between the groups.")
                    else:
                      st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: there no significant difference between the groups.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")
                st.warning('⚠️ Check! You cannot have More than two groups to perform Mann-whitney U Test. Try Kruskal Wallis H Test for More than two groups.')        

            # Wilcoxon Signed-Rank Test
          elif select_non == 'Wilcoxon Signed-Rank Test':
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            val_wil1 = st.sidebar.selectbox('Select Sample-1', numeric_cols)
            val_wil2 = st.sidebar.selectbox('Select Sample-2', numeric_cols)
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            # perform Wilcoxon Signed-Rank 
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button("Run Wilcoxon Signed-Rank"):
                  stat, p_value = wc(df4[val_wil1], df4[val_wil2])
                  st.subheader("📊 Result of Wilcoxon Signed-Rank Test")
                  st.metric(label="**Wilcoxon Signed-Rank Test stat:**", value=f"{stat: .4f}")
                  st.metric(label="**P-value:**", value=f"{p_value: .6f}")

                  st.subheader("🧾 Interpretation")
                  st.markdown( f'•	If <b>P-value < {sign_levl}</b>, there is a significant different between the samples in population means.\n' \
                  f'\n•	If <b>P-value ≥ {sign_levl}</b>, there no significant difference between the samples in population means.\n' \
                  '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Wilcoxon Signed-Rank Test</a>', unsafe_allow_html=True)
                  if p_value < float(sign_levl):
                    st.success(f"✅ In this case; theres's enough evidence to  reject the null hypothesis: there is a significant difference in population means between {val_wil1} and {val_wil2}.")
                  else:
                    st.info(f"❎ In this case; there's no much evidence, fail to reject the null hypothesis: there no significant in population means between {val_wil1} and {val_wil2}.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")      

            # Kruskal Wallis H Test
          elif select_non == 'Kruskal Wallis H Test':
            # Kruskal-Wallis H test 
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df4.select_dtypes(exclude=['float64', 'int64']).columns.tolist()
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            dependent_var = st.sidebar.selectbox('Select dependent Variable(Numeric):', numeric_cols)
            group_var = st.sidebar.selectbox('Select the independent group Variable(Categorical):', categorical_cols)
            # perform Kruskal Wallis H test 
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button('Run Kruskal Wallis H test'):
                  groups =[]
                  for level in df4[group_var].dropna().unique():
                    group_data = df4[df4[group_var] == level][dependent_var].dropna()
                    groups.append(group_data)
                  if len(groups) <=2:
                    st.warning('⚠️ You need at least three or more groups to perform Kruskal Wallis H Test')
                  else:
                    stat, p_val = stats.kruskal(*groups)
                    st.subheader("📊 Result of Kruskal-Wallis H Test")
                    st.write(f'**Independent Group Variable:** {group_var}')
                    st.write(f'**Number of Groups:** {len(groups)}')
                    st.metric(label="**H-Statistic:**", value=f"{stat: .4f}")
                    st.metric(label="**P-value:**", value=f"{p_val: .6f}")

                    st.subheader("🧾 Interpretation")
                    st.markdown( f'•	If <b>P-value < {sign_levl}</b>, indicates that at least one group has significantly different ranks, to that the populations are not equal.\n' \
                    f'\n•	If <b>P-value ≥ {sign_levl}</b>, suggesting no significant difference in ranks across groups.\n' \
                    '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Kruskal-Wallis H Test</a>', unsafe_allow_html=True)
                    if p_val < float(sign_levl):
                      st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: there is a significant different in ranks across groups.")
                    else:
                      st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: there no significant difference in ranks across groups.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")        

            # Friedman Test
          elif select_non == 'Friedman Test':
            # friedman test 
            numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
            sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
            st.sidebar.info("❎ 0.05 is usual used for significant level")
            indep_val = st.sidebar.multiselect("Select Groups:", numeric_cols)
            if sign_levl == str():
              st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
            else:
              try:
                if st.sidebar.button('Run Friedman test'):
                  groups =[]
                  for column in df4[indep_val]:
                    group_data = df4[column]
                    groups.append(group_data)
                  if len(groups) <= 2:
                    st.warning('⚠️ You need at least three or more sample set to perform Friedman Test')
                  else:
                    stat, p_val = fc(*groups)
                    st.subheader("📊 Result of Friedman Test")
                    st.metric(label="**Friedman Test Statistic:**", value=f"{stat: .4f}")
                    st.metric(label="**P-value:**", value=f"{p_val: .6f}")

                    st.subheader("🧾 Interpretation")
                    st.markdown( f'•	If <b>P-value < {sign_levl}</b>, it indicates a statistically significant difference in the medians across the repeated measurements.\n' \
                    f'\n•	If <b>P-value ≥ {sign_levl}</b>, suggesting no significant difference in the medians across the repeated measurements.\n' \
                    '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Friedman Test</a>', unsafe_allow_html=True)
                    if p_val < float(sign_levl):
                      st.success("✅ In this case; theres's enough evidence to  reject the null hypothesis: there is a significant different in the medians across the repeated measurements.")
                    else:
                      st.info("❎ In this case; there's no much evidence, fail to reject the null hypothesis: there no significant difference in the medians across the repeated measurements.")
              except Exception as e:
                st.error(f"❌ An error occured: {e}")        

        # Confidence Intervals
      elif analy_option == 'Confidence Intervals':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
        mean_col = st.sidebar.selectbox('Choose Sample Mean:', numeric_cols)
        # confidence interval 
        if st.sidebar.checkbox("Perform Confidence Interval"):
          try:
            if st.sidebar.button("Run Confidence Interval"):
              # mean_Mark
              data = df4[mean_col].dropna().astype(float).values
              mean_mark = float(np.mean(data))
              # standard error of mean
              sem = float(stats.sem(data))

              # confidence interval 
              
              interval = stats.t.interval(confidence=0.95,df=len(data) - 1, loc = mean_mark, scale = sem)
              lower = float(interval[0])
              upper = float(interval[1])
              
              st.subheader(f"❎ 95% Confidence  Interval For Mean {mean_col}")
              st.metric(label="**Mean:**", value=f"{mean_mark: .4f}")
              st.metric(label="**Lower Bound Confidence:**", value=f"{lower: .2f}")
              st.metric(label="**Upper Bound Confidence:**", value=f"{mean_mark: .2f}")
              #visual distribution
              fig, ax = plt.subplots()
              ax.hist(data, bins='auto')
              ax.set_xlabel("Values")
              ax.set_ylabel("Frequency")
              ax.set_title('Distribution of Sample Data')
              st.pyplot(fig)
              st.markdown('<a href="https://selar.com/n461o6yn1l">ReadMore On Confidence Interval</a>', unsafe_allow_html=True)
          except Exception as e:
            st.error(f"❌ An error occured: {e}")    

        # Correlation and Regression
      elif analy_option == 'Correlation and Regression':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        cr = ['Selct Option','Correlation-coefficient', 'Linear Regression']
        cr_option = st.sidebar.selectbox('Select Option:', cr)
        
        # correlation_coeffficient 
        if cr_option == 'Correlation-coefficient':
          # correlation Coefficient
          if st.sidebar.checkbox('Perform Correlation Coefficient'):
            try:
              if st.sidebar.button('Run corrrelation Coefficient'):
                # calculate correlation 
                correlation = df4.corr(numeric_only=True)
                st.subheader("📊 Result of Correlation Coefficient")
                st.dataframe(correlation)

                st.subheader("🧾 Interpretation")
                st.markdown( f'•	A value 1 or close to 1 indicates a strong positive correlation. \n' \
                f'\n•	A value close to -1 indicates a stong negative correlation.\n'
                f'\n•	•	A value close to 0 indicates a weak or no correlation.\n' \
                '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Correlation Coefficient</a>', unsafe_allow_html=True)
                # visualization 
                fig, ax = plt.subplots(figsize=(8,4))
                ax = sns.heatmap(correlation, annot=True, cmap= 'coolwarm', fmt='.2f', linewidths=0.5)
                plt.title('Correlation Coefficient Heatmap')
                st.pyplot(fig)
            except Exception as e:
              st.error(f"❌ An error occured: {e}")    
            


          # Linear Regression
        elif cr_option == 'Linear Regression':
          numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
          sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
          st.sidebar.info("❎ 0.05 is usual used for significant level")
          indep_val = st.sidebar.multiselect("Select Independent Variables:", numeric_cols)
          depen_val = st.sidebar.selectbox('Select Dependent Variable:', numeric_cols)
          if sign_levl == str():
            st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
          else:
            try:
              if st.sidebar.button('Run Linear Regression'):
                # Linear Regression
                # independent variables 
                x = df4[indep_val]
                # dependent 
                y = df4[depen_val]
                # add a constant term to x for the intercept
                const_X = sm.add_constant(x)
                # create and fit the OLS model 
                model = sm.OLS(y, const_X)
                results = model.fit()
                st.subheader("📊 Result of Linear Regression")
                st.write(results.summary())

                st.subheader("🧾 Interpretation")
                st.markdown( f'**P-values** for coefficients indicate the probability of observing such a coeffient if there were no actual relationship between the variables. **P-value < {sign_levl}** suggests that the coefficient is statistically significant, meaning the relationship is unlikely to be due to random chance. \n' \
                '\n<a href="https://selar.com/n461o6yn1l">ReadMore On Linear Regression</a>', unsafe_allow_html=True)
            except Exception as e:
              st.error(f"❌ An error occured: {e}")    


        # Circular Mean
      elif analy_option == 'Circular Mean':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        # circular mean
        numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
        cir_m = st.sidebar.selectbox('Select Column For Circular Mean:', numeric_cols)
        if st.sidebar.checkbox(f'Calculate Circular Mean'):
          try:
            if st.sidebar.button("Run Circular Mean"):
              # calculate circular mean 
              circular_mean = cm(df4[cir_m])
              st.subheader("📊 Result of Circular Mean")
              st.metric(label=f"**Circular Mean Of {cir_m} :**", value=f"{circular_mean:.4f}")

              # visualization
              st.subheader("📊 Scatter Plot Showing Circular Mean")
              fig, ax = plt.subplots(figsize=(8,4))
              ax = sns.scatterplot(x= cir_m, y= circular_mean, ax=ax, data=df4)
              plt.title(f'Circular Mean of {cir_m} with Scatter Plot')
              st.pyplot(fig)
          except Exception as e:
            st.error(f"❌ An error occured: {e}")    

    


        # Time Series Analysis
      elif analy_option == 'Time Series Analysis':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        ts = ['Selct Option','ARIMA', 'SARIMA']
        ts_option = st.sidebar.selectbox('Select T-S Analysis Option:', ts)

        # ARIMA
        if ts_option == 'ARIMA':
          # time series data 
          or_d = '''examaples of common ARIMA order (p,d,q):\n 
          \n"0 0 0" "1 0 0" "0 0 1" "0 1 0"  "0 1 1" "2 1 2" "5 1 0"'''
          numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
          ts_data = st.sidebar.selectbox('Select Time Series Data:', numeric_cols, help= or_d)
          # ts_ord = st.sidebar.selectbox('Select ARIMA Order (p,d,q):', or_d)
          st.sidebar.subheader("Choose ARIMA Order (p,d,q)")
          p = st.sidebar.number_input('insert P:')
          d = st.sidebar.number_input('Insert d:')
          q = st.sidebar.number_input('insert q:')
          sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
          st.sidebar.info("❎ 0.05 is usual used for significant level")
          if sign_levl == str():
            st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
          else:
            try:
              if st.sidebar.button("Run ARIMA"):
                data = df4[ts_data]
                # order (p, d, q) 
                pdq = (p,d,q)
                order = pdq # adjust based on your data analysis
                model = AM(data, order= order)
                model_fit = model.fit()
                st.subheader("📊 ARIMA Model summary")
                st.write(model_fit.summary())
                st.markdown( f'<a href="https://selar.com/n461o6yn1l">Interpretation On ARIMA</a>', unsafe_allow_html=True)
            except Exception as e:
              st.error(f"❌ An error occured: {e}")

          # SARIMA
        elif ts_option == 'SARIMA':
          numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
          ts_data = st.sidebar.selectbox('Select Time Series Data:', numeric_cols)
          st.sidebar.subheader("Choose SARIMA Order (p,d,q)")
          p = st.sidebar.number_input('Insert P:')
          d = st.sidebar.number_input('Insert d:')
          q = st.sidebar.number_input('Insert q:')
          st.sidebar.subheader("Choose Seasonal Order (P,D,Q,S)")
          p2 = st.sidebar.number_input('Choose P:')
          d2 = st.sidebar.number_input('Choose D:')
          q2 = st.sidebar.number_input('Choose Q:')
          s = st.sidebar.number_input('Choose S:')
          sign_levl = st.sidebar.text_input("Choose Your Significant Level:")
          st.sidebar.info("❎ 0.05 is usual used for significant level")
          if sign_levl == str():
            st.warning("⚠️ Choose Significant Level and Press Enter Key to Proceed.")
          else:
            try:
              if st.sidebar.button("Run SARIMA"):
                data = df4[ts_data]
                # order (p, d, q) 
                pdq = (p,d,q)
                sea = (p2,d2,q2,s)
                order = pdq # adjust based on your data analysis
                seasonal = sea
                model = SX(data, order= order, seasonal_order=seasonal, enforce_stationarity=False, enforce_invertibility=False)
                results = model.fit(disp=False) # disp=false suppresses convergence message
                st.subheader("📊 SARIMA Model Summary")
                st.write(results.summary())
                st.markdown( f'<a href="https://selar.com/n461o6yn1l">Interpretation On SARIMA</a>', unsafe_allow_html=True)
            except Exception as e:
              st.error(f"❌ An error occured: {e}")    

        # Survival Analysis
      elif analy_option == 'Survival Analysis':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        sa = ['Selct Option','Proportional Hazard Regression (COX Model)', 'Survivor Function Estimation (KaplanMeier)']
        sa_option = st.sidebar.selectbox('Select Survival Analysis Option:', sa)
        
        # Proportional Hazard Regression (COX Model)
        if sa_option == 'Proportional Hazard Regression (COX Model)':
          st.sidebar.info("❎ Recode your data to 0 and 1 or numbers to suit this analysis. e.g Yes=1 and No=0")
          # Proprtional harzards regression
          numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
          s_endog = st.sidebar.selectbox('Select Time to Event or Censoring:', numeric_cols)
          s_stat = st.sidebar.selectbox('Select Event Status:', numeric_cols)
          s_exog = st.sidebar.multiselect('Choose Columns for Covariates:', numeric_cols)
          try:
            if st.sidebar.button("Run PHR"):
              endog = df4[s_endog] # endog is time variable, time to event or censoring
              stat = df4[s_stat] # event status
              exog = df4[s_exog] # contains the covariates
              # fit the proportional harzardss model 
              model = PHReg(endog, exog, status=stat, tie_method= 'breslow')
              results = model.fit()
              st.subheader("📊 Proportional Hazard Regression Model Summary")
              st.write(results.summary())
              st.markdown( f'<a href="https://selar.com/n461o6yn1l">Interpretation On Proportional Hazard Regression</a>', unsafe_allow_html=True)
          except Exception as e:
            st.error(f"❌ An error occured: {e}")    

          # Survivor Function Estimation (KaplanMeier)
        elif sa_option == 'Survivor Function Estimation (KaplanMeier)':
          st.sidebar.info("❎ Recode your data to 0 and 1 or numbers to suit this analysis. e.g Yes=1 and No=0")
          numeric_cols = df4.select_dtypes(include=['float64', 'int64']).columns.tolist()
          sf_endog = st.sidebar.selectbox('Select Time Variable (Duration):', numeric_cols)
          sf_stat = st.sidebar.selectbox('Select Status Variable (Event Indicator):', numeric_cols)
          try:
            if st.sidebar.button("Run SFE"):
              # Survivor Function estimation
              time_v = df4[sf_endog] # the time variable (duration)
              stat = df4[sf_stat] # the status variable (event indicator)
              # survivor function 
              sf = sm.SurvfuncRight(time_v, stat)
              st.subheader("📊 Survival Function Summary")
              st.write(sf.summary())
              # Estimate specific quantiles of the survival distribution 
              try:
                # time which 25% of events have occurred
                st.subheader("❎Time which 25% Of Events have Occurred")
                st.metric(label=f"**25% quantile:**", value=f"{sf.quantile(0.25)}")
                st.metric(label=f"**25% confidence interval:**", value=f"{np.int64(sf.quantile_ci(0.25))}")
              except ValueError as e:
                st.write(f"Could not estimate quantile or CI: {e}")
              st.markdown( f'<a href="https://selar.com/n461o6yn1l">Survivor Function Estimation</a>', unsafe_allow_html=True)
          except Exception as e:
            st.error(f"❌ An error occured: {e}")    



    # Data Visualization
  elif select_menu == 'Data Visualization':
    # Hide menu 
    st.markdown(hide2, unsafe_allow_html=True)
    #title
    st.markdown("<h2 class='subtitle'>Create Visuals</h2>", unsafe_allow_html=True)

    # upload file 
    st.sidebar.subheader("📂 Upload File to Create Visuals")
    upload_file = st.sidebar.file_uploader("Upload a File", type=['csv', "xlsx"])
    
    # condition to upload file 
    if upload_file != None:

      # success message 
      st.sidebar.success('✅ File Upload successfully!')
      
      # read file 
      if upload_file.name.endswith(".csv"):
        df5 = pd.read_csv(upload_file)
      else:
        df5 = pd.read_excel(upload_file)
      visual = [ 'Select Option', 'Scatter Plot', 'Line Plot', 'Bar Plot', 'Histogram', 'Density Plot', 'Box Plot','Violin Plot', 'Heatmap', 'Joint Plot', 'Fecet Grid', 'Pie Chart']
      visual_option = st.sidebar.selectbox("Visual option:", visual)
      # show dataset  
      if st.sidebar.checkbox("Show Dataset"):
        st.subheader('Your Dataset')
        st.write(df5)
      
      # Scatter Plot
      if visual_option == 'Scatter Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        sc = st.sidebar.selectbox("Choose Scatter Plot Option:", ['Select Option','Normal Scatter Plot', 'Customize Scatter Plot'])
        if sc == 'Normal Scatter Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Create Scatter Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.scatterplot(x= x, y= y, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Normal Scatter Plot")
            else:
              plt.title(title)
            st.pyplot(fig)
        elif sc == 'Customize Scatter Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          hue = st.sidebar.selectbox("Select Column for Hue (distinguish data points):", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Customize Scatter Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.scatterplot(x= x, y= y, hue=hue, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Customized Scatter Plot")
            else:
              plt.title(title)
            st.pyplot(fig)

        # Line Plot 
      elif visual_option == 'Line Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        lp = st.sidebar.selectbox("Choose Line Plot Option:", ['Select Option','Normal Line Plot', 'Customize Line Plot'])
        if lp == 'Normal Line Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Create Line Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.lineplot(x= x, y= y, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Normal Line Plot")
            else:
              plt.title(title)
            st.pyplot(fig)
        elif lp == 'Customize Line Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          hue = st.sidebar.selectbox("Select Column for Hue (distinguish data points):", df5.columns)
          style = st.sidebar.selectbox("Select Column for Style:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Customize Line Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.lineplot(x= x, y= y, hue=hue, style= style, markers=True, dashes=False ,data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Customized Line Plot")
            else:
              plt.title(title)
            st.pyplot(fig)


        # Bar plot 
      elif visual_option == 'Bar Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        lp = st.sidebar.selectbox("Choose Bar Plot Option:", ['Select Option','Normal Bar Plot', 'Customize Bar Plot'])
        if lp == 'Normal Bar Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          lab = st.sidebar.checkbox("Add Data Label")
          color = st.sidebar.color_picker("Choose Color For Bar Chart:")
          if st.sidebar.button("Create Bar Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.barplot(x= x, y= y, ax=ax, errorbar=None, data=df5, color=color)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Normal Bar Plot")
            else:
              plt.title(title)
            if lab:
              ax.bar_label(ax.containers[0])
            st.pyplot(fig)
        elif lp == 'Customize Bar Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          hue = st.sidebar.selectbox("Select Column for Hue (distinguish bars):", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          lab = st.sidebar.checkbox("Add Data Label")
          if st.sidebar.button("Customize Bar Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.barplot(x=x, y=y,hue=hue,estimator="mean", errorbar=None, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Customized Bar Plot")
            else:
              plt.title(title)
            if lab:
              for con in ax.containers:
                ax.bar_label(con)
            st.pyplot(fig)

        # Histogram
      elif visual_option == 'Histogram':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        hist = st.sidebar.selectbox("Choose Histogram Option:", ['Select Option','Normal Histogram', 'Customize Histogram'])
        if hist == 'Normal Histogram':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          lab = st.sidebar.checkbox("Add Data Label")
          if st.sidebar.button("Create Histogram"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.histplot(x= x, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if title == str():
              plt.title("Normal Histogram")
            else:
              plt.title(title)
            if lab:
              ax.bar_label(ax.containers[0])
            st.pyplot(fig)
        elif hist == 'Customize Histogram':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          lab = st.sidebar.checkbox("Add Data Label")
          color = st.sidebar.color_picker("Choose Color For Histogram:")
          if st.sidebar.button("Customize Histogram"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.histplot(data=df5, x=x, bins=20, kde=True, color=color)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if title == str():
              plt.title("Customize Histogram")
            else:
              plt.title(title)
            if lab:
              ax.bar_label(ax.containers[0])
            st.pyplot(fig)

        # Density Plot
      elif visual_option == 'Density Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        den = st.sidebar.selectbox("Choose Histogram Option:", ['Select Option','Normal Density Plot', 'Customize Density Plot'])
        if den == 'Normal Density Plot':
          numeric_cols = df5.select_dtypes(include=['float64', 'int64', 'datetime64']).columns.tolist()
          x = st.sidebar.selectbox("Select Column for X-axis:", numeric_cols)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Create Density"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.kdeplot(x= x, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if title == str():
              plt.title("Normal Density")
            else:
              plt.title(title)
            st.pyplot(fig)
        elif den == 'Customize Density Plot':
          numeric_cols = df5.select_dtypes(include=['float64', 'int64', 'datetime64']).columns.tolist()
          x = st.sidebar.selectbox("Select Column for X-axis:", numeric_cols)
          hue = st.sidebar.selectbox("Select Column for Hue:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Customize Density"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.kdeplot(data=df5, x=x, hue=hue, fill=True, alpha=0.6, linewidth=1.5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if title == str():
              plt.title("Customize Histogram")
            else:
              plt.title(title)
            st.pyplot(fig)

        # Box Plot
      elif visual_option == 'Box Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        box = st.sidebar.selectbox("Choose Box Plot Option:", ['Select Option','Normal Box Plot', 'Customize Box Plot'])
        if box == 'Normal Box Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Create Box Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.boxplot(x= x, y= y, ax=ax, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Normal Box Plot")
            else:
              plt.title(title)
            st.pyplot(fig)
        elif box == 'Customize Box Plot':
          x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
          y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
          hue = st.sidebar.selectbox("Select Column for Hue:", df5.columns)
          x_lab = st.sidebar.text_input("Choose Label For X-axis:")
          y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
          title = st.sidebar.text_input("Choose Title For The Plot:")
          if st.sidebar.button("Customize Box Plot"):
            fig, ax = plt.subplots(figsize=(8,4))
            ax = sns.boxplot( x=x, y=y,hue=hue, linewidth=1.5, palette="Set3", fliersize=4, data=df5)
            if x_lab == str():
              plt.xlabel(x)
            else:
              plt.xlabel(x_lab)
            if y_lab == str():
              plt.ylabel(y)
            else:
              plt.ylabel(y_lab)
            if title == str():
              plt.title("Customized Box Plot")
            else:
              plt.title(title)
            st.pyplot(fig)

        # Violin Plot
      elif visual_option == 'Violin Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
        y = st.sidebar.selectbox("Select Column for Y-axis:", df5.columns)
        x_lab = st.sidebar.text_input("Choose Label For X-axis:")
        y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
        title = st.sidebar.text_input("Choose Title For The Plot:")
        if st.sidebar.button("Create Violin Plot"):
          fig, ax = plt.subplots(figsize=(8,4))
          ax = sns.violinplot(x= x, y= y, ax=ax, data=df5)
          if x_lab == str():
            plt.xlabel(x)
          else:
            plt.xlabel(x_lab)
          if y_lab == str():
            plt.ylabel(y)
          else:
            plt.ylabel(y_lab)
          if title == str():
            plt.title("Violin Plot")
          else:
            plt.title(title)
          st.pyplot(fig)

        # Heatmap
      elif visual_option == 'Heatmap':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        if st.sidebar.checkbox("Create Heatmap"):
          if st.sidebar.button("Plot Heatmap"):
            fig, ax = plt.subplots(figsize=(8,4))
            corr = df5.corr(numeric_only=True)
            ax = sns.heatmap(corr)
            st.pyplot(fig)

        # join plot 
      elif visual_option == 'Joint Plot':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        x = st.sidebar.selectbox("Select Column for X-axis:", df5.columns)
        y = st.sidebar.selectbox("Select Column for y-axis:", df5.columns)
        x_lab = st.sidebar.text_input("Choose Label For X-axis:")
        y_lab = st.sidebar.text_input("Choose Label For Y-axis:")
        title = st.sidebar.text_input("Choose Title For The Plot:")
        if st.sidebar.button("Create Joint Plot"):
          fig, ax = plt.subplots(figsize=(8,4))
          ax = sns.jointplot( x=x, y=y, ax=ax, data=df5)
          if x_lab == str():
            plt.xlabel(x)
          else:
            plt.xlabel(x_lab)
          if y_lab == str():
            plt.ylabel(y)
          else:
            plt.ylabel(y_lab)
          if title == str():
            plt.title("Joint Plot")
          else:
            plt.title(title)
          st.pyplot(ax)

        # Fecet Grid
      elif visual_option == 'Fecet Grid':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        x = st.sidebar.selectbox("Select Grid Column:", df5.columns)
        y = st.sidebar.selectbox("Select Column for Histogram:", df5.columns)
        if st.sidebar.button("Create Fecet Grid"):
          fig, ax = plt.subplots(figsize=(8,4))
          ax = fecet= sns.FacetGrid(df5, col=x)
          # histogram 
          fecet.map(sns.histplot, y)
          st.pyplot(ax)

        # pie chart 
      elif visual_option == 'Pie Chart':
        # hide subtitle
        st.markdown(subtitle, unsafe_allow_html=True)
        y = st.sidebar.selectbox("Select Column For Pie Chart:", df5.columns)
        title = st.sidebar.text_input("Choose Title For The Plot:")
        if st.sidebar.button("Create Pie Chart"):
          y2 = df5[y].value_counts()
          fig, ax = plt.subplots(figsize=(8,4))
          color = sns.color_palette('bright')
          ax = plt.pie(y2, labels=y2.index, colors=color, autopct='%.0f%%')
          if title == str():
            plt.title("Pie chart")
          else:
            plt.title(title)
          st.pyplot(fig)

    # Home page 
  elif select_menu == 'About App':
    st.markdown(hide2, unsafe_allow_html=True)
    welcome = st.markdown('<h2>Welcome To All-in-One Data Workspace</h2>' \
    '<p style="text-align: justify;">Turn raw data into clear, actionable insight; faster and smarter.</P>' \
    '<p style="text-align: justify;">This app is built for professionals who work with data every day and need results without friction. Whether your data comes messy, incomplete, or in different formats, this platform helps you clean, analyse, visualise, and convert files seamlessly.</p>'
    '<h4> What You Can Do</h4>'
    '<ul style="text-align: justify;"> <li><b>Clean and Prepare Data:</b> Detect and fix errors, handle missing values, handle duplicates, standardise formats, and get your data analysis ready in minutes.</li> <li><b>Analyse with Confidence:</b> Explore patterns, trends, and key metrics using reliable statistical and analytical tools designed for real-world datasets. </li><li><b>Visualise for Insight:</b> Transform numbers into clear charts that make insights easy to understand and share.</li> <li><b>Covert with Ease:</b> Upload files in multiple formats and quickly convert them to CSV or Excel files, ensuring compatibility with your preferred tools and Workflows.</li></ul>'
    '<h4>Why This App?</h4>'
    '<ul style="text-align: justify;"><li><b>Fast and Intuitive:</b> No steep learning curve; focus on insight, not setup.</li> <li><b>Accurate and Reliable:</b> Built to handle complex and messy data.</li> <li><b>Flexible:</b> Suitable for analysts, researchers, M&E professionals, and decision-makers.</li></ul>' \
    '<p style="text-align: justify;">From row data to meaningful stories, this app supports every step of your data journey. Click the <a href="https://selar.com/n461o6yn1l">Link</a> to learn more about Data Analysis.</p>'\
    '<p style="text-align: justify;"><strong>Upload your data and start transforming information into impact.</strong></p> ', unsafe_allow_html=True) 
    image_placeholder = st.empty()
    image_placeholder.image("book.jpg", caption="The Book that teaches you Data Analysis (Click the Link Above)")

    # My portfolio 
  elif select_menu == 'My Portfolio':
    st.markdown(hide2, unsafe_allow_html=True)
    col1,col2 = st.columns([5,5])

    with col1:
      st.image("my_img.jpg")
    
    with col2:
      st.markdown('ABOUT MM ADEIZA' \
      '\n---')
      
      st.markdown(
        '<div style="text-align: justify;">Is a vissionary data expert leveraging technology to drive impact. With expertise in data engineering, MEARL, Data Analysis, Data Management, Data Science, Information Technology, Health Informatics, and Project Management. He has developed innovative tracking systems using DHIS2 for diseases like meningitis, Mpox, and Lassa Fever, and Also contributed to success of Sierra leone National Medical Supply DHIS2 (MSUPP). Improving epidemic control and decision-making in Africa and grobally. His passion for data-driven solution has enhanced public health/other sectors outcomes</div>', unsafe_allow_html=True
      )

    st.markdown('<div style="text-align: justify;">and he continues to push boundaries in research, data-informed and advocacy.<br>He obtained his first educatinal qualifications in Computer Science from <b>Kogi State Polytechnic Lokoja</b>, where he developed strong computer theoretical skills. His academic background has provided a solid foundation for his career in Information Technology (IT), Data Analytics, Health Information Systems, and Technology-driven Solutions. He also obtained various Analytics and Project management certificates from <b>Geospatial Analytics Technology</b> and Other registered/verified platform, where he developed strong analytical, technical, health information systems,  technology-driven solutions, and problem-solving skills. <br> Originally hailed form Ihima part of Okehi L.G.A of Kogi State, Nigeria, Mustapha Muhammed Adeiza has built a reputation for professionalism, dedication, and continuous learning. Throughout his career, he has contributed to variuos projects in public health, monitoring and evaluation, and digital systems strenghening, working with government agencies, development partiners, and non-govermental organizations. With a commitment to excellence and innovation, he continues to pursue opportunities that create positive impact through data, technology, and community development. </div><hr>', unsafe_allow_html=True)


    st.subheader("MY Portfolio")

    st.markdown("----")

    col3,col4 = st.columns([3,7])

    with col3:
      st.image("nysc.jpg")
    
    with col4:
      st.markdown('Successfully Completed One Year NYSC Programme in Bauchi State' \
      '\n---')
      
      st.markdown(
        '<div style="text-align: justify;">Successfully completed the one-year <b>National Youth Service Corps (NYSC)</b> programme in <b>Bauchi State</b> in year 2022 to 2023, demonstrating exceptional commitment to national service, community development, and professional excellence. Throughout the service year, actively participated in all mandatory phases of the NYSC scheme, including the orientation course, primary assignment, community development service (CDS), and passing-out activities. The NYSC programme is designed to promote national unity, leadership development, self-reliance, and community engagement among Nigerian graduates.<br><a href="https://docs.google.com/document/d/1R5exzsLSe2SGs_Jwp7uCNF8T5_hhkTLwHuJkuKV5X0A/edit?usp=sharing">Read more</a></div>', unsafe_allow_html=True
      )

    st.markdown('<hr>', unsafe_allow_html=True)
    col5,col6 = st.columns([4,6])

    with col5:
      st.image("com.jpg")
    
    with col6:
      st.markdown('Field Supportive Supervision Across the 20 LGA of Bauchi State' \
      '\n---')
      
      st.markdown(
        '<div style="text-align: justify;">I participated in successfully planned, coordinated, and conducted supportive supervision activities in 20 LGA of</div>', unsafe_allow_html=True
      )
    st.markdown('<div style="text-align: justify;">Bauchi State in 2024 in the course of working with Pro-health International, ensuring effective implementation of program activities and adherence to established operational standards. Demonstrated strong leadership, technical expertise, and problem-solving skills while providing guidance and mentorship to field personnel, fostering improved performance, accountability, and service delivery.<br><a href="https://docs.google.com/document/d/1R5exzsLSe2SGs_Jwp7uCNF8T5_hhkTLwHuJkuKV5X0A/edit?usp=sharing">Read more</a></div><hr>', unsafe_allow_html=True)

    col7,col8 = st.columns([4,6])

    with col7:
      st.image("dqa.jpg")
    
    with col8:
      st.markdown('Participated in Data Quality Assessment (DQA) in Adamawa State' \
      '\n---')
      
    st.markdown(
      '<div style="text-align: justify;">I joined the Strategic Information Team of Pro-health International to conduct comprehensive <b>Data Quality Assessment (DQA)</b> in year 2023, activities to evaluate the accuracy, completeness, consistency, timeliness, and reliability of programme data. Demonstrated strong analytical, monitoring, and evaluation skills in assessing data management systems and ensuring that reported information met established quality standards and reporting requirements.<br><a href="https://docs.google.com/document/d/1R5exzsLSe2SGs_Jwp7uCNF8T5_hhkTLwHuJkuKV5X0A/edit?usp=sharing">Read more</a></div><hr>', unsafe_allow_html=True
    )

    col9,col10 = st.columns([4,6])

    with col9:
      st.image("tot.jpg")

    with col10:
      st.markdown('Training of Trainers (ToT) on Sierra Leone LMIS and DHIS2 Integration' \
      '\n---')
      
    st.markdown(
      '<div style="text-align: justify;">I successfully designed, facilitated, and completed a comprehensive <b>Training of Trainers (ToT) on the integration of the Sierra Leone Logistics Management Information System (LMIS) and District Health Information Software 2 (DHIS2) which is called MSUPP</b> ending of year 2025, aimed at strengthening health information management, supply chain visibility, and data-driven decision-making across the health sector, District and National level.<br><a href="https://docs.google.com/document/d/1R5exzsLSe2SGs_Jwp7uCNF8T5_hhkTLwHuJkuKV5X0A/edit?usp=sharing">Read more</a></div><hr>', unsafe_allow_html=True
    )

    col11,col12 = st.columns([3,7])
    with col11:
      st.image("dhis2.png")
    
    with col12:
      st.markdown('Developed DHIS2 Disease Surveillance System for Meningitis and Mpox Tracking' \
      '\n---')
      
    st.markdown(
      '<div style="text-align: justify;">Successfully led the design, development, configuration, and implementation of a <b>DHIS2-based disease surveillance and monitoring system,</b> to strengthen the tracking, reporting, and management of priority public health diseases, including <b>Meningitis</b> and <b>Mpox (Monkeypox)</b>. The initiative enhanced the capacity of health authorities and implementing partners to monitor disease trends, improve data quality, and support timely public health decision-making.<br><a href="https://docs.google.com/document/d/1R5exzsLSe2SGs_Jwp7uCNF8T5_hhkTLwHuJkuKV5X0A/edit?usp=sharing">Read more</a></div><hr>', unsafe_allow_html=True
    )

    col13,col14 = st.columns([3,7])
    with col13:
      st.image("book.jpg")
    
    with col14:
      st.markdown('I wrote a book title: Python as Your Data Analytical Superpower' \
      '\n---')
      
    st.markdown(
      '<div style="text-align: justify;">Python has become a leading tool for data analysis because of its simplicity, versatility, and powerful analytical capabilities. It enables users to collect, clean, analyze, visualize, and interpret data efficiently using libraries such as Pandas, NumPy, and Matplotlib. Python supports data-driven decision-making, automates repetitive tasks, and powers advanced analytics, machine learning, and artificial intelligence applications. Its widespread use across industries including public health, finance, education, and business; combined with strong community support, has made Python an essential analytical superpower for solving complex problems and generating actionable insights. <a href="https://selar.com/n461o6yn1l">Get Your Copy here</a></div>', unsafe_allow_html=True
    )

    cv = """
      <style>
      .cv{
        text-align: right;
      }
      </style>
      <div class="cv"><hr><a href="https://drive.google.com/file/d/19Yxkhqa5amJadMIIypZ2sNRO_KB8W7L3/view?usp=sharing">Detailed Curriculum Vitae (CV)</a></div><hr>

    """

    st.markdown(cv, unsafe_allow_html=True)


# footer
footer = """
<style>
.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #0E1117;
  padding: 10px;
  text-align: center;
  z-index: 999;
}
.footer a {
  margin: 0 12px;
  text-decoration: none;
}
.footer img {
  width: 32px;
  height: 32px;
  vertical-align: middle;
}
.footer span{
  color: grey;
  padding-left:150px;
}
.footer strong{
  color: grey;
}
</style>

<div class="footer">
  <strong>Contact Us:</strong><br>
  <a href="mailto:mustaphamuhammedadeiza@gmail.com" target="_blank">
    <img src="https://cdn.simpleicons.org/gmail" alt="Email">
  </a>

  <a href="https://www.linkedin.com/in/muhammed-mustapha-79039a1b5?utm_source=share_via&utm_content=profile&utm_medium=member_android" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">
  </a>

  <a href="https://www.facebook.com/profile.php?id=100078822710731" target="_blank">
    <img src="https://cdn.simpleicons.org/facebook" alt="Facebook">
  </a>

  <a href="https://wa.me/qr/TDJGVIJP5HK4P1" target="_blank">
    <img src="https://cdn.simpleicons.org/whatsapp" alt="WhatsApp">
  </a>

  <a href="https://x.com/Jayplus4kogi" target="_blank">
    <img src="https://cdn.simpleicons.org/x" alt="X">
  </a>

  <a href="https://www.instagram.com/mm_adeiza?igsh=MW4wOWk5ZXh5eHFxeQ==" target="_blank">
    <img src="https://cdn.simpleicons.org/instagram" alt="Instagram">
  </a>
  <span>Developed by: MM Adeiza</span>
  <span>&#169;Officially My Portfolio</span>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
