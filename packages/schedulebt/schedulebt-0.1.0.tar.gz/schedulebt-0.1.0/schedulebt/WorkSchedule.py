 
class WorkSchedule:
    '''
        按照小时，优化L1范数排班
    '''
    def __init__(self, audit_data, schedule_constraints, N, block_size = 1):
        assert type(audit_data) == AuditLogData
        self.block_size = block_size
        self.audit_data = audit_data
        self.schedule_constraints = schedule_constraints
        self.dim = int(1440/self.block_size)
        self.N = N

        # 构造排班矩阵
        self.__add_schedule_constraints__()

        # 计算日均各时段工作量
        self.__block_workload__()

    def __block_workload__(self):
        assert 60 % self.block_size == 0
        ts = pd.MultiIndex.from_product([list(range(0,24)), [int(j) for j in np.linspace(0,60,60//self.block_size+1)][:-1]])
        self.workload = \
        self.audit_data.get_data().groupby([self.audit_data.get_data().task_time.dt.floor('1D'),
                                            self.audit_data.get_data().task_time.dt.hour,
                                            self.audit_data.get_data().task_time.dt.floor(str(self.block_size)+'T').dt.minute])['aht']\
        .sum().unstack(level=0)\
        .mean(axis = 1).reindex(ts).fillna(0).values.flatten()



    def __add_schedule_constraints__(self):
        # 每个班次的休息时间
        vacant = np.zeros(24,dtype=int) - 1
        for _, z in self.schedule_constraints.iterrows():
            vacant[z[0]] = z[1]
            
        # 排班矩阵
        self.A = np.zeros((self.dim,24))
        for j in range(24):
            if vacant[j] < 0:
                continue
            indices = [int(j1) % self.dim for j1 in np.linspace(j*int(60/self.block_size),
                                                                ((j+8)*(int(60/self.block_size)) + int(60/self.block_size) - 1),
                                                                9*int(60/self.block_size))]
            self.A[indices,j] = 1
            self.A[vacant[j]*int(60/self.block_size):(vacant[j]+1)*int(60/self.block_size) ,j] = 0
                
        
    def optimize(self):
        '''
            定义优化问题
        '''
        b = self.workload
    
        # 定义变量，这里指定为整数
        x = cp.Variable(self.A.shape[1], integer=True)
    
        # 定义目标函数（L1范数最小化）
        objective = cp.Minimize(cp.norm(self.A @ x * (self.block_size * 60) - b, 1))
        
        # 定义约束条件
        constraints = [x >= 0]
        # constraints.append(A @ x * (block_size * 60) >= 0.50*b)
        # constraints.append(sum(A @ x * (block_size * 60)) >= 1.0*avg_amt)
        # 总人数等于当天在班人力
        constraints.append(sum(x) == self.N)

        # 可排班时点
        v = np.ones(24)
        for _, z in self.schedule_constraints.iterrows():
            v[z[0]] = 0
        
       # # 固定23:00开始的班次排一个人
       #  v1 = np.zeros(24)
       #  v1[23] = 1
        
        constraints.append(x @ v == 0)
        # constraints.append(x @ v1 >= 1)
        prob = cp.Problem(objective, constraints)
        prob.solve(solver='SCIP')
        self.opt_schedule = x
        self.opt_mat = pd.DataFrame({'starts': list(range(24)), 'workers': [int(j) for j in x.value]})
    
        # 分钟级审核人力状态
        hours = []
        minutes = []
        block_capacity = (self.A@x.value)*60*self.block_size
        ts = []
        for h, m in product(range(0,24), np.linspace(0,60-self.block_size,int(60/self.block_size))):
            hours.append(h)
            minutes.append(m)
            ts.append(pd.to_datetime('2000-01-01') + timedelta(seconds=h*3600+m*60))
    
        self.opt_capacity = pd.DataFrame({'audit_capacity': block_capacity, 'workload': self.workload})
        self.opt_capacity.index = pd.Series(ts).dt.time

    def plot_schedule(self):
        fig,ax = plt.subplots(figsize=(12,6))
        self.opt_capacity.plot(ax=ax,use_index=False)
        plt.xticks([j * 120 for j in range(12)],self.opt_capacity.index[[j * 120 for j in range(12)]],rotation = 45)
        plt.legend()
        plt.ylabel('每分钟总工作量(单位：人 x 秒）')
        plt.xlabel('timestamps')
        plt.show()


    def backtest(self, waiting_max = 1e8, enable_priority = False):
        '''
            回测当前排班下的时效
        '''

        hours = np.array([t.hour  for t in work_schedule.opt_capacity.index.tolist()])
        minutes = np.array([t.minute  for t in work_schedule.opt_capacity.index.tolist()])
        # 初始状态
        total_logs = []
        waiting_queue = pd.DataFrame(columns = self.audit_data.df.columns)
    
        # 模拟审核过程
        for t in tqdm(self.audit_data.full_indices, total = len(self.audit_data.full_indices)):
            ## 队列送审, 根据优先级和时间判定队列里任务的排序
            waiting_queue = pd.concat([waiting_queue, 
                                       self.audit_data.df.loc[(self.audit_data.df.task_time >= t)\
                                                             &(self.audit_data.df.task_time < t+timedelta(seconds=60))]],
                                       axis=0)

            # 是否存在优先级排序
            if enable_priority:
                waiting_queue.sort_values(by=['priority','task_time'],inplace=True)
            
            ## 完成每个case所需要的累计审核时长
            waiting_queue['cum_cap'] = waiting_queue.aht.cumsum()
            
            ## 改分钟内存在的审核时长（实际审核能力）
            cap = self.opt_capacity.loc[(hours == t.hour) & \
                                        (minutes == t.minute),'audit_capacity'].values[0]
            
            ## 实际审出时间标记: 超时自动生效和人力可以审核完成的情形
            logs_man  = waiting_queue.loc[(waiting_queue.cum_cap < cap)] # 人审二确
            logs_auto = waiting_queue.loc[(waiting_queue.cum_cap >= cap) & \
                                          (t+timedelta(seconds=60-waiting_max) > waiting_queue.task_time)]
            logs_man['finish_type'] = 'man'
            logs_auto['finish_type'] = 'auto'
            logs = pd.concat([logs_man, logs_auto],axis=0)
            logs['end_time'] = t+timedelta(seconds=60)
            total_logs.append(logs)
            
            ## 更新等待审核状态
            # 可以审核完成的case
            waiting_queue = waiting_queue.loc[(waiting_queue.cum_cap >= cap)&(t+timedelta(seconds=60-waiting_max) <= waiting_queue.task_time)]
    
            # 超过最大等等时长自动生效的case
            
            
        self.audit_logs = pd.concat(total_logs)
        self.audit_logs['duration'] = (self.audit_logs.end_time - self.audit_logs.task_time).dt.total_seconds().div(60)


    def get_percentiles(self):
        self.n_days = self.audit_logs.task_time.dt.floor('1D').nunique()
        d_percent = self.audit_logs.duration.quantile([(5 * j)/100 for j in range(1,21)])
        d_amt = self.audit_logs.duration.groupby(
                pd.cut(work_schedule.audit_logs.duration,
               [0]+d_percent.values.tolist())).size()
        d_daily_amt = d_amt / self.n_days
        df_percentiles = d_daily_amt.to_frame('daily_amt').join(d_amt.to_frame('total_amt'))
        df_percentiles['percentiles'] = d_percent.index
        df_percentiles['quantiles'] = d_percent.values
        
        
        return df_percentiles

    def percentile(self, p):
        return self.audit_logs.duration.quantile(p)