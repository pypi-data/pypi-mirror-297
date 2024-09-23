import pandas as pd
from typing import Union
from pathlib import Path
from BoschRpaMagicBox.helper_functions import *
from calendar import monthrange


def copy_as_new_file(from_folder_path: str, from_file_name: str, update_folder_path: str, update_file_name: str, from_period: str, user_name: str, user_password: str,
                     server_ip: str, server_name: str, share_name: str, port: int):
    """This function is used to copy files from from_folder or sub_folder to update folder

    Args:

        from_folder_path: This is the from_folder_path
        from_file_name: This is the file name that contains common file name fragment
        update_folder_path: This is the target folder path
        update_file_name: This is the file name of update file
        from_period(str): This is the start period
        user_name(str): This is the username
        user_password(str): This is the password
        server_ip(str): This is the ip address of the public folder, which can be same as server name
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
    """
    from_file_extension = Path(from_file_name).suffix
    save_update_file_name = f"{update_file_name}{from_period}.{from_file_extension}"

    from_file_path = from_folder_path + os.sep + from_file_name
    update_file_path = update_folder_path + os.sep + save_update_file_name

    is_from_file_exist = smb_check_file_exist(user_name, user_password, server_ip, server_name, share_name, from_file_path, port)

    if is_from_file_exist:
        from_file_obj = smb_load_file_obj(user_name, user_password, server_ip, server_name, share_name, from_file_path, port)
        smb_store_remote_file_by_obj(user_name, user_password, server_ip, server_name, share_name, update_file_path, from_file_obj, port)
        print(f'--------------- copy file for {from_file_path} to {update_file_path}---------------')
    else:
        print('Target file is not found！')


def hrs_calculate_duration(hrs_time_data: Union[pd.DataFrame, None], from_column: str, from_period: str, new_column: str, ) -> pd.DataFrame:
    """This function is used to calculate time difference between values of from column and today

    Args:
        hrs_time_data(pd.DataFrame): This is the hrs time related data
        from_column:This is the column name
        from_period(str): This is the start period
        new_column: This is the new column that will record compare result
    """
    hrs_time_data[from_column].fillna('', inplace=True)
    hrs_time_data[from_column] = hrs_time_data[from_column].astype(str)
    hrs_time_data[from_column] = hrs_time_data[from_column].str.strip().str.split(' ', expand=True)[0]
    hrs_time_data[from_column] = (pd.to_datetime(hrs_time_data[from_column], errors='coerce')).dt.date
    for row_index in hrs_time_data.index:
        row_data = hrs_time_data.loc[row_index]
        previous_date = row_data[from_column]
        if not pd.isna(previous_date) and previous_date:
            if from_period:
                current_date = datetime.datetime.strptime(f'{from_period[:4]}-{from_period[4:6]}-{from_period[6:8]}', '%Y-%m-%d').date()
            else:
                current_date = datetime.datetime.now().date()
            day_duration = (current_date - previous_date).days
            year_duration = current_date.year - previous_date.year
            hrs_time_data.loc[row_index, new_column] = f'{day_duration} days'
            if previous_date.month == current_date.month:
                if previous_date.day == current_date.day and year_duration > 0:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                elif previous_date.month == 2 and previous_date.day == 29 and monthrange(current_date.year, current_date.month)[1] == 28 and current_date.day == 28:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                else:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
            else:
                hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
        else:
            hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
    return hrs_time_data
