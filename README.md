﻿# Deep Reinforcement Learning

1,Deep Reinforcement Learning

2,Gym http://gym.openai.com/

Settings:

# Export different directory modules
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# using gpu
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 1.0
config.gpu_options.allow_growth = True
tf.compat.v1.Session(config=config)

# using cpu
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
