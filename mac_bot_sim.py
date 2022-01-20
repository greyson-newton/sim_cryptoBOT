# init
import matplotlib.pyplot as plt
import seaborn as sns
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Use white grid plot background from seaborn
sns.set(font_scale=1.5, style="whitegrid")
import os
import stat
from shutil import rmtree
from helpers import pdirs,pfnames,pdict
import pandas as pd
from os.path import exists


def run(args):

	# sim=bot_sim(args.fconfig)
	simcmds={0:{'market':'all','sim':'fast-sample','granularity':3600,
	'exchange':'coinbasepro','sim-enddate':'2017-01-01','verbose':'0'},

	1:{'market':'all','sim':'fast-sample','granularity':3600,
	'exchange':'coinbasepro','sim-enddate':'2017-01-01','verbose':'0'},

	# 2:{'market':'all','sim':'fast-sample','granularity':3600,
	# 'exchange':'coinbasepro','sim-startdate':'2017-01-01'}
	}

	all_coins=pd.read_csv('coinbase_codes.csv').ACR.tolist()[:1]
	from datetime import date,timedelta
	if len(args.coins)<1:
		print('default coins\n\tBTC & ETH')
		args.coins=['BTC','ETH']

	# sim=bot_sim(simcmd=args.sim,coins=args.coins)
	trades=dict()
	# {'yr':,'mth':,'day':}
	bot_results,params=[],[]
	sim=mac_bot_sim()
	sim.init(args.coins)	
	for i in range(args.run):
		for cnt,cmd in simcmds.items():
			# print('\t[MacCB-Sim] #',cnt+1,'--> STARTING ',pdict(cmd,size=50))
			sim.start(cmd)
			sim_results=sim.trade_history()
			bot_results.append(sim_results)
			for i in range(len(sim_results)):
				params.append(cmd)			
	sim.clear(all_coins)
			
			
	proc_results = pd.concat(bot_results)
	print('SIMULATION PROCESS RESULTS:\n',proc_results)
	proc_results['params']=params
	print('SIMULATION PROCESS RESULTS:\n',proc_results)
	log_name=log_dir+str(len(pfnames(log_dir)))+'_log'
	proc_results.to_csv(log_name)
	print('saving sim results to ',log_name)
	return log_name


def plot(args,log_name):
	import pandas as pd
	# init
	import matplotlib.pyplot as plt
	import seaborn as sns
	# Handle date time conversions between pandas and matplotlib
	from pandas.plotting import register_matplotlib_converters
	register_matplotlib_converters()

	sim_results=pd.read_csv(log_name)
	print('PLOTTING\n\t',sim_results)
	print(sim_results)
	fig, ax = plt.subplots(figsize=(10, 10))
	# Add x-axis and y-axis
	sim_results.groupby(by=['Market']).plot(x="Datetime", y="Profit", kind="line", ax=ax, color="C3")

	# ax.plot(sim_results['Datetime'],
	#         sim_results['Profit'],
	#         color='purple')
	# # Set title and labels for axes
	# ax.set(xlabel="Date",
	#        ylabel="Precipitation (inches)",
	#        title="Daily Total Precipitation\nBoulder, Colorado in July 2018")
	plt_name=plt_dir+str(len(pfnames(plt_dir)))+'_plot'
	fig.savefig(plt_dir)
	plt.show()

class mac_bot_sim:
	def __init__(self,config=None,simcmd=None,coins=None,base_dir=None):
		print('-->Setting Environment for Mac_Crypto Trading Bot Simulations')
		print('-->\t[MacCB-Sim]')
		self.sims=[]
		self.num_trades=0
		self.dfs=[]
		self.cmds=[]

		self.coins=['ETH','ADA']
		if coins is not None and type(coins)==list:
			self.coins=coins
		if simcmd is not None:
			self.simcmd=simcmd
			self.update_cmds(simcmd)
		# self.coins=['BTC','ETH','ADA','SOL','SHIB']
		self.base_name='cryptoBOT'
		if base_dir==None:
			self.base_dir=os.getcwd()+'/'
		else:
			self.base_dir=base_dir
		# print(self.base_dir)

		# check if config file passed
		if config is not None:
			if type(config)==dict:
				print('using update_dict')
				if 'all' in next(iter(config)).lower():
					for sim in self.sims:
						self.update_config(sim,config.get('all'))	
				else:			
					for bot,cfg in config.items():
						self.update_config(self.base_dir+'/'+bot+self.base_name+'/',cfg)
			elif type(config)==str:
				print('using cfg_file')
				for sim in self.sims:
					cpcmd='cp '+self.base_dir+config+" "+sim+'config.json'
					os.system(cpcmd)
				# for coin,sim in zip(self.coins,self.sims):
				# 	self.update_config(sim,{'base_currency':coin})

		# check is simcmd passed 

	def init(self,coins=None):
		if coins is None:
			coins=['BTC','ETH']
		if self.check():
			print('\n\t[MacCB-Sim]: Initializing bots for simulations','\n\t\t',coins,'\n')
			gitcmd='git clone https://github.com/greyson-newton/cryptoBOT.git'
			
			for coin in self.coins:
				sim_name=coin+'cryptoBOT'
				os.system(gitcmd)
				os.rename(self.base_name,sim_name)
				self.sims.append(self.base_dir+sim_name+'/')
				self.update_config(self.sims[-1],{'base_currency':coin})
		else:
			print('\n\t\t - using existing bots')


	def update_cmds(self,simcmd):
		if simcmd is not None and type(simcmd)==dict:
			if simcmd.get('market') == 'all':
				for sim,coin in zip(self.sims,self.coins):
					cmd='python3 pycryptobot.py '
					for param,value in simcmd.items():
						if param=='market':
							cmd+='--market '+coin+'-USD '
						else:
							cmd+='--'+param+' '+str(value)+' '
					self.cmds.append(cmd)

		# print('\n\tCMDS\n',self.cmds)
		
		

	# def get_trades(self):
	# 	for coin,sim in zip(self.coins,self.sims):
	# 		if exists(sim+'csv/trades.csv'):
	# 			print(pd.read_csv(sim+'csv/trades.csv'))
	# 			self.dfs.append(pd.read_csv(sim+'csv/trades.csv'))
	def add_trades(self):
		for coin,sim in zip(self.coins,self.sims):
			if exists(sim+'csv/trades.csv'):
				# print(pd.read_csv(sim+'csv/trades.csv'))
				self.dfs.append(pd.read_csv(sim+'csv/trades.csv'))
		# trades.drop('Unnamed: 0', axis=1, inplace=True)
		# trades.dropna()
		# print(self.trades)
		# if len(self.trades)<1:
		# 	self.trades=trades
		# else:
		# 	self.trades.append(trades)
		# self.num_trades+=len(trades)
		# print('\t\t|',coin,len(trades),' Num of Trades |\n')
		# print('\t\t-> | sim_trades |\n\n\t\t',trades)
		# else:
		# 	print('\t\t|',coin,len(trades),' NO Trades |\n')
				# print('\t\t',trades)						
	def ret_trades(self):
		return self.trades
	def trade_history(self):
		return pd.concat(self.dfs)
	def ret_cfg(self,sim):
		cfg_path=sim+'config.json'
		# print(cfg_path)
		cfg=pd.read_json(cfg_path)	
		config=cfg['coinbasepro'].config
		return config
	def set_cfg(self,sim,config):
		cfg_path=sim+'config.json'
		cfg=pd.read_json(cfg_path)
		cfg['coinbasepro'].config = config
		cfg.to_json(cfg_path)
	def update_config(self,sim,update_dict):
		config=self.ret_cfg(sim)
		# print('\n\t',sim.rsplit('/',2)[1],' OLD cfg\n',config)
		for param,value in update_dict.items():
			config[param]=value
		self.set_cfg(sim,config)
		# print('\n\t',sim.rsplit('/',2)[1],' NEW cfg\n',self.ret_cfg(sim))
		
	def check(self):
		# print('check')
		if len(self.sims) >0:
			# print('sims exist')
			return False
		else:
			for fname in pdirs(self.base_dir):
				# print(fname)
				if self.base_name in fname:
					# print('flagged')
					self.sims.append(self.base_dir+fname+'/')
			if len(self.sims) >0:
				# print('sims exist')
				return False					
			else:	
				return True
	# start
	def start(self,cmds=None):
		if cmds is not None:
			self.update_cmds(cmds)

		if len(self.cmds)>0:
			for sim,cmd,coin in zip(self.sims,self.cmds,self.coins):
				print('\n\t[MacCB-Sim]:',coin,'cmd_Simulation started','\n')
				print('\n\t\t - simcmd: \n\t\t')
				pdict(cmds,size=100)
				# print('\n\tSTART simcmd',coin)
				# print('\n\t\tCONFIG',self.ret_cfg(sim))				
				os.chdir(sim)
				os.system(cmd)
				# print(cmd) 
		else:
			for sim,coin in zip(self.sims,self.coins):
				print('\n\t[MacCB-Sim]:',coin,'cfg_Simulation started','\n')
				# print('\n\t\tCONFIG',self.ret_cfg(sim))
				os.chdir(sim)
				runcmd='python '+sim+'pycryptobot.py'
				# print(runcmd)
				os.system(runcmd)
				os.chdir(self.base_dir)

		# self.get_trades()
		self.add_trades()

	def clear(self,coins):
		print('\n\t[MacCB-Sim]: Simulations cleared','\n')
		# print(pdirs(self.base_dir))
		for fname in pdirs(self.base_dir):
			# print(fname)
			if self.base_name in fname:
				rmtree(self.base_dir+fname)
		# print(pdirs(self.base_dir))

import argparse
import ast
from datetime import date
base_dir=os.getcwd()+'/'
dtime = date.today().strftime("%m/%d/%y")
sim_dir=base_dir+'sim_results/'
os.makedirs(sim_dir, exist_ok=True )

n_files=len(pdirs('./sim_results/'))
n_logs=len(pdirs('./sim_results/'))

log_dir=sim_dir+str(n_logs)+'/logs/'
plt_dir=sim_dir+str(n_files)+'/plts/'

os.makedirs(log_dir, exist_ok=True )
os.makedirs(plt_dir, exist_ok=True )

parser = argparse.ArgumentParser()
parser.add_argument('--fconfig', help="newConfig.json")
parser.add_argument('--config', type=ast.literal_eval, help="CURR:dict(newConfig)")
parser.add_argument('--sim', type=ast.literal_eval, help="CURR:dict(newConfig)",default=None)
parser.add_argument('--coins', type=ast.literal_eval, help="[]",default=[])
parser.add_argument('--run', type=int, help="number of runs",default=1)

# # sim=bot_sim()
# {'market':'all','granularity':3600,'verbose':0,
# 'sim':'fast','sim-startdate':'2021-01-01','sim-enddate':'2021-01-01'}
# python3 pycryptobot.py --market XLM-EUR --granularity 3600 --verbose 0 --sim fast
args = parser.parse_args()
print(args)
# log_name=None:
log_name=run(args)
# if log_name is None:
# 	log_name
plot(args,log_name)

# trades['sim_num']=itrs
# print('\n\t-> TRADES',sim.dfs)
# print('\n\t-> TRADES',trades)
# print('\n\t-> TRADES',pd.DataFrame.from_dict(trades))

# sim.clear()

# else:
# 	if args.fconfig is None:
# 		sim=bot_sim(args.config)
# 	else:
# 		sim=bot_sim(args.fconfig)

# clear
# rmcmd=''

# sim_time={'yr':0,'mth':0,'day':14}
# start_date={'yr':2017,'mth':1,'day':14}
# timeframe={'yr':3,'mth':0,'day':0}
# def t2str(t):
# 	return str(t.get('yr'))+' '
# def t2day(t):
# 	days=mth
# def t_op(op,t1,t2):
# 	if op=='add':
# 		yr=t1.get('yr')+t2.get('yr')
# 		mth=t1.get('mth')+t2.get('mth')
# 		day=t1.get('dat')+t2.get('day')
# 		return {'yr':yr,'mth'mth:,'day':day}
# 	elif op=='sub':
# 		yr=t1.get('yr')-t2.get('yr')
# 		mth=t1.get('mth')-t2.get('mth')
# 		day=t1.get('dat')-t2.get('day')
# 		return {'yr':yr,'mth'mth:,'day':day}	