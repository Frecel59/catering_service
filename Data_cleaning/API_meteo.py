from Clean_data import clean_file_in_folder, data_folder


start_date = clean_file_in_folder(data_folder).Date.min()
end_date = clean_file_in_folder(data_folder).Date.max()


if __name__ == '__main__':
    print(start_date, end_date)
