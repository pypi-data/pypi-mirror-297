class AuditLogData:
    def __init__(self, input_data):
        if type(input_data) == pd.core.frame.DataFrame :
            self.df = input_data
        else:
            print("Not valid input datatype")

        assert self.check_data()
        self.df.sort_values(by='task_time',inplace=True)

        self.__audit_duration__()

        self.__get_full_ts__()
        
            

    def check_data(self):
        if set(['task_time']).issubset(set(self.df.columns.tolist())):
            return True
        return False

    def get_data(self):
        return self.df

    def __audit_duration__(self):
        if 'aht' in self.df.columns:
            return
        elif 'end_time' in self.df.columns and 'start_time' in self.df.columns:
            self.df['aht'] = (self.df['end_time'] - self.df['start_time']).dt.total_seconds()
            return
        else:
            print("Please ensure your input data contains columns 'start_time'+'end_time' or 'aht' to estimate processing duration! ")

    def __get_full_ts__(self):
        ### 按照最小时间单元的全部时间戳 
        self.full_indices = \
        pd.date_range(start = self.df.task_time.dt.floor('1D').min(), 
                      end   = self.df.task_time.dt.floor('1D').max() + timedelta(days=1),
                      freq = '1T')[:-1]        
      

    def display(self, steps = '5T'):
        self.df.groupby(self.df.task_time.dt.floor(steps)).size().plot(figsize = (12,5),grid = 'y')
        plt.xlabel('date')
        plt.ylabel('audit amount')
        plt.show()