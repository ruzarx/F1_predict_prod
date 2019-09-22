import pandas as pd
from gc import collect
import os

class Data_import:
    
    def __init__(self):

        self.path_dir = './data/'

        self.needed_columns = {'practice': ['Pos', 'Driver', 'Car', 'Time', 'Laps', 'Session', 'Year', 'Race_no', 'Track'],
                    'qualifying': ['Pos', 'Driver', 'Car', 'Q1', 'Q2', 'Q3', 'Laps', 'Year', 'Race_no', 'Track'],
                    'race': ['Pos', 'Driver', 'Car', 'Laps', 'Time/Retired', 'Year', 'Race_no', 'Track']}

        if not self.existance_check():
            quit()

        self.df_p1 = self.practice('practice-1')
        self.df_p2 = self.practice('practice-2')
        self.df_p3 = self.practice('practice-3')

        self.df_q = self.qualifying()
        self.df_r = self.race()

        print("Import successful")
        print(f"Available races {self.races_available}. Of them:")
        print(f"Missing practices {self.missing_practices}")
        print(f"Missing qualifications {self.missing_qualifications}")
        print(f"Missing races {self.missing_races}")

    def existance_check(self):

        if not os.path.exists(self.path_dir):
            print(f"{self.path_dir} does not exist")
            return False

        for session_dir in ['practice-1', 'practice-2', 'practice-3', 'qualifying', 'race']:
            if not os.path.exists(self.path_dir + session_dir):
                print(f"Location {session_dir} does not exist")
                return False

        # Checking existing files
        files_existing = [os.listdir(self.path_dir + session_dir) for session_dir in ['practice-1', 
                'practice-2', 'practice-3', 'qualifying', 'race']]

        # Checking how many of them match
        self.races_available = len(list(set(files_existing[0]).intersection(set(files_existing[1]).intersection(set(files_existing[2]).intersection(set(files_existing[3]).intersection(set(files_existing[4])))))))

        del files_existing
        collect()

        if self.races_available < 10:
            print(f"Amount of available data is {self.races_available} races. Too few")
            return False
        
        return True

    def practice(self, practice_no):

        self.missing_practices = 0

        practice_path = self.path_dir + practice_no + '/'

        files_list = os.listdir(practice_path)

        self.current_df = pd.read_csv(practice_path + files_list[0])
        if self.check_columns('practice'):
            self.practice_df = self.current_df[self.needed_columns['practice']]
        else:
            self.missing_practices += 1

        for next_file in files_list[1:]:
            self.current_df = pd.read_csv(practice_path + next_file)
            if self.check_columns('practice'):
                self.practice_df = self.practice_df.append(self.current_df[self.needed_columns['practice']])
            else:
                self.missing_practices += 1

        return self.practice_df

    def qualifying(self):

        self.missing_qualifications = 0

        qualifying_path = self.path_dir + 'qualifying/'

        files_list = os.listdir(qualifying_path)

        self.current_df = pd.read_csv(qualifying_path + files_list[0])
        if self.check_columns('qualifying'):
            self.qualifying_df = self.current_df[self.needed_columns['qualifying']]
        else:
            self.missing_qualifications += 1

        for next_file in files_list[1:]:
            self.current_df = pd.read_csv(qualifying_path + next_file)
            if self.check_columns('qualifying'):
                self.qualifying_df = self.qualifying_df.append(self.current_df[self.needed_columns['qualifying']])
            else:
                self.missing_qualifications += 1

        return self.qualifying_df

    def race(self):

        self.missing_races = 0

        race_path = self.path_dir + 'race/'

        files_list = os.listdir(race_path)

        self.current_df = pd.read_csv(race_path + files_list[0])
        if self.check_columns('race'):
            self.race_df = self.current_df[self.needed_columns['race']]
        else:
            self.missing_races += 1

        for next_file in files_list[1:]:
            self.current_df = pd.read_csv(race_path + next_file)
            if self.check_columns('race'):
                self.race_df = self.race_df.append(self.current_df[self.needed_columns['race']])
            else:
                self.missing_races += 1

        return self.race_df

    def check_columns(self, session_type):

        if self.current_df.columns.all() in self.needed_columns[session_type]:
            return True
        else:
            return False