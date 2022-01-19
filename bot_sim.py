# init
import os
import stat
from shutil import rmtree
from helpers import pdirs,pfnames
import pandas as pd
class bot_sim:
	def __init__(self,config=None):
		self.sims=[]
		self.coins=['BTC','ETH','ADA','SOL','SHIB']
		self.base_name='cryptoBOT'
		self.base_dir=os.getcwd()+'\\'
		print(self.base_dir)
		if self.check():
			gitcmd='git clone https://github.com/greyson-newton/cryptoBOT.git'
			
			for coin in self.coins:
				sim_name=coin+'cryptoBOT'
				os.system(gitcmd)
				os.rename(self.base_name,sim_name)
				self.sims.append(self.base_dir+sim_name+'\\')
				self.update_config(self.sims[-1],{'base_currency':coin})
			if config is None:
				self.start()
			else:
				if type(config)==dict:
					if 'all' in next(iter(config)).lower():
						for sim in self.sims:
							self.update_config(sim,config.get('all'))	
					else:			
						for bot,cfg in config.items():
							self.update_config(self.base_dir+'\\'+bot+self.base_name+'\\',cfg)
				else:
					for sim in self.sims:
						cpcmd='xcopy '+self.base_dir+config+" "+sim+'config.json'
						os.system(cpcmd)
					for coin,sim in zip(self.coins,self.sims):
						self.update_config(sim,{'base_currency':coin})
				self.start()

		if config is None:
			self.start()
		else:
			if type(config)==dict:

				if 'all' in next(iter(config)).lower():
					for sim in self.sims:
						self.update_config(sim,config.get('all'))	
				else:			
					for bot,cfg in config.items():
						self.update_config(self.base_dir+'\\'+bot+self.base_name+'\\',cfg)
			else:
				for sim in self.sims:
					cpcmd='xcopy '+self.base_dir+config+" "+sim+'config.json'
					os.system(cpcmd)
					for coin,sim in zip(self.coins,self.sims):
						self.update_config(sim,{'base_currency':coin})					
			self.start()				
	def update_config(self,sim,update_dict):
		cfg_path=sim+'config.json'
		cfg=pd.read_json(cfg_path)
		# print(cfg)
		config=cfg['coinbasepro'].config

		for param,value in update_dict.items():
			config[param]=value
		print(config)
		cfg['coinbasepro'].config = config
		print(config.get('base_currency'))
		print(cfg['coinbasepro'].config)
		cfg.to_json(cfg_path)
	def check(self):
		print('check')
		if len(self.sims) >0:
			print('sims exist')
			return False
		else:
			for fname in pdirs(self.base_dir):
				# print(fname)
				if self.base_name in fname:
					print('flagged')
					self.sims.append(self.base_dir+fname+'\\')
			if len(self.sims) >0:
				print('sims exist')
				return False					
			else:	
				return True
	# start
	def start(self):

		print('starting sims\n\t->',self.sims)
		for sim in self.sims:
			os.chdir(sim)
			# runcmd='python '+sim+'pycryptobot.py'
			# print(runcmd)
			os.system('python pycryptobot.py')
			os.chdir(self.base_dir)
	def clear(self):
		# print(pdirs(self.base_dir))
		for fname in pdirs(self.base_dir):
			print(fname)
			if self.base_name in fname:
				print('flagged')
				return False
		return True

import argparse
import ast
parser = argparse.ArgumentParser()
parser.add_argument('--fconfig', type=str, help="nweConfig.json")
parser.add_argument('--config', type=ast.literal_eval, help="CURR:dict(newConfig)")

args = parser.parse_args()
print(args)
sim=bot_sim(args.fconfig)
if args.fconfig is None:
	sim=bot_sim(args.config)
else:
	sim=bot_sim(args.fconfig)

# clear
# rmcmd=''

