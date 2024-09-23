import pandas as pd
import numpy as np
import re
import cvxpy as cp
import seaborn as sns
from tqdm import tqdm
from datetime import timedelta
from itertools import product
import matplotlib.pyplot as plt
import pyscipopt
# Set the font to a font that supports Chinese characters
try:
	plt.rcParams['font.sans-serif'] = ['Songti SC']  
	plt.rcParams['axes.unicode_minus'] = False  # Ensure that minus signs are displayed correctly
except:
	pass
import warnings
warnings.filterwarnings('ignore')