import warnings
warnings.filterwarnings("ignore")
import math
import random
import names
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


agent: dict = {
    "agent_name": [],
    "money": [],
    "food": [],
    "energy": [],
    "health": [],
    "alive": [],
    "living_strategy": [],
    "agentsInteracted": [],
    "alliesList": []
}

#livingStrategies: list = ["risk-taker", "worker", "survivalist", "adaptive"]
livingStrategies: list = ["adaptive"]
#livingStrategies: list = ["risk-taker", "worker", "adaptive"]

days: list = []
agentAliveCount: list = []
agentAvgMoney: list = []
highestAgentMoney: list = []
lowestAgentMoney: list = []
livingAgentsIndex: list = []

initialriskTakerCount = 0
initialWorkerCount = 0
initialSurvivalistCount = 0
initialAdaptiveCount = 0
riskTakerATP: list = []
workerATP: list = []
survivalistATP: list = []
adaptiveATP: list = []

numTrades = 0

numKnownTrades = 0

foodAvailability: int = 50

foodAvailabilityHistory: list = []


#adaptiveAgentQTable: dict = {('low_money', 'medium_food', 'high_energy', 'high_health'): {'work': 230.3897359848621, 'rest': 101.1184656331137, 'buy_food': 176.27371110572702}, ('low_money', 'high_food', 'low_energy', 'low_health'): {'work': 83.71633888400032, 'rest': 172.68790917222515, 'buy_food': 48.23205168847488}, ('medium_money', 'high_food', 'medium_energy', 'high_health'): {'work': 373.98852375859667, 'rest': 342.4560490975992, 'buy_food': 369.7618822557574}, ('medium_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 196.48886732109293, 'rest': 146.60550479539418, 'buy_food': 274.7386037744029}, ('low_money', 'high_food', 'medium_energy', 'low_health'): {'work': 98.20307756048815, 'rest': 209.5958271349681, 'buy_food': 51.20495560491058}, ('low_money', 'high_food', 'medium_energy', 'high_health'): {'work': 379.1733187283064, 'rest': 342.85553995066834, 'buy_food': 345.00144642870634}, ('high_money', 'low_food', 'high_energy', 'medium_health'): {'work': 81.54092291012687, 'rest': 67.95884427513674, 'buy_food': 238.95613788181527}, ('low_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 333.4985589865278, 'rest': 302.6688928274389, 'buy_food': 290.69426061729484}, ('high_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 64.2958149204374, 'rest': 63.9871416217591, 'buy_food': 122.50725732343278}, ('medium_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 47.12443815021452, 'rest': 132.782092905187, 'buy_food': 55.51030776138338}, ('low_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 53.55835301991931, 'rest': 64.37835462743644, 'buy_food': -12.970508366909838}, ('medium_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 104.57904510628683, 'rest': 144.6365851648926, 'buy_food': 198.42629126481145}, ('low_money', 'medium_food', 'low_energy', 'low_health'): {'work': 34.476241639366876, 'rest': 62.32583166592162, 'buy_food': -15.676641892412663}, ('low_money', 'high_food', 'low_energy', 'high_health'): {'work': 345.5460721978165, 'rest': 340.01369744512925, 'buy_food': 305.58082243678496}, ('high_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 143.3442422960805, 'rest': 131.07169619917804, 'buy_food': 241.18549137985775}, ('low_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 61.39296391160105, 'rest': 63.972487022160145, 'buy_food': 20.35612148733795}, ('high_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 338.1465015005085, 'rest': 335.5464643417306, 'buy_food': 347.6748435798549}, ('medium_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 318.60597513873506, 'rest': 330.50690950739363, 'buy_food': 323.27631958412275}, ('low_money', 'high_food', 'low_energy', 'medium_health'): {'work': 314.6525472050715, 'rest': 322.6230259545311, 'buy_food': 269.4386775225967}, ('low_money', 'low_food', 'low_energy', 'medium_health'): {'work': 24.4081276097871, 'rest': 9.074751030077698, 'buy_food': -3.71225042158064}, ('low_money', 'low_food', 'low_energy', 'high_health'): {'work': 19.999999999999986, 'rest': -12.949136205719794, 'buy_food': -18.19999999999999}, ('low_money', 'medium_food', 'low_energy', 'high_health'): {'work': 69.91701364750112, 'rest': 50.406243983714916, 'buy_food': 14.206346365262322}, ('low_money', 'low_food', 'low_energy', 'low_health'): {'work': -15.790640499254323, 'rest': -0.2513812794061465, 'buy_food': -39.63373448996097}, ('medium_money', 'low_food', 'low_energy', 'medium_health'): {'work': 20.650311557889314, 'rest': 29.34471149916942, 'buy_food': 31.296347205370648}, ('low_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 37.37391969471633, 'rest': -14.11055927628383, 'buy_food': 6.476192874923228}, ('low_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 140.2395443317101, 'rest': 58.03998927682586, 'buy_food': 92.16395809621922}, ('medium_money', 'low_food', 'high_energy', 'medium_health'): {'work': 106.19064359732971, 'rest': 63.66349843443182, 'buy_food': 189.27270631876982}, ('low_money', 'low_food', 'high_energy', 'medium_health'): {'work': 70.96574788511093, 'rest': -10.733163462556469, 'buy_food': 18.57689638380142}, ('medium_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 47.20403343792991, 'rest': 36.08023153080661, 'buy_food': 107.24480198065588}, ('low_money', 'high_food', 'high_energy', 'high_health'): {'work': 413.39447354016954, 'rest': 348.5432221181125, 'buy_food': 387.09652449661564}, ('medium_money', 'medium_food', 'low_energy', 'high_health'): {'work': 71.8278455992462, 'rest': 93.4742554120951, 'buy_food': 144.44425651626202}, ('medium_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 63.01803852422974, 'rest': 86.76855126272844, 'buy_food': 71.92076102912498}, ('medium_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 122.13622711943604, 'rest': 136.6687062049397, 'buy_food': 225.34012321569696}, ('low_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 150.70438482497258, 'rest': 35.055320708349896, 'buy_food': 103.14561109158595}, ('medium_money', 'low_food', 'medium_energy', 'high_health'): {'work': 59.5134039096375, 'rest': 8.336056588461341, 'buy_food': 125.91882605440998}, ('low_money', 'low_food', 'medium_energy', 'high_health'): {'work': 60.269188340506695, 'rest': -12.37939110559413, 'buy_food': 16.502544290609666}, ('medium_money', 'high_food', 'low_energy', 'high_health'): {'work': 337.2360487059686, 'rest': 345.15297209143307, 'buy_food': 334.996120448555}, ('medium_money', 'high_food', 'high_energy', 'medium_health'): {'work': 312.9123445796132, 'rest': 307.98662093812123, 'buy_food': 321.8849607429017}, ('high_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 171.79713992590965, 'rest': 181.10403647883084, 'buy_food': 285.9969573497939}, ('low_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 204.69287699398626, 'rest': 131.9254791330624, 'buy_food': 141.63651894879283}, ('low_money', 'low_food', 'high_energy', 'low_health'): {'work': -49.52729546760624, 'rest': -74.12997412062415, 'buy_food': -84.72135879899196}, ('low_money', 'high_food', 'high_energy', 'medium_health'): {'work': 327.6507901385178, 'rest': 295.77884276729645, 'buy_food': 291.4511792728175}, ('medium_money', 'high_food', 'low_energy', 'low_health'): {'work': 171.92115319387202, 'rest': 253.9041691717417, 'buy_food': 153.05824033874475}, ('medium_money', 'high_food', 'high_energy', 'low_health'): {'work': 76.25181244485061, 'rest': 137.4997473106655, 'buy_food': 80.90805726619769}, ('medium_money', 'medium_food', 'low_energy', 'low_health'): {'work': 16.441783230118446, 'rest': 105.23296915400283, 'buy_food': 53.64984693444289}, ('low_money', 'low_food', 'medium_energy', 'low_health'): {'work': -22.750061028553933, 'rest': -38.801288993343334, 'buy_food': -49.60000327388248}, ('medium_money', 'low_food', 'high_energy', 'high_health'): {'work': 99.86616990435562, 'rest': 47.306764503156735, 'buy_food': 184.7829096420541}, ('low_money', 'low_food', 'high_energy', 'high_health'): {'work': 94.33742684996952, 'rest': 12.668299493977846, 'buy_food': 29.744442198198144}, ('medium_money', 'low_food', 'medium_energy', 'low_health'): {'work': -9.15136360326073, 'rest': 37.13796377076027, 'buy_food': 28.238643803481168}, ('medium_money', 'medium_food', 'high_energy', 'low_health'): {'work': 46.97294208361093, 'rest': 123.76464540844914, 'buy_food': 84.35330674586197}, ('medium_money', 'medium_food', 'high_energy', 'high_health'): {'work': 220.3145001879773, 'rest': 197.1871490106888, 'buy_food': 324.9989124478391}, ('medium_money', 'high_food', 'medium_energy', 'low_health'): {'work': 129.35354140802346, 'rest': 215.9457049014806, 'buy_food': 123.3518389874687}, ('low_money', 'high_food', 'high_energy', 'low_health'): {'work': 99.48418522774597, 'rest': 183.81879269931719, 'buy_food': 66.9204755355996}, ('high_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 119.6898224809001, 'rest': 184.7859462774998, 'buy_food': 265.18586865566675}, ('medium_money', 'low_food', 'high_energy', 'low_health'): {'work': 12.89110441757939, 'rest': 15.285867656839503, 'buy_food': 74.92765794999725}, ('medium_money', 'low_food', 'low_energy', 'high_health'): {'work': 14.414402490150945, 'rest': 5.961077350254029, 'buy_food': 52.549230380568794}, ('medium_money', 'high_food', 'high_energy', 'high_health'): {'work': 400.80734918568476, 'rest': 348.78883378249554, 'buy_food': 405.1600056187859}, ('medium_money', 'high_food', 'low_energy', 'medium_health'): {'work': 313.82190189021065, 'rest': 325.4699757472741, 'buy_food': 308.24556806925153}, ('high_money', 'low_food', 'high_energy', 'high_health'): {'work': 138.73875806898818, 'rest': 83.83691249568994, 'buy_food': 196.08661946823554}, ('high_money', 'medium_food', 'high_energy', 'low_health'): {'work': 27.548806883480143, 'rest': 98.57523886881417, 'buy_food': 53.87257328386934}, ('high_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 49.21205449408767, 'rest': 179.67555625406408, 'buy_food': 74.08429327879287}, ('high_money', 'high_food', 'high_energy', 'low_health'): {'work': 32.04835853203027, 'rest': 57.08269185928541, 'buy_food': 52.878644409755566}, ('high_money', 'high_food', 'medium_energy', 'low_health'): {'work': 102.71842430331795, 'rest': 184.77918752171044, 'buy_food': 174.21691016193785}, ('high_money', 'high_food', 'high_energy', 'medium_health'): {'work': 304.4327856379349, 'rest': 314.2080453459145, 'buy_food': 332.9389444184883}, ('high_money', 'medium_food', 'high_energy', 'high_health'): {'work': 239.01688574455235, 'rest': 143.21375544932073, 'buy_food': 359.0933862366512}, ('high_money', 'high_food', 'high_energy', 'high_health'): {'work': 396.2391890936524, 'rest': 354.0232954023536, 'buy_food': 403.4849282471445}, ('low_money', 'medium_food', 'high_energy', 'low_health'): {'work': 91.71628444423074, 'rest': 75.475176774972, 'buy_food': 20.31238362947125}, ('high_money', 'low_food', 'medium_energy', 'high_health'): {'work': 43.6456293069535, 'rest': 23.340332386348315, 'buy_food': 170.53725368160605}, ('high_money', 'high_food', 'medium_energy', 'high_health'): {'work': 366.97635335337, 'rest': 350.1717916855619, 'buy_food': 373.316442219639}, ('high_money', 'low_food', 'medium_energy', 'low_health'): {'work': 18.49069187884879, 'rest': 34.855213779705004, 'buy_food': 82.36345140897802}, ('medium_money', 'low_food', 'low_energy', 'low_health'): {'work': -15.626740264697474, 'rest': 22.63731386468499, 'buy_food': -10.342421880000025}, ('high_money', 'low_food', 'high_energy', 'low_health'): {'work': -4.20426435123162, 'rest': 33.50133203967388, 'buy_food': 54.92326408237799}, ('high_money', 'high_food', 'low_energy', 'high_health'): {'work': 337.86967029105045, 'rest': 352.3145902864129, 'buy_food': 346.89426720837815}, ('high_money', 'high_food', 'low_energy', 'low_health'): {'work': 127.40133775290691, 'rest': 304.1803351607734, 'buy_food': 159.39502649703684}, ('high_money', 'high_food', 'low_energy', 'medium_health'): {'work': 337.61984262211377, 'rest': 357.1748297672509, 'buy_food': 346.9527283808326}, ('high_money', 'low_food', 'low_energy', 'low_health'): {'work': -6.76400817963845, 'rest': 47.67003007836819, 'buy_food': -0.23571140449844297}, ('high_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 98.0896615808182, 'rest': 160.8746786516608, 'buy_food': 138.1854031591358}, ('high_money', 'low_food', 'low_energy', 'medium_health'): {'work': 43.141275667840674, 'rest': 42.9666280720363, 'buy_food': 83.83043581265622}, ('high_money', 'low_food', 'low_energy', 'high_health'): {'work': 12.793242715186805, 'rest': 8.987307169880305, 'buy_food': 38.25236933217231}, ('high_money', 'medium_food', 'low_energy', 'high_health'): {'work': 71.4778477127482, 'rest': 103.51563436435713, 'buy_food': 200.84705140577626}, ('high_money', 'medium_food', 'low_energy', 'low_health'): {'work': 11.384572508953017, 'rest': 123.11252596884718, 'buy_food': 49.41718256881065}}

#adaptiveAgentQTable: dict = {('medium_money', 'high_food', 'high_energy', 'low_health'): {'work': 256.5359029307498, 'rest': 288.07678826774816, 'buy_food': 225.93829284825065}, ('low_money', 'low_food', 'medium_energy', 'low_health'): {'work': 39.92420121269706, 'rest': 22.717966104375776, 'buy_food': 31.19010946804871}, ('low_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 308.99620263055317, 'rest': 267.52418849254633, 'buy_food': 239.81648225861653}, ('medium_money', 'high_food', 'medium_energy', 'low_health'): {'work': 274.7439424864583, 'rest': 291.53250428451594, 'buy_food': 250.91349169108102}, ('low_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 258.94833310347775, 'rest': 249.66411287640386, 'buy_food': 220.12428754317102}, ('low_money', 'low_food', 'high_energy', 'medium_health'): {'work': 144.6682575248049, 'rest': 51.07220390282598, 'buy_food': 114.38539760328021}, ('low_money', 'high_food', 'low_energy', 'high_health'): {'work': 292.4363260932143, 'rest': 284.4578109529598, 'buy_food': 229.71104430067214}, ('low_money', 'medium_food', 'low_energy', 'high_health'): {'work': 257.81370012813665, 'rest': 238.88145713572592, 'buy_food': 213.6976852209794}, ('medium_money', 'high_food', 'low_energy', 'low_health'): {'work': 276.59538771815323, 'rest': 307.8544073818406, 'buy_food': 281.52309887425884}, ('low_money', 'high_food', 'medium_energy', 'low_health'): {'work': 277.88119372881386, 'rest': 279.5327008619427, 'buy_food': 223.56740604034047}, ('medium_money', 'high_food', 'medium_energy', 'high_health'): {'work': 311.98922796699514, 'rest': 288.36293981737884, 'buy_food': 275.59930620788543}, ('low_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 253.3603689824097, 'rest': 197.82567469082255, 'buy_food': 190.75522073988375}, ('medium_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 242.2642701012672, 'rest': 224.86172787987377, 'buy_food': 234.5740516135685}, ('low_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 203.28999592217664, 'rest': 169.45239458674, 'buy_food': 156.99181680562288}, ('low_money', 'medium_food', 'low_energy', 'low_health'): {'work': 208.1602183944525, 'rest': 240.88482133241186, 'buy_food': 200.90069779126586}, ('low_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 280.0218681462405, 'rest': 215.21200452997863, 'buy_food': 223.48425237394068}, ('low_money', 'low_food', 'low_energy', 'high_health'): {'work': 213.2930756886741, 'rest': 180.58880041018966, 'buy_food': 127.23651837703189}, ('medium_money', 'low_food', 'low_energy', 'high_health'): {'work': 228.43644941466087, 'rest': 223.0047557435375, 'buy_food': 239.267395948064}, ('medium_money', 'low_food', 'low_energy', 'low_health'): {'work': 144.95350022195439, 'rest': 200.0323369849641, 'buy_food': 178.1535483704323}, ('low_money', 'high_food', 'medium_energy', 'high_health'): {'work': 329.4584545823058, 'rest': 295.8644191141437, 'buy_food': 244.76052301927115}, ('medium_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 281.80953968128256, 'rest': 246.32965717525178, 'buy_food': 271.5799343423488}, ('medium_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 264.6336931863124, 'rest': 266.402170937393, 'buy_food': 259.59221788462764}, ('medium_money', 'high_food', 'low_energy', 'high_health'): {'work': 277.6941067883869, 'rest': 285.6718760988933, 'buy_food': 253.98421682302444}, ('medium_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 278.8030439468347, 'rest': 242.41730378134014, 'buy_food': 269.65797260327014}, ('medium_money', 'low_food', 'high_energy', 'medium_health'): {'work': 183.02854660060223, 'rest': 122.43137599310673, 'buy_food': 178.35164056389004}, ('low_money', 'high_food', 'high_energy', 'medium_health'): {'work': 314.27788982744005, 'rest': 272.1843172011966, 'buy_food': 239.6346636974499}, ('low_money', 'low_food', 'high_energy', 'low_health'): {'work': -1.5289897844194427, 'rest': -50.700965072745944, 'buy_food': -32.46323015927672}, ('low_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 235.1749675871444, 'rest': 136.09927115421783, 'buy_food': 199.59948869330117}, ('low_money', 'low_food', 'high_energy', 'high_health'): {'work': 231.01187805404106, 'rest': 158.463596987607, 'buy_food': 187.3694079119874}, ('medium_money', 'low_food', 'low_energy', 'medium_health'): {'work': 217.85713980611715, 'rest': 222.89370718385018, 'buy_food': 250.63563432841116}, ('low_money', 'high_food', 'high_energy', 'high_health'): {'work': 361.6676667430258, 'rest': 293.5471296538001, 'buy_food': 271.3762395400871}, ('medium_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 291.7627777202934, 'rest': 272.4552105310899, 'buy_food': 267.63626617488353}, ('medium_money', 'medium_food', 'low_energy', 'low_health'): {'work': 246.33941400976508, 'rest': 285.5851943685053, 'buy_food': 262.34288180958254}, ('medium_money', 'high_food', 'high_energy', 'high_health'): {'work': 336.59009524923135, 'rest': 291.08235455712577, 'buy_food': 299.4263192044433}, ('medium_money', 'low_food', 'high_energy', 'high_health'): {'work': 249.02175758302565, 'rest': 192.87546183248352, 'buy_food': 253.45554677951517}, ('medium_money', 'medium_food', 'high_energy', 'low_health'): {'work': 208.55986314789126, 'rest': 198.7324825726503, 'buy_food': 193.34187646653046}, ('medium_money', 'high_food', 'low_energy', 'medium_health'): {'work': 273.452550194208, 'rest': 278.66597547008996, 'buy_food': 262.81966316970033}, ('medium_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 252.1333139841633, 'rest': 201.2793556904169, 'buy_food': 260.0431842401315}, ('low_money', 'low_food', 'medium_energy', 'high_health'): {'work': 251.35275090581246, 'rest': 190.24345555356336, 'buy_food': 205.85768324206754}, ('medium_money', 'low_food', 'medium_energy', 'high_health'): {'work': 268.3063160514699, 'rest': 212.91795489818838, 'buy_food': 278.4433750615648}, ('low_money', 'low_food', 'low_energy', 'low_health'): {'work': 54.88273357824711, 'rest': 119.90570811192654, 'buy_food': 59.29998094389106}, ('medium_money', 'medium_food', 'low_energy', 'high_health'): {'work': 256.9192064360227, 'rest': 247.13322185131196, 'buy_food': 242.91834643459174}, ('low_money', 'medium_food', 'high_energy', 'high_health'): {'work': 310.4796070858973, 'rest': 219.84412054470963, 'buy_food': 238.4279273033186}, ('medium_money', 'medium_food', 'high_energy', 'high_health'): {'work': 301.038809570956, 'rest': 242.82932663148995, 'buy_food': 294.60254589444173}, ('low_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 290.410786374933, 'rest': 239.8368147424065, 'buy_food': 228.273310483249}, ('low_money', 'high_food', 'high_energy', 'low_health'): {'work': 262.3460478811811, 'rest': 252.8140865211596, 'buy_food': 200.39909577603166}, ('medium_money', 'low_food', 'high_energy', 'low_health'): {'work': 36.9605327648496, 'rest': 65.99367206520697, 'buy_food': 79.76589466311141}, ('low_money', 'medium_food', 'high_energy', 'low_health'): {'work': 179.2895040219498, 'rest': 135.3490903308606, 'buy_food': 132.1447378533082}, ('low_money', 'high_food', 'low_energy', 'medium_health'): {'work': 278.2483998887918, 'rest': 282.30346952173227, 'buy_food': 234.19454196346535}, ('medium_money', 'high_food', 'high_energy', 'medium_health'): {'work': 298.89727055188933, 'rest': 263.6034338877648, 'buy_food': 269.3060910336563}, ('medium_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 269.08347472666935, 'rest': 224.88453259464563, 'buy_food': 253.40593724495426}, ('low_money', 'low_food', 'low_energy', 'medium_health'): {'work': 200.93704638407314, 'rest': 164.46101292737197, 'buy_food': 192.51238744023158}, ('low_money', 'high_food', 'low_energy', 'low_health'): {'work': 270.92686346771615, 'rest': 297.3571093725517, 'buy_food': 245.8775072675115}, ('medium_money', 'low_food', 'medium_energy', 'low_health'): {'work': 147.05180310480088, 'rest': 145.27440781708347, 'buy_food': 133.2828547818678}, ('high_money', 'medium_food', 'medium_energy', 'low_health'): {'work': 259.02363160451165, 'rest': 279.2132286641357, 'buy_food': 279.165082135519}, ('high_money', 'medium_food', 'low_energy', 'low_health'): {'work': 270.36742643172096, 'rest': 305.3449087587043, 'buy_food': 313.4872570348934}, ('high_money', 'medium_food', 'medium_energy', 'high_health'): {'work': 278.1992258000325, 'rest': 260.97037723086873, 'buy_food': 273.28805579542876}, ('high_money', 'medium_food', 'high_energy', 'medium_health'): {'work': 275.56526447449403, 'rest': 248.6622841284026, 'buy_food': 264.0918525542795}, ('high_money', 'medium_food', 'high_energy', 'low_health'): {'work': 250.90163682805684, 'rest': 271.73075898584, 'buy_food': 267.827369012774}, ('high_money', 'medium_food', 'medium_energy', 'medium_health'): {'work': 276.47932886068037, 'rest': 258.55987613022205, 'buy_food': 272.29673709748835}, ('high_money', 'medium_food', 'low_energy', 'high_health'): {'work': 256.8860784275956, 'rest': 266.1745351182446, 'buy_food': 264.1622651403304}, ('high_money', 'medium_food', 'low_energy', 'medium_health'): {'work': 259.53999573493644, 'rest': 274.6612606211645, 'buy_food': 278.4775350825471}, ('high_money', 'high_food', 'medium_energy', 'medium_health'): {'work': 300.60778845127186, 'rest': 285.62999436511024, 'buy_food': 270.5776793737051}, ('high_money', 'high_food', 'medium_energy', 'high_health'): {'work': 302.5190053470123, 'rest': 277.20675196791996, 'buy_food': 258.3887844118397}, ('high_money', 'low_food', 'low_energy', 'high_health'): {'work': 258.7289537655522, 'rest': 245.52797777129243, 'buy_food': 288.4578356538295}, ('high_money', 'high_food', 'low_energy', 'medium_health'): {'work': 285.77228170674283, 'rest': 299.7098707058454, 'buy_food': 286.2170004275062}, ('high_money', 'high_food', 'high_energy', 'low_health'): {'work': 277.8115190022277, 'rest': 293.6743592311554, 'buy_food': 253.9479902471117}, ('high_money', 'high_food', 'high_energy', 'high_health'): {'work': 323.9442472302397, 'rest': 282.4850767697414, 'buy_food': 272.88906820572527}, ('high_money', 'low_food', 'low_energy', 'low_health'): {'work': 208.33745675257381, 'rest': 259.6765510196289, 'buy_food': 281.3479385745631}, ('high_money', 'medium_food', 'high_energy', 'high_health'): {'work': 302.48698404630716, 'rest': 261.20627911481176, 'buy_food': 288.1750106000345}, ('high_money', 'high_food', 'high_energy', 'medium_health'): {'work': 295.04928100732786, 'rest': 278.16435009734886, 'buy_food': 258.2665937708092}, ('high_money', 'low_food', 'low_energy', 'medium_health'): {'work': 263.84189084371815, 'rest': 260.1712858959725, 'buy_food': 311.1170716508163}, ('high_money', 'low_food', 'medium_energy', 'medium_health'): {'work': 260.66706521229935, 'rest': 237.84389525310684, 'buy_food': 280.4000424231516}, ('high_money', 'low_food', 'medium_energy', 'low_health'): {'work': 216.30989161889423, 'rest': 214.54497117436495, 'buy_food': 266.6291097246251}, ('high_money', 'low_food', 'medium_energy', 'high_health'): {'work': 268.5532182553742, 'rest': 230.44930253882495, 'buy_food': 274.61830788472054}, ('high_money', 'low_food', 'high_energy', 'high_health'): {'work': 279.1824209563582, 'rest': 225.5106406220899, 'buy_food': 289.18269971548165}, ('high_money', 'high_food', 'medium_energy', 'low_health'): {'work': 286.04941542935524, 'rest': 299.8910817594042, 'buy_food': 279.78874710234464}, ('high_money', 'low_food', 'high_energy', 'medium_health'): {'work': 248.61493317751336, 'rest': 208.99704838829072, 'buy_food': 270.8766178274715}, ('high_money', 'high_food', 'low_energy', 'low_health'): {'work': 283.151391834493, 'rest': 316.53503292957, 'buy_food': 307.30977520582}, ('high_money', 'low_food', 'high_energy', 'low_health'): {'work': 147.33178173251432, 'rest': 147.42051937393074, 'buy_food': 211.05035379572027}, ('high_money', 'high_food', 'low_energy', 'high_health'): {'work': 278.9467859981294, 'rest': 287.04373460827804, 'buy_food': 263.8318603514237}}


for i in range(500):
    agent["agent_name"].append(names.get_full_name())
    agent["money"].append(random.randint(5, 25))
    agent["food"].append(random.randint(0, 10))
    agent["energy"].append(random.randint(0, 100))
    agent["health"].append(random.randint(0, 10))
    agent["alive"].append(True)
    agent["living_strategy"].append(random.choice(livingStrategies))
    agent["agentsInteracted"].append({})
    agent["alliesList"].append([])

    livingAgentsIndex.append(i)

    if agent["living_strategy"][i] == "risk-taker":
        initialriskTakerCount += 1
    elif agent["living_strategy"][i] == "worker":
        initialWorkerCount += 1
    elif agent["living_strategy"][i] == "survivalist":
        initialSurvivalistCount += 1
    else:
        initialAdaptiveCount += 1
'''
print(f'Initial risk-taker count: {initialriskTakerCount}')
print(f'Initial worker count: {initialWorkerCount}')
print(f'Initial survivalist count: {initialSurvivalistCount}')
print(f'Initial adaptive count: {initialAdaptiveCount}')
print(livingAgentsIndex)
'''
'''
for i in range(500):
    print(f'Initial state of the agent {i+1} ({agent["agent_name"][i]}):')
    print(f'Money: {agent["money"][i]}')
    print(f'Food: {agent["food"][i]}')
    print(f'Energy: {agent["energy"][i]}')
    print(f'Health: {agent["health"][i]}')
    print(f'Alive: {agent["alive"][i]}')
    print(f'Living Strategy: {agent["living_strategy"][i]}')
    print('-------------------')
'''
def AgentStateVector(agentNumber):

    return np.array([
        agent["money"][agentNumber],
        agent["food"][agentNumber],
        agent["energy"][agentNumber],
        agent["health"][agentNumber],
    ])

ACTIONS = ["rest", "work", "buy_food", "ally"]
state_size = 4
action_size = len(ACTIONS)

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_size, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, action_size)
        )

    def forward(self, x):
        return self.network(x)

model = DQN()
target_model = DQN()
target_model.load_state_dict(model.state_dict())
target_model.eval()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()
replay_buffer = deque(maxlen=10000)
batch_size = 64
gamma = 0.9
training_steps = 0
target_update_frequency = 500

state = AgentStateVector(0)
state_tensor = torch.FloatTensor(state)

q_values = model(state_tensor)
action_index = torch.argmax(q_values).item()
ACTIONS[action_index]


def evaluate_agent_state(agentNumber):
    moneyState = ""
    energyState = ""
    foodState = ""
    healthState = ""

    if agent["money"][agentNumber] < 15:
                moneyState = "low_money"

    elif agent["money"][agentNumber] < 30:
         moneyState = "medium_money"

    else:
        moneyState = "high_money"

    if agent["energy"][agentNumber] < 30:
        energyState = "low_energy"
    elif agent["energy"][agentNumber] < 70:
        energyState = "medium_energy"

    else:
        energyState = "high_energy"
    if agent["food"][agentNumber] < 3:
        foodState = "low_food"

    elif agent["food"][agentNumber] < 7:
        foodState = "medium_food"

    else:
        foodState = "high_food"

    if agent["health"][agentNumber] < 3:
        healthState = "low_health"

    elif agent["health"][agentNumber] < 7:
        healthState = "medium_health"

    else:
        healthState = "high_health"

    return moneyState, foodState, energyState, healthState


def surviveOneDay(dayNumber: int = 1, agentNumber: int = 0):

    global foodAvailability

    moneyState, foodState, energyState, healthState = evaluate_agent_state(agentNumber)
    reward = 0
    
    if agent["living_strategy"][agentNumber] == "worker": #WORKER INSTRUCTIONS
        if (agent["energy"][agentNumber] < 15 or agent["health"][agentNumber] < 1) and agent["food"][agentNumber] >= 1: #RESTING
            agent["food"][agentNumber] = agent["food"][agentNumber] - 1
            agent["energy"][agentNumber] = min(agent["energy"][agentNumber] + 20, 100)
            agent["health"][agentNumber] = min(agent["health"][agentNumber] + 1, 10)

        elif agent["health"][agentNumber] > 2 and agent["energy"][agentNumber] > 20 and agent["food"][agentNumber] >= 1: #WORKING
            agent["money"][agentNumber] = agent["money"][agentNumber] + 10
            agent["food"][agentNumber] = agent["food"][agentNumber] - 1
            agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10
            agent["health"][agentNumber] = agent["health"][agentNumber] - 0.5

        elif agent["food"][agentNumber] <= 1:

            if agent["money"][agentNumber] >=20: #BUYING FOOD
                agent["money"][agentNumber] = agent["money"][agentNumber] - 10
                agent["food"][agentNumber] = agent["food"][agentNumber] + 5
                agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10

            else:
                if agent["health"][agentNumber] > 1:
                    agent["health"][agentNumber] = agent["health"][agentNumber] - 1
                else:
                    agent["alive"][agentNumber] = False
                    livingAgentsIndex.remove(agentNumber)
        
    if agent["living_strategy"][agentNumber] == "risk-taker": #RISK-TAKER INSTRUCTIONS
            if (agent["energy"][agentNumber] < 5 or agent["health"][agentNumber] < 0.5) and agent["food"][agentNumber] >= 1: #RESTING
                agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                agent["energy"][agentNumber] = min(agent["energy"][agentNumber] + 20, 100)
                agent["health"][agentNumber] = min(agent["health"][agentNumber] + 1, 10)

            elif agent["health"][agentNumber] > 0.5 and agent["energy"][agentNumber] > 10 and agent["food"][agentNumber] >= 1: #WORKING
                agent["money"][agentNumber] = agent["money"][agentNumber] + 10
                agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10
                agent["health"][agentNumber] = agent["health"][agentNumber] - 0.5

            elif agent["food"][agentNumber] <= 0:

                if agent["money"][agentNumber] >=20: #BUYING FOOD
                    agent["money"][agentNumber] = agent["money"][agentNumber] - 10
                    agent["food"][agentNumber] = agent["food"][agentNumber] + 5
                    agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10

                else:
                    if agent["health"][agentNumber] > 1:
                        agent["health"][agentNumber] = agent["health"][agentNumber] - 1
                    else:
                        agent["alive"][agentNumber] = False
                        livingAgentsIndex.remove(agentNumber)

    if agent["living_strategy"][agentNumber] == "survivalist": #SURVIVALIST INSTRUCTIONS
            if (agent["energy"][agentNumber] < 50 or agent["health"][agentNumber] < 5) and agent["food"][agentNumber] >= 1: #RESTING
                agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                agent["energy"][agentNumber] = min(agent["energy"][agentNumber] + 20, 100)
                agent["health"][agentNumber] = min(agent["health"][agentNumber] + 1, 10)

            elif agent["health"][agentNumber] > 2 and agent["energy"][agentNumber] > 60 and agent["food"][agentNumber] >= 2: #WORKING
                agent["money"][agentNumber] = agent["money"][agentNumber] + 10
                agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10
                agent["health"][agentNumber] = agent["health"][agentNumber] - 0.5

            elif agent["food"][agentNumber] <= 4:

                if agent["money"][agentNumber] >=20: #BUYING FOOD
                    agent["money"][agentNumber] = agent["money"][agentNumber] - 10
                    agent["food"][agentNumber] = agent["food"][agentNumber] + 5
                    agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10

                else:
                    if agent["health"][agentNumber] > 1:
                        agent["health"][agentNumber] = agent["health"][agentNumber] - 1
                    else:
                        agent["alive"][agentNumber] = False
                        livingAgentsIndex.remove(agentNumber)
    
    if agent["living_strategy"][agentNumber] == "adaptive": #ADAPTIVE INSTRUCTIONS\


            agentoldState = AgentStateVector(agentNumber)
            state_tensor = torch.FloatTensor(agentoldState)

            q_values = model(state_tensor)

            epsilon = 0.1

            if random.random() < epsilon:
                action_index = random.randint(0, len(ACTIONS) - 1)
            else:
                action_index = torch.argmax(q_values).item()

            randomChoice = ACTIONS[action_index]

            if randomChoice == "rest":

                if agent["food"][agentNumber] >= 1: #RESTING
                    agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                    agent["energy"][agentNumber] = min(agent["energy"][agentNumber] + 20, 100)
                    agent["health"][agentNumber] = min(agent["health"][agentNumber] + 1, 10)

                    if moneyState == "low_money":

                        reward = reward - 5

                    elif moneyState == "medium_money":
                        reward = reward + 5

                    else:
                        moneyState = "high_money"
                        reward = reward + 10

                    
                    if energyState == "low_energy":
                        reward = reward + 20

                    elif energyState == "medium_energy":
                        reward = reward + 5

                    else:
                        energyState = "high_energy"
                        reward = reward - 5


                    if foodState == "low_food":
                        reward = reward - 10

                    elif foodState == "medium_food":
                        reward = reward + 5

                    else:
                        foodState = "high_food"
                        reward = reward + 5
                    
                    if healthState == "low_health":
                        reward = reward + 20
                        
                    elif healthState == "medium_health":
                        reward = reward - 10

                    else:
                        healthState = "high_health"
                        reward = reward - 20

                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()


                else:
                   

                    if agent["health"][agentNumber] <= 0:
                        agent["health"][agentNumber] = 0
                        agent["alive"][agentNumber] = False
                        reward -= 100

                        if agentNumber in livingAgentsIndex:
                            livingAgentsIndex.remove(agentNumber)

                    if agent["food"][agentNumber] <= 0:
                        agent["food"][agentNumber] = 0
                        agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                        reward -= 20
                    
                    if moneyState == "low_money":

                        reward = reward - 5

                    elif moneyState == "medium_money":
                        reward = reward + 5

                    else:
                        moneyState = "high_money"
                        reward = reward + 10

                    
                    if energyState == "low_energy":
                        reward = reward + 20

                    elif energyState == "medium_energy":
                        reward = reward + 5

                    else:
                        energyState = "high_energy"
                        reward = reward - 5


                    if foodState == "low_food":
                        reward = reward - 10

                    elif foodState == "medium_food":
                        reward = reward + 5

                    else:
                        foodState = "high_food"
                        reward = reward + 5
                    
                    if healthState == "low_health":
                        reward = reward + 20
                        
                    elif healthState == "medium_health":
                        reward = reward - 10

                    else:
                        healthState = "high_health"
                        reward = reward - 20

                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()

                            

            elif randomChoice == "work":
                

                if agent["health"][agentNumber] > 0.5 and agent["energy"][agentNumber] > 10 and agent["food"][agentNumber] >= 1:
                    agent["money"][agentNumber] = agent["money"][agentNumber] + 10
                    agent["food"][agentNumber] = agent["food"][agentNumber] - 1
                    agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10
                    agent["health"][agentNumber] = agent["health"][agentNumber] - 0.5

                    if moneyState == "low_money":

                        reward = reward + 20

                    elif moneyState == "medium_money":
                        reward = reward + 10

                    else:
                        moneyState = "high_money"
                        reward = reward + 5

                    
                    if energyState == "low_energy":
                        reward = reward - 10

                    elif energyState == "medium_energy":
                        reward = reward + 5

                    else:
                        energyState = "high_energy"
                        reward = reward + 10

                    if foodState == "low_food":
                        reward = reward - 5

                    elif foodState == "medium_food":
                        reward = reward + 5

                    else:
                        foodState = "high_food"
                        reward = reward + 10
                    
                    if healthState == "low_health":
                        reward = reward - 10
                        
                    elif healthState == "medium_health":
                        reward = reward + 10

                    else:
                        healthState = "high_health"
                        reward = reward + 15
                    
                    next_state = AgentStateVector(agentNumber)
                    done = not agent["alive"][agentNumber]

                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()


                else:

                    if agent["health"][agentNumber] <= 0:
                        agent["health"][agentNumber] = 0
                        agent["alive"][agentNumber] = False
                        reward -= 100

                        if agentNumber in livingAgentsIndex:
                            livingAgentsIndex.remove(agentNumber)

                    
                    if agent["food"][agentNumber] <= 0:
                        agent["food"][agentNumber] = 0
                        agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                        reward -= 20

                    if moneyState == "low_money":

                        reward = reward + 20

                    elif moneyState == "medium_money":
                        reward = reward + 10

                    else:
                        moneyState = "high_money"
                        reward = reward + 5

                    
                    if energyState == "low_energy":
                        reward = reward - 10

                    elif energyState == "medium_energy":
                        reward = reward + 5

                    else:
                        energyState = "high_energy"
                        reward = reward + 10


                    if foodState == "low_food":
                        reward = reward - 5

                    elif foodState == "medium_food":
                        reward = reward + 5

                    else:
                        foodState = "high_food"
                        reward = reward + 10
                    
                    if healthState == "low_health":
                        reward = reward - 10
                        
                    elif healthState == "medium_health":
                        reward = reward + 10

                    else:
                        healthState = "high_health"
                        reward = reward + 15

                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()

            
            elif randomChoice == "ally":

                if agent["money"][agentNumber] > 7 and agent["health"][agentNumber] >= 0.5 and agent["energy"][agentNumber] > 20 and len(agent["agentsInteracted"][agentNumber]) > 0:
                    trusted_agents = sorted(
                                            agent["agentsInteracted"][agentNumber],
                                            key=lambda x: agent["agentsInteracted"][agentNumber][x],
                                            reverse=True
                                        )
                    
                    agent["money"][agentNumber] = agent["money"][agentNumber] - 7
                    agent["energy"][agentNumber] = agent["energy"][agentNumber] - 20
                    agent["health"][agentNumber] = agent["health"][agentNumber] - 0.5

                    for i in trusted_agents:
                        if i != agentNumber and agent["alive"][i] == True and i not in agent["alliesList"][agentNumber] and agent["agentsInteracted"][i][agentNumber] > 3 and agent["agentsInteracted"][agentNumber][i] > 3:
                                agent["money"][agentNumber] = agent["money"][agentNumber] - 7
                                agent["money"][agentNumber] 
                                agent["alliesList"][agentNumber].append(i)
                                agent["alliesList"][i].append(agentNumber)

                                break
                        elif i == trusted_agents[-1]:
                            if agent["health"][agentNumber] <= 0:
                                agent["health"][agentNumber] = 0
                                agent["alive"][agentNumber] = False
                                reward -= 100

                                if agentNumber in livingAgentsIndex:
                                    livingAgentsIndex.remove(agentNumber)

                            
                            if agent["food"][agentNumber] <= 0:
                                agent["food"][agentNumber] = 0
                                agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                                reward -= 20
                        else:
                            continue

                    if moneyState == "low_money":

                        reward = reward - 10

                    elif moneyState == "medium_money":
                        reward = reward + 5

                    else:
                        moneyState = "high_money"
                        reward = reward + 10

                    if energyState == "low_energy":
                        reward = reward - 15

                    elif energyState == "medium_energy":
                        reward = reward + 5

                    else:
                        energyState = "high_energy"
                        reward = reward + 15


                    if foodState == "low_food":
                        reward = reward - 5

                    elif foodState == "medium_food":
                        reward = reward + 5

                    else:
                        foodState = "high_food"
                        reward = reward + 10
                    
                    if healthState == "low_health":
                        reward = reward - 10
                        
                    elif healthState == "medium_health":
                        reward = reward + 10

                    else:
                        healthState = "high_health"
                        reward = reward + 15
                    
                    if len(agent["alliesList"][agentNumber]) > 7 and len(agent["agentsInteracted"][agentNumber]) > 15:
                        reward = reward + 20
                    
                    elif len(agent["alliesList"][agentNumber]) > 5 and len(agent["agentsInteracted"][agentNumber]) > 10:
                        reward = reward + 5
                    
                    else:
                        reward = reward - 5


                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()

                else:    
                    if agent["health"][agentNumber] <= 0:
                        agent["health"][agentNumber] = 0
                        agent["alive"][agentNumber] = False
                        reward -= 100

                        if agentNumber in livingAgentsIndex:
                            livingAgentsIndex.remove(agentNumber)

                    
                    if agent["food"][agentNumber] <= 0:
                        agent["food"][agentNumber] = 0
                        agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                        reward -= 20
                    
                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()
                    

            elif randomChoice == "buy_food":
                
                if agent["money"][agentNumber] >=10 and agent["energy"][agentNumber] > 10: #BUYING FOOD

                    if foodAvailability >= 5:
                        agent["money"][agentNumber] = agent["money"][agentNumber] - 10
                        agent["food"][agentNumber] = agent["food"][agentNumber] + 5
                        foodAvailability = foodAvailability - 5
                        agent["energy"][agentNumber] = agent["energy"][agentNumber] - 10
                    
                    else:
                        tradeDone = False

                        if agent["money"][agentNumber] >= 15 and agent["energy"][agentNumber] > 10:

                            trusted_agents = sorted(
                                                    agent["agentsInteracted"][agentNumber],
                                                    key=lambda x: agent["agentsInteracted"][agentNumber][x],
                                                    reverse=True
                                                )

                            for i in trusted_agents:
                                global numTrades
                                global numKnownTrades
                                

                                if len(agent["agentsInteracted"][agentNumber]) > 0:

                                    if i != agentNumber and agent["food"][i] >= 6 and agent["alive"][i] == True:
                                        agent["money"][agentNumber] = agent["money"][agentNumber] - 15
                                        agent["food"][agentNumber] = agent["food"][agentNumber] + 2
                                        agent["money"][i] = agent["money"][i] + 15
                                        agent["food"][i] = agent["food"][i] - 2
                                        numTrades += 1
                                        agent["agentsInteracted"][agentNumber][i] += 1
                                        agent["agentsInteracted"][i][agentNumber] += 0.2
                                        tradeDone = True
                                        numKnownTrades += 1
                                        break

                                    elif i == trusted_agents[-1]:
                                        if agent["health"][agentNumber] <= 0:
                                            agent["health"][agentNumber] = 0
                                            agent["alive"][agentNumber] = False
                                            reward -= 100

                                            if agentNumber in livingAgentsIndex:
                                                livingAgentsIndex.remove(agentNumber)

                                        
                                        if agent["food"][agentNumber] <= 0:
                                            agent["food"][agentNumber] = 0
                                            agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                                            reward -= 20

                                    else:
                                        agent["agentsInteracted"][agentNumber][i] -= 0.2
                                        continue

                                
                                else:
                                    break
                            
                            if tradeDone == False:
                                for i in livingAgentsIndex:
                                    if i != agentNumber and agent["food"][i] >= 6 and agent["alive"][i] == True:
                                        agent["money"][agentNumber] = agent["money"][agentNumber] - 15
                                        agent["food"][agentNumber] = agent["food"][agentNumber] + 2
                                        agent["money"][i] = agent["money"][i] + 15
                                        agent["food"][i] = agent["food"][i] - 2
                                        numTrades += 1
                                        agent["agentsInteracted"][agentNumber][i] = agent["agentsInteracted"][agentNumber].get(i, 0) + 0.2
                                        agent["agentsInteracted"][i][agentNumber] = agent["agentsInteracted"][i].get(agentNumber, 0) + 0.2
                                        tradeDone = True
                                        break

                                    elif i == livingAgentsIndex[-1]:
                                        if agent["health"][agentNumber] <= 0:
                                            agent["health"][agentNumber] = 0
                                            agent["alive"][agentNumber] = False
                                            reward -= 100

                                            if agentNumber in livingAgentsIndex:
                                                livingAgentsIndex.remove(agentNumber)

                                        
                                        if agent["food"][agentNumber] <= 0:
                                            agent["food"][agentNumber] = 0
                                            agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                                            reward -= 20

                                    else:
                                        continue
                                                        
                    if moneyState == "low_money":

                        reward = reward - 20

                    elif moneyState == "medium_money":
                        reward = reward + 10

                    else:
                        moneyState = "high_money"
                        reward = reward + 15

                    
                    if energyState == "low_energy":
                        reward = reward + 10

                    elif energyState == "medium_energy":
                        reward = reward - 5

                    else:
                        energyState = "high_energy"
                        reward = reward - 10


                    if foodState == "low_food":
                        reward = reward + 15

                    elif foodState == "medium_food":
                        reward = reward - 5

                    else:
                        foodState = "high_food"
                        reward = reward - 15
                    
                    if healthState == "low_health":
                        reward = reward + 10
                        
                    elif healthState == "medium_health":
                        reward = reward + 5

                    else:
                        healthState = "high_health"
                        reward = reward - 5

                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()

                else:
                    if agent["health"][agentNumber] <= 0:
                        agent["health"][agentNumber] = 0
                        agent["alive"][agentNumber] = False
                        reward -= 100

                        if agentNumber in livingAgentsIndex:
                            livingAgentsIndex.remove(agentNumber)

                    
                    if agent["food"][agentNumber] <= 0:
                        agent["food"][agentNumber] = 0
                        agent["health"][agentNumber] = max(agent["health"][agentNumber] - 1, 0)
                        reward -= 20


                    if moneyState == "low_money":

                        reward = reward - 20

                    elif moneyState == "medium_money":
                        reward = reward + 10

                    else:
                        moneyState = "high_money"
                        reward = reward + 15

                    
                    if energyState == "low_energy":
                        reward = reward + 10

                    elif energyState == "medium_energy":
                        reward = reward - 5

                    else:
                        energyState = "high_energy"
                        reward = reward - 10


                    if foodState == "low_food":
                        reward = reward + 15

                    elif foodState == "medium_food":
                        reward = reward - 5

                    else:
                        foodState = "high_food"
                        reward = reward - 15
                    
                    if healthState == "low_health":
                        reward = reward + 10
                        
                    elif healthState == "medium_health":
                        reward = reward + 5

                    else:
                        healthState = "high_health"
                        reward = reward - 5

                    next_state = AgentStateVector(agentNumber)
                    next_state_tensor = torch.FloatTensor(next_state)
                    done = not agent["alive"][agentNumber]


                    replay_buffer.append((
                        agentoldState,
                        action_index,
                        reward,
                        next_state,
                        done
                    ))

                    train_from_replay()

def train_from_replay():
    global training_steps

    if len(replay_buffer) < batch_size:
        return

    batch = random.sample(replay_buffer, batch_size)

    states = []
    actions = []
    rewards = []
    next_states = []
    dones = []


    for experience in batch:
        state, action, reward, next_state, done = experience

        states.append(state)
        actions.append(action)
        rewards.append(reward)
        next_states.append(next_state)
        dones.append(done)

    states_tensor = torch.FloatTensor(np.array(states))
    actions_tensor = torch.LongTensor(actions)
    rewards_tensor = torch.FloatTensor(rewards)
    next_states_tensor = torch.FloatTensor(np.array(next_states))
    dones_tensor = torch.FloatTensor(dones)
    q_values = model(states_tensor)

    predicted_q_values = q_values.gather(
        1,
        actions_tensor.unsqueeze(1)
    ).squeeze(1)

    with torch.no_grad():
        next_q_values = target_model(next_states_tensor)
        max_future_q_values = torch.max(next_q_values, dim=1)[0]

    targets = rewards_tensor + gamma * max_future_q_values * (1 - dones_tensor)

    loss = loss_fn(predicted_q_values, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    training_steps += 1

    if training_steps % target_update_frequency == 0:
        target_model.load_state_dict(model.state_dict())


'''EPISDOE RUN'''
            
for c in range(10):
    if c >= 1:
        agentAliveCount: list = []
        agentAvgMoney: list = []
        highestAgentMoney: list = []
        lowestAgentMoney: list = []
        livingAgentsIndex: list = []

        initialriskTakerCount = 0
        initialWorkerCount = 0
        initialSurvivalistCount = 0
        initialAdaptiveCount = 0
        riskTakerATP: list = []
        workerATP: list = []
        survivalistATP: list = []
        adaptiveATP: list = []
        agent["agent_name"] = []
        agent["money"] = []
        agent["food"] = []
        agent["energy"] = []
        agent["health"] = []
        agent["alive"] = []
        agent["living_strategy"] = []
        agent["agentsInteracted"] = []
        agent["alliesList"] = []

        for i in range(500):
            agent["agent_name"].append(names.get_full_name())
            agent["money"].append(random.randint(5, 25))
            agent["food"].append(random.randint(0, 10))
            agent["energy"].append(random.randint(0, 100))
            agent["health"].append(random.randint(0, 10))
            agent["alive"].append(True)
            agent["living_strategy"].append(random.choice(livingStrategies))
            agent["agentsInteracted"].append({})
            agent["alliesList"].append([])

            livingAgentsIndex.append(i)

            if agent["living_strategy"][i] == "risk-taker":
                initialriskTakerCount += 1
            elif agent["living_strategy"][i] == "worker":
                initialWorkerCount += 1
            elif agent["living_strategy"][i] == "survivalist":
                initialSurvivalistCount += 1
            else:
                initialAdaptiveCount += 1

        
    for i in range(1200):

        currentriskTakerCount = 0
        currentWorkerCount = 0
        currentSurvivalistCount = 0
        currentAdaptiveCount = 0

        for j in range(500):
            if agent["alive"][j]:

                surviveOneDay(dayNumber=i+1, agentNumber=j)

                if agent["living_strategy"][j] == "risk-taker":
                    currentriskTakerCount += 1
                
                elif agent["living_strategy"][j] == "survivalist":
                    currentSurvivalistCount += 1
                
                elif agent["living_strategy"][j] == "worker":
                    currentWorkerCount += 1
                else:
                    currentAdaptiveCount += 1

            else:
                continue
        
        workerATP.append(currentWorkerCount)
        riskTakerATP.append(currentriskTakerCount)
        survivalistATP.append(currentSurvivalistCount)
        adaptiveATP.append(currentAdaptiveCount)

        elementCount = len(agent["money"])
        aliveAgentCount = len(livingAgentsIndex)
        avgMoney = sum(agent["money"])/aliveAgentCount if aliveAgentCount > 0 else 1
        agentAvgMoney.append(avgMoney)
        aliveCount = sum(agent["alive"])
        agentAliveCount.append(aliveCount)
        days.append(i+1)
        highestAgentMoney.append(max(agent["money"]))
        lowestAgentMoney.append(min(agent["money"]))
        foodAvailabilityHistory.append(foodAvailability)
        foodAvailability += 200


    print(f'Highest money at the end of ep {c+1}: {max(agent["money"])}')
    print(f'Lowest money at the end of day {c+1}: {min(agent["money"])}')
    print(f'Average money at the end of day {c+1}: {avgMoney}')
    print(f'Number of alive agents at the end of day {c+1}: {aliveCount}')
    print(f'Wealth gap at the end of day {c+1}: {max(agent["money"]) - min(agent["money"])}')
    print(f'Top 3 wealth contribution at the end of the day {c+1}: {sum(sorted(agent["money"], reverse=True)[:3]) / sum(agent["money"]) * 100}%')
    print(f'Adaptive count at the end of day {c+1}: {currentAdaptiveCount}')
    print(f'Adaptive death count at the end of day {c+1}: {initialAdaptiveCount - currentAdaptiveCount}')


    print("-------------------")

    print(f'Number of trades until {i+1}: {numTrades}')
    print(f'Number of known trades until {i+1}: {numKnownTrades}')

    

'''
plt.figure(figsize=(12, 6))
plt.plot(days, agentAliveCount, label='Alive Agents', marker='o')
plt.plot(days, agentAvgMoney, label='Average Money', marker='o')
plt.title('Alive Agents and Average Money Over Time')
plt.xlabel('Days')
plt.ylabel('Count / Average Money')
plt.legend()
plt.grid()

plt.figure(figsize=(12, 6))
plt.plot(days, highestAgentMoney, label='Highest Money', marker='o')
plt.plot(days, lowestAgentMoney, label='Lowest Money', marker='o')
plt.title('Alive Agents Lowest and Highest Money Over Time')
plt.xlabel('Days')
plt.ylabel('Count / Average Money')
plt.legend()
plt.grid()

plt.figure(figsize=(12, 6))
plt.plot(days, workerATP, label='Worker Count', marker='o')
plt.plot(days, riskTakerATP, label='Risk-taker Count', marker='o')
plt.plot(days, survivalistATP, label='Survivalist Count', marker='o')
plt.plot(days, adaptiveATP, label='Adaptive Count', marker='o')
plt.title('Alive Agents by Living Strategy Over Time')
plt.xlabel('Days')
plt.ylabel('Count')
plt.legend()
plt.grid()

plt.figure(figsize=(12, 6))
plt.plot(days, foodAvailabilityHistory, label='Food Availability', marker='o')
plt.title('Food Availability Over Time')
plt.xlabel('Days')
plt.ylabel('Food Availability')
plt.legend()
plt.grid()

plt.show()

'''

def evaluate_agent_state(agentNumber):
    moneyState = ""
    energyState = ""
    foodState = ""
    healthState = ""

    if agent["money"][agentNumber] < 15:
                moneyState = "low_money"

    elif agent["money"][agentNumber] < 30:
         moneyState = "medium_money"

    else:
        moneyState = "high_money"
                    
    if agent["energy"][agentNumber] < 30:
        energyState = "low_energy"
    elif agent["energy"][agentNumber] < 70:
        energyState = "medium_energy"
 
    else:
        energyState = "high_energy"
    if agent["food"][agentNumber] < 3:
        foodState = "low_food"

    elif agent["food"][agentNumber] < 7:
        foodState = "medium_food"
            
    else:
        foodState = "high_food"

    if agent["health"][agentNumber] < 3:
        healthState = "low_health"
  
    elif agent["health"][agentNumber] < 7:
        healthState = "medium_health"
 
    else:
        healthState = "high_health"

    return moneyState, foodState, energyState, healthState