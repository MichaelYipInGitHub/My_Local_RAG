#####################################
#######       File Upload      #######
#####################################
import gradio as gr
import os
import shutil
import pandas as pd

STRUCTURED_FILE_PATH = "File/Structured"
UNSTRUCTURED_FILE_PATH = "File/Unstructured"

# Refresh Unstructured Categories
def refresh_label():
    return os.listdir(UNSTRUCTURED_FILE_PATH)

# Refresh Structured Data Tables
def refresh_data_table():
    return os.listdir(STRUCTURED_FILE_PATH)

# Upload Unstructured Data
def upload_unstructured_file(files, label_name):
    if files is None:
        gr.Info("Please upload files")
    elif len(label_name) == 0:
        gr.Info("Please enter the category name")
    # Check if the category already exists
    elif label_name in os.listdir(UNSTRUCTURED_FILE_PATH):
        gr.Info(f"Category {label_name} already exists")
    else:
        try:
            if not os.path.exists(os.path.join(UNSTRUCTURED_FILE_PATH, label_name)):
                os.mkdir(os.path.join(UNSTRUCTURED_FILE_PATH, label_name))
            for file in files:
                print(file)
                file_path = file.name
                file_name = os.path.basename(file_path)
                destination_file_path = os.path.join(UNSTRUCTURED_FILE_PATH, label_name, file_name)
                shutil.move(file_path, destination_file_path)
            gr.Info(f"Files have been uploaded to the {label_name} category. Please proceed to create the knowledge base.")
        except:
            gr.Info("Please avoid duplicate uploads")

# Upload Structured Data
def upload_structured_file(files, label_name):
    if files is None:
        gr.Info("Please upload files")
    elif len(label_name) == 0:
        gr.Info("Please enter the data table name")
    # Check if the data table already exists
    elif label_name in os.listdir(STRUCTURED_FILE_PATH):
        gr.Info(f"Data table {label_name} already exists")
    else:
        try:
            if not os.path.exists(os.path.join(STRUCTURED_FILE_PATH, label_name)):
                os.mkdir(os.path.join(STRUCTURED_FILE_PATH, label_name))
            for file in files:
                file_path = file.name
                file_name = os.path.basename(file_path)
                destination_file_path = os.path.join(STRUCTURED_FILE_PATH, label_name, file_name)
                shutil.move(file_path, destination_file_path)
                if os.path.splitext(destination_file_path)[1] == ".xlsx":
                    df = pd.read_excel(destination_file_path)
                elif os.path.splitext(destination_file_path)[1] == ".csv":
                    df = pd.read_csv(destination_file_path)
                txt_file_name = os.path.splitext(file_name)[0] + '.txt'
                columns = df.columns
                with open(os.path.join(STRUCTURED_FILE_PATH, label_name, txt_file_name), "w") as file:
                    for idx, row in df.iterrows():
                        file.write("【")
                        info = []
                        for col in columns:
                            info.append(f"{col}:{row[col]}")
                        infos = ",".join(info)
                        file.write(infos)
                        if idx != len(df) - 1:
                            file.write("】\n")
                        else:
                            file.write("】")
                os.remove(destination_file_path)
            gr.Info(f"Files have been uploaded to the {label_name} data table. Please proceed to create the knowledge base.")
        except:
            gr.Info("Please avoid duplicate uploads")

# Update Structured Data Table in Real Time
def update_datatable():
    return gr.update(choices=os.listdir(STRUCTURED_FILE_PATH))

# Update Unstructured Categories in Real Time
def update_label():
    return gr.update(choices=os.listdir(UNSTRUCTURED_FILE_PATH))

# Delete Category
def delete_label(label_name):
    if label_name is not None:
        for label in label_name:
            folder_path = os.path.join(UNSTRUCTURED_FILE_PATH, label)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                gr.Info(f"Category {label} has been deleted")

# Delete Data Table
def delete_data_table(table_name):
    if table_name is not None:
        for table in table_name:
            folder_path = os.path.join(STRUCTURED_FILE_PATH, table)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                gr.Info(f"Data table {table} has been deleted")