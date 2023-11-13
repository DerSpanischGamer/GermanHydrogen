import copy
import json
import numpy as np
import geopandas as gpd
from itertools import combinations

h2Need = {'DE111': 36672.66964327198,
 'DE112': 25563.439215157072,
 'DE113': 35059.0020723022,
 'DE114': 18329.37501590929,
 'DE115': 37255.56566156357,
 'DE116': 30244.140132852976,
 'DE117': 9191.433957780293,
 'DE118': 24338.90102045851,
 'DE119': 8030.137298369095,
 'DE11A': 14615.203696922223,
 'DE11B': 0.0,
 'DE11C': 10216.90730557495,
 'DE11D': 25319.818443786087,
 'DE121': 0.0,
 'DE122': 17794.698553653678,
 'DE123': 34397.183781883476,
 'DE124': 18645.643360088972,
 'DE125': 8538.246578513072,
 'DE126': 206785.48790875534,
 'DE127': 0.0,
 'DE128': 41482.68740141751,
 'DE129': 7607.951342300067,
 'DE12A': 0.0,
 'DE12B': 15186.547494713654,
 'DE12C': 0.0,
 'DE131': 0.0,
 'DE132': 21123.657253138586,
 'DE133': 12227.421180525655,
 'DE134': 337629.7695263752,
 'DE135': 10611.821254885434,
 'DE136': 15949.645512151645,
 'DE137': 9772.602764861002,
 'DE138': 21345.909738473332,
 'DE139': 18973.354197026434,
 'DE13A': 0.0,
 'DE141': 15800.093385751055,
 'DE142': 14681.908469376041,
 'DE143': 13156.577527346062,
 'DE144': 0.0,
 'DE145': 15186.941919282897,
 'DE146': 13460.860930557314,
 'DE147': 15961.375592749895,
 'DE148': 19544.798506038227,
 'DE149': 9316.864957769469,
 'DE211': 9715.434648975634,
 'DE212': 70518.48149830624,
 'DE213': 0.0,
 'DE214': 52324.75254284973,
 'DE215': 0.0,
 'DE216': 0.0,
 'DE217': 0.0,
 'DE218': 8745.721420473166,
 'DE219': 69830.34115497106,
 'DE21A': 8660.750297381455,
 'DE21B': 10425.366480678735,
 'DE21C': 0.0,
 'DE21D': 0.0,
 'DE21E': 0.0,
 'DE21F': 0.0,
 'DE21G': 7242.614196382986,
 'DE21H': 21668.94014734408,
 'DE21I': 0.0,
 'DE21J': 135177.086308692,
 'DE21K': 15743.291347897119,
 'DE21L': 0.0,
 'DE21M': 9455.602321421138,
 'DE21N': 7729.175450145118,
 'DE221': 0.0,
 'DE222': 0.0,
 'DE223': 0.0,
 'DE224': 7681.596312693751,
 'DE225': 0.0,
 'DE226': 8628.70909722071,
 'DE227': 9490.850708456777,
 'DE228': 14319.345446835714,
 'DE229': 0.0,
 'DE22A': 0.0,
 'DE22B': 5237.528712968358,
 'DE22C': 7560.737494854836,
 'DE231': 0.0,
 'DE232': 0.0,
 'DE233': 0.0,
 'DE234': 5494.929853666982,
 'DE235': 6362.761040600504,
 'DE236': 0.0,
 'DE237': 5562.3782252437795,
 'DE238': 12502.970593721937,
 'DE239': 10400.061615440074,
 'DE23A': 0.0,
 'DE241': 0.0,
 'DE242': 0.0,
 'DE243': 0.0,
 'DE244': 0.0,
 'DE245': 0.0,
 'DE246': 5777.407132796547,
 'DE247': 0.0,
 'DE248': 0.0,
 'DE249': 0.0,
 'DE24A': 0.0,
 'DE24B': 0.0,
 'DE24C': 0.0,
 'DE24D': 0.0,
 'DE251': 0.0,
 'DE252': 7499.554837888711,
 'DE253': 0.0,
 'DE254': 30651.674816994044,
 'DE255': 0.0,
 'DE256': 0.0,
 'DE257': 8770.813924125829,
 'DE258': 9531.882968631993,
 'DE259': 0.0,
 'DE25A': 5264.512193699981,
 'DE25B': 9303.764362225096,
 'DE25C': 0.0,
 'DE261': 5262.213298130601,
 'DE262': 0.0,
 'DE263': 9230.339853378697,
 'DE264': 0.0,
 'DE265': 0.0,
 'DE266': 0.0,
 'DE267': 5385.7105843251675,
 'DE268': 0.0,
 'DE269': 9723.638340604952,
 'DE26A': 0.0,
 'DE26B': 0.0,
 'DE26C': 11890.664294740856,
 'DE271': 16890.573631873634,
 'DE272': 0.0,
 'DE273': 0.0,
 'DE274': 0.0,
 'DE275': 8786.828571871754,
 'DE276': 181071.1543240011,
 'DE277': 6310.266969405338,
 'DE278': 8557.654513361256,
 'DE279': 11949.336464078235,
 'DE27A': 6403.801293088149,
 'DE27B': 9076.068409730036,
 'DE27C': 0.0,
 'DE27D': 0.0,
 'DE27E': 12571.850849098775,
 'DE300': 193802.04185796715,
 'DE401': 156623.10721888742,
 'DE402': 0.0,
 'DE403': 0.0,
 'DE404': 8190.369859601896,
 'DE405': 15140.5277905866,
 'DE406': 15625.130212005042,
 'DE407': 8621.348914673803,
 'DE408': 15148.156572839252,
 'DE409': 16935.831215253267,
 'DE40A': 169241.66756441913,
 'DE40B': 7030.117913227145,
 'DE40C': 271329.65043051966,
 'DE40D': 7967.7417756221585,
 'DE40E': 20414.407105479695,
 'DE40F': 6520.254308254024,
 'DE40G': 8914.11583844603,
 'DE40H': 15487.249049246428,
 'DE40I': 8565.486253663317,
 'DE501': 303527.06459276384,
 'DE502': 0.0,
 'DE600': 459792.75854854577,
 'DE711': 12334.387306172173,
 'DE712': 55059.457096772,
 'DE713': 0.0,
 'DE714': 23526.501025352078,
 'DE715': 23335.36823615313,
 'DE716': 28404.534739678144,
 'DE717': 23445.60386162466,
 'DE718': 0.0,
 'DE719': 38515.85441224147,
 'DE71A': 0.0,
 'DE71B': 8577.41290602284,
 'DE71C': 0.0,
 'DE71D': 0.0,
 'DE71E': 25420.49348493414,
 'DE721': 23177.35860216199,
 'DE722': 73644.2400250175,
 'DE723': 17851.285074001782,
 'DE724': 21906.881852242943,
 'DE725': 7062.85357069601,
 'DE731': 0.0,
 'DE732': 18378.71367609827,
 'DE733': 10717.418973856915,
 'DE734': 0.0,
 'DE735': 0.0,
 'DE736': 0.0,
 'DE737': 0.0,
 'DE803': 8195.654242033506,
 'DE804': 4066.840877702313,
 'DE80J': 16831.596194412683,
 'DE80K': 16656.96800543774,
 'DE80L': 16512.71460019007,
 'DE80M': 12739.2037073791,
 'DE80N': 17053.361599117405,
 'DE80O': 17975.513242784236,
 'DE911': 21741.607790072423,
 'DE912': 494063.6180585313,
 'DE913': 0.0,
 'DE914': 21048.807559258217,
 'DE916': 0.0,
 'DE917': 0.0,
 'DE918': 15569.627950026674,
 'DE91A': 501340.0844794388,
 'DE91B': 0.0,
 'DE91C': 33660.15321674343,
 'DE922': 26259.96692568598,
 'DE923': 17083.773550546688,
 'DE925': 31531.254753448233,
 'DE926': 0.0,
 'DE927': 14885.276827085572,
 'DE928': 18268.36065725681,
 'DE929': 120968.01909396201,
 'DE931': 21520.568329525337,
 'DE932': 62246.01378242182,
 'DE933': 29985.746387318777,
 'DE934': 6174.605095574519,
 'DE935': 19925.51861683911,
 'DE936': 13534.235107964007,
 'DE937': 20151.05565118691,
 'DE938': 16583.024924303598,
 'DE939': 23332.868379637777,
 'DE93A': 11478.154729801703,
 'DE93B': 16369.010217814077,
 'DE941': 0.0,
 'DE942': 5528.83883046715,
 'DE943': 18931.457697585764,
 'DE944': 15778.019882351393,
 'DE945': 0.0,
 'DE946': 15439.769254555587,
 'DE947': 23653.01120001504,
 'DE948': 19354.833585511533,
 'DE949': 190332.7219311415,
 'DE94A': 12366.992219184542,
 'DE94B': 16074.863393986667,
 'DE94C': 20686.65114822195,
 'DE94D': 15618.65917612242,
 'DE94E': 97424.53904270031,
 'DE94F': 16334.059978367053,
 'DE94G': 10529.434573317536,
 'DE94H': 7085.654137729651,
 'DEA11': 59045.166004820196,
 'DEA12': 2518865.1011021044,
 'DEA13': 43473.81797202266,
 'DEA14': 50814.72579251491,
 'DEA15': 27553.31026884666,
 'DEA16': 0.0,
 'DEA17': 15948.097719473142,
 'DEA18': 10728.942166363402,
 'DEA19': 14220.184100357921,
 'DEA1A': 28728.27458796363,
 'DEA1B': 32597.136336791023,
 'DEA1C': 45793.95399682095,
 'DEA1D': 43276.73403957051,
 'DEA1E': 30731.09301127164,
 'DEA1F': 37527.347914552454,
 'DEA22': 27007.01392711189,
 'DEA23': 332216.36249562626,
 'DEA24': 15294.212450272977,
 'DEA26': 27873.96441609333,
 'DEA27': 45655.63626885001,
 'DEA28': 21317.6620308693,
 'DEA29': 28795.66331098272,
 'DEA2A': 29561.475389822048,
 'DEA2B': 31942.206205199203,
 'DEA2C': 154656.41508970264,
 'DEA2D': 56271.36796750537,
 'DEA31': 0.0,
 'DEA32': 0.0,
 'DEA33': 25889.812128447345,
 'DEA34': 37920.30417781274,
 'DEA35': 22057.655899562727,
 'DEA36': 206322.97107438647,
 'DEA37': 45938.95587161087,
 'DEA38': 28343.16110074672,
 'DEA41': 30785.072703249978,
 'DEA42': 37381.11893619576,
 'DEA43': 27675.519550762285,
 'DEA44': 0.0,
 'DEA45': 36833.82935457688,
 'DEA46': 34504.77808653376,
 'DEA47': 32275.014075935745,
 'DEA51': 61649.79165975681,
 'DEA52': 56182.859269263914,
 'DEA53': 28792.452597260275,
 'DEA54': 16810.19090922011,
 'DEA55': 13546.088077590768,
 'DEA56': 60342.26461923973,
 'DEA57': 27103.385111897875,
 'DEA58': 38902.787006177605,
 'DEA59': 14582.914136160329,
 'DEA5A': 62505.196781373284,
 'DEA5B': 32349.65540082842,
 'DEA5C': 38747.150135508346,
 'DEB11': 0.0,
 'DEB12': 0.0,
 'DEB13': 11885.005390641978,
 'DEB14': 0.0,
 'DEB15': 5814.512646140778,
 'DEB16': 0.0,
 'DEB17': 0.0,
 'DEB18': 0.0,
 'DEB19': 0.0,
 'DEB1A': 11494.13880151422,
 'DEB1B': 0.0,
 'DEB21': 0.0,
 'DEB22': 5336.04584769831,
 'DEB23': 0.0,
 'DEB24': 4639.0802273194495,
 'DEB25': 7939.506944479267,
 'DEB31': 4834.2181610085545,
 'DEB32': 10079.959826048289,
 'DEB33': 0.0,
 'DEB34': 208090.58053957866,
 'DEB35': 19230.201477669834,
 'DEB36': 0.0,
 'DEB37': 0.0,
 'DEB38': 0.0,
 'DEB39': 8439.840135814395,
 'DEB3A': 0.0,
 'DEB3B': 13543.04498247666,
 'DEB3C': 0.0,
 'DEB3D': 6972.014902309848,
 'DEB3E': 13813.510523592264,
 'DEB3F': 14841.297916994654,
 'DEB3G': 6049.916634598068,
 'DEB3H': 12282.674151257881,
 'DEB3I': 200486.29995828774,
 'DEB3J': 0.0,
 'DEB3K': 8291.616496944122,
 'DEC01': 405033.7228079984,
 'DEC02': 10440.2472038993,
 'DEC03': 0.0,
 'DEC04': 385818.86480328767,
 'DEC05': 13299.52702193278,
 'DEC06': 0.0,
 'DED21': 30033.81255562614,
 'DED2C': 22470.547161443847,
 'DED2D': 19693.64339977779,
 'DED2E': 220802.09836037317,
 'DED2F': 26149.392034885,
 'DED41': 13860.513935392968,
 'DED42': 26322.81153754398,
 'DED43': 24513.659055493466,
 'DED44': 0.0,
 'DED45': 24453.603518437358,
 'DED51': 35312.050850287415,
 'DED52': 24356.092737486488,
 'DED53': 16318.746087530908,
 'DEE01': 4645.497389073011,
 'DEE02': 13390.065319667045,
 'DEE03': 15897.78510171312,
 'DEE04': 5561.640613325523,
 'DEE05': 11020.844888350646,
 'DEE06': 7548.683105129969,
 'DEE07': 14870.822580807344,
 'DEE08': 12327.067957658046,
 'DEE09': 0.0,
 'DEE0A': 10630.135556452055,
 'DEE0B': 162198.42564780824,
 'DEE0C': 14312.272379896856,
 'DEE0D': 7985.660206678465,
 'DEE0E': 588476.5388217336,
 'DEF01': 0.0,
 'DEF02': 0.0,
 'DEF03': 0.0,
 'DEF04': 0.0,
 'DEF05': 20974.61750567344,
 'DEF06': 17686.85794395271,
 'DEF07': 0.0,
 'DEF08': 20524.250926805573,
 'DEF09': 27702.249755571287,
 'DEF0A': 0.0,
 'DEF0B': 51548.09741916581,
 'DEF0C': 18215.284548162348,
 'DEF0D': 23639.81582693813,
 'DEF0E': 374380.9424014493,
 'DEF0F': 22109.688398939295,
 'DEG01': 14420.216608905128,
 'DEG02': 5804.823949362074,
 'DEG03': 6309.107098631875,
 'DEG04': 2045.0876042681791,
 'DEG05': 0.0,
 'DEG06': 0.0,
 'DEG07': 0.0,
 'DEG09': 9302.604510328807,
 'DEG0A': 6365.411552322828,
 'DEG0B': 0.0,
 'DEG0C': 0.0,
 'DEG0D': 3974.332277401486,
 'DEG0E': 0.0,
 'DEG0F': 8808.427563205145,
 'DEG0G': 7010.305704127619,
 'DEG0H': 0.0,
 'DEG0I': 8655.792331091261,
 'DEG0J': 6098.523707178742,
 'DEG0K': 0.0,
 'DEG0L': 8275.126469844674,
 'DEG0M': 6375.340509849104,
 'DEG0N': 3375.251954832132,
 'DEG0P': 9958.142498341933}
indexes = ['DE111', 'DE112', 'DE113', 'DE114', 'DE115', 'DE116', 'DE117',
       'DE118', 'DE119', 'DE11A', 'DE11B', 'DE11C', 'DE11D', 'DE121',
       'DE122', 'DE123', 'DE124', 'DE125', 'DE126', 'DE127', 'DE128',
       'DE129', 'DE12A', 'DE12B', 'DE12C', 'DE131', 'DE132', 'DE133',
       'DE134', 'DE135', 'DE136', 'DE137', 'DE138', 'DE139', 'DE13A',
       'DE141', 'DE142', 'DE143', 'DE144', 'DE145', 'DE146', 'DE147',
       'DE148', 'DE149', 'DE211', 'DE212', 'DE213', 'DE214', 'DE215',
       'DE216', 'DE217', 'DE218', 'DE219', 'DE21A', 'DE21B', 'DE21C',
       'DE21D', 'DE21E', 'DE21F', 'DE21G', 'DE21H', 'DE21I', 'DE21J',
       'DE21K', 'DE21L', 'DE21M', 'DE21N', 'DE221', 'DE222', 'DE223',
       'DE224', 'DE225', 'DE226', 'DE227', 'DE228', 'DE229', 'DE22A',
       'DE22B', 'DE22C', 'DE231', 'DE232', 'DE233', 'DE234', 'DE235',
       'DE236', 'DE237', 'DE238', 'DE239', 'DE23A', 'DE241', 'DE242',
       'DE243', 'DE244', 'DE245', 'DE246', 'DE247', 'DE248', 'DE249',
       'DE24A', 'DE24B', 'DE24C', 'DE24D', 'DE251', 'DE252', 'DE253',
       'DE254', 'DE255', 'DE256', 'DE257', 'DE258', 'DE259', 'DE25A',
       'DE25B', 'DE25C', 'DE261', 'DE262', 'DE263', 'DE264', 'DE265',
       'DE266', 'DE267', 'DE268', 'DE269', 'DE26A', 'DE26B', 'DE26C',
       'DE271', 'DE272', 'DE273', 'DE274', 'DE275', 'DE276', 'DE277',
       'DE278', 'DE279', 'DE27A', 'DE27B', 'DE27C', 'DE27D', 'DE27E',
       'DE300', 'DE401', 'DE402', 'DE403', 'DE404', 'DE405', 'DE406',
       'DE407', 'DE408', 'DE409', 'DE40A', 'DE40B', 'DE40C', 'DE40D',
       'DE40E', 'DE40F', 'DE40G', 'DE40H', 'DE40I', 'DE501', 'DE502',
       'DE600', 'DE711', 'DE712', 'DE713', 'DE714', 'DE715', 'DE716',
       'DE717', 'DE718', 'DE719', 'DE71A', 'DE71B', 'DE71C', 'DE71D',
       'DE71E', 'DE721', 'DE722', 'DE723', 'DE724', 'DE725', 'DE731',
       'DE732', 'DE733', 'DE734', 'DE735', 'DE736', 'DE737', 'DE803',
       'DE804', 'DE80J', 'DE80K', 'DE80L', 'DE80M', 'DE80N', 'DE80O',
       'DE911', 'DE912', 'DE913', 'DE914', 'DE916', 'DE917', 'DE918',
       'DE91A', 'DE91B', 'DE91C', 'DE922', 'DE923', 'DE925', 'DE926',
       'DE927', 'DE928', 'DE929', 'DE931', 'DE932', 'DE933', 'DE934',
       'DE935', 'DE936', 'DE937', 'DE938', 'DE939', 'DE93A', 'DE93B',
       'DE941', 'DE942', 'DE943', 'DE944', 'DE945', 'DE946', 'DE947',
       'DE948', 'DE949', 'DE94A', 'DE94B', 'DE94C', 'DE94D', 'DE94E',
       'DE94F', 'DE94G', 'DE94H', 'DEA11', 'DEA12', 'DEA13', 'DEA14',
       'DEA15', 'DEA16', 'DEA17', 'DEA18', 'DEA19', 'DEA1A', 'DEA1B',
       'DEA1C', 'DEA1D', 'DEA1E', 'DEA1F', 'DEA22', 'DEA23', 'DEA24',
       'DEA26', 'DEA27', 'DEA28', 'DEA29', 'DEA2A', 'DEA2B', 'DEA2C',
       'DEA2D', 'DEA31', 'DEA32', 'DEA33', 'DEA34', 'DEA35', 'DEA36',
       'DEA37', 'DEA38', 'DEA41', 'DEA42', 'DEA43', 'DEA44', 'DEA45',
       'DEA46', 'DEA47', 'DEA51', 'DEA52', 'DEA53', 'DEA54', 'DEA55',
       'DEA56', 'DEA57', 'DEA58', 'DEA59', 'DEA5A', 'DEA5B', 'DEA5C',
       'DEB11', 'DEB12', 'DEB13', 'DEB14', 'DEB15', 'DEB16', 'DEB17',
       'DEB18', 'DEB19', 'DEB1A', 'DEB1B', 'DEB21', 'DEB22', 'DEB23',
       'DEB24', 'DEB25', 'DEB31', 'DEB32', 'DEB33', 'DEB34', 'DEB35',
       'DEB36', 'DEB37', 'DEB38', 'DEB39', 'DEB3A', 'DEB3B', 'DEB3C',
       'DEB3D', 'DEB3E', 'DEB3F', 'DEB3G', 'DEB3H', 'DEB3I', 'DEB3J',
       'DEB3K', 'DEC01', 'DEC02', 'DEC03', 'DEC04', 'DEC05', 'DEC06',
       'DED21', 'DED2C', 'DED2D', 'DED2E', 'DED2F', 'DED41', 'DED42',
       'DED43', 'DED44', 'DED45', 'DED51', 'DED52', 'DED53', 'DEE01',
       'DEE02', 'DEE03', 'DEE04', 'DEE05', 'DEE06', 'DEE07', 'DEE08',
       'DEE09', 'DEE0A', 'DEE0B', 'DEE0C', 'DEE0D', 'DEE0E', 'DEF01',
       'DEF02', 'DEF03', 'DEF04', 'DEF05', 'DEF06', 'DEF07', 'DEF08',
       'DEF09', 'DEF0A', 'DEF0B', 'DEF0C', 'DEF0D', 'DEF0E', 'DEF0F',
       'DEG01', 'DEG02', 'DEG03', 'DEG04', 'DEG05', 'DEG06', 'DEG07',
       'DEG09', 'DEG0A', 'DEG0B', 'DEG0C', 'DEG0D', 'DEG0E', 'DEG0F',
       'DEG0G', 'DEG0H', 'DEG0I', 'DEG0J', 'DEG0K', 'DEG0L', 'DEG0M',
       'DEG0N', 'DEG0P']

pipesDestination = gpd.GeoDataFrame({'h2Need': h2Need.values()}, index = indexes)
nodeServing = gpd.GeoDataFrame({'gasDemand': np.zeros(401)}, index = indexes)

with open("connections_O_10.json", 'r') as file:
	Conections = json.load(file)

optimalPlaces = {}
optimalPlaces[0] = []

for node in Conections:
    temp = 0
    
    for destination in Conections[node]:
        if (destination == "XX"): continue
        
        if (Conections[node][destination] != None):
            temp += pipesDestination.loc[destination, "h2Need"]
    
    nodeServing.loc[node, "gasDemand"] = temp

def guardar(n):
	with open("optimalPlaces_n_N_" + str(n) + ".json", 'w') as file:
		json.dump(optimalPlaces, file, indent = 4)

def getMask(nodo):
    mask = gpd.GeoDataFrame({"accessible": np.zeros(401).astype(bool)}, index = indexes)
	
    for destino in Conections[nodo]:
        if (destino == "XX" or Conections[nodo][destino] == None): continue
        mask.loc[destino, "accessible"] = True
    
    return mask

s = 0.5 # % of H2 demand to satisfy

nodeKeys = list(Conections.keys())
threshold = s * pipesDestination["h2Need"].sum()

safeIndexes = []
combis = []

# Case n = 1
for index, nodos in enumerate(nodeKeys):
	mask = getMask(nodos)
	
	tot = (mask["accessible"].values.astype(int) * pipesDestination["h2Need"].values).sum()
	if (tot >= threshold):
		combis.append([index])
		safeIndexes.append(index)

optimalPlaces[1] = copy.deepcopy(combis)

safeCombinations = {}
safeCombinations[1] = [[int(a) for a in nodeC] for nodeC in list(combinations(safeIndexes, 1))]

diffCombinations = {}

# Ordenar los threshold de mayor % a menor -> a partir de cierto punto no está asegurado el suministro
toConsider = [x for x in range(len(nodeKeys)) if x not in safeIndexes]

# n = 2

nodeCombinations = list(combinations(toConsider, 2))
nodeCombinations = [[int(a) for a in nodeC] for nodeC in nodeCombinations]

print("Going into the 2nd layer with", len(nodeCombinations))

combis = []

for nodos in nodeCombinations:
	mask = getMask(nodeKeys[nodos[0]])
	
	for i in range(1, 2):
		mask["accessible"] = np.logical_or(mask["accessible"], getMask(nodeKeys[nodos[i]])["accessible"])
	
	tot = (mask["accessible"].values.astype(int) * pipesDestination["h2Need"].values).sum()
	if (tot >= threshold):
		combis.append(nodos)

print("Adding the trivial combinations")

# Add the nodes that are safe, given that we are in n = 2, we just take the nodes that are safe, and add for each node, one node in AllNodes
for safe in safeIndexes:
	for node in nodeKeys:
		if (safe != node):
			combis.append([safe, node])


optimalPlaces[2] = copy.deepcopy(combis)

guardar(20)

# n = 3


nodeCombinations = list(combinations(toConsider, 3))
nodeCombinations = [[int(a) for a in nodeC] for nodeC in nodeCombinations]

print("Going into the 3rd layer with", len(nodeCombinations))

combis = []

for nodos in nodeCombinations:
	mask = getMask(nodeKeys[nodos[0]])
	
	for i in range(1, 3):
		mask["accessible"] = np.logical_or(mask["accessible"], getMask(nodeKeys[nodos[i]])["accessible"])
	
	tot = (mask["accessible"].values.astype(int) * pipesDestination["h2Need"].values).sum()
	if (tot >= threshold):
		combis.append(nodos)

# Add the nodes that are safe, given that we are in n = 2, we just take the nodes that are safe, and add for each node, one node in AllNodes

safeIndexesDict = {}

for i in range(1, 3):
	safeIndexesDict[i] = [[int(a) for a in nodC] for nodeC in list(combinations(safeIndexes, i))]
	diffIndexes[3 - i] = [[int(a) for a in nodC] for nodeC in list(combinations(toConsider, 3 - i))]
	
	for safe in safeIndexes[i]:
		for node in diffIndexes[3 - i]:
			if (safe != node):
				combis.append([safe, node])

for a in [[int(a) for a in nodC] for nodeC in list(combinations(safeIndexes, 3))]:
	combis.append(copy.deepcopy(a))


optimalPlaces[3] = copy.deepcopy(combis)

guardar(30)
# for n in range(2, 4):	# n = 3 max
	# Initialize the combinations to check (they come from the values that do NOT meet the demand by themselves
	# nodeCombinations = list(combinations(toConsider, n))
	# nodeCombinations = [[int(a) for a in nodeC] for nodeC in nodeCombinations]
	
	# print("Going into the", n, "th layer with", len(nodeCombinations))
	
	# combis = []
	
	# for nodos in nodeCombinations:
		# for prev in optimalPlaces[n-1]:
			# if (set(prev) <= set(nodos)):
				# combis.append(nodos)
				# continue
		
		# mask = getMask(nodeKeys[nodos[0]])
		
		# for i in range(1, n):
			# mask["accessible"] = np.logical_or(mask["accessible"], getMask(nodeKeys[nodos[i]])["accessible"])
		
		# tot = (mask["accessible"].values.astype(int) * pipesDestination["h2Need"].values).sum()
		# if (tot >= threshold):
			# combis.append(nodos)
	
	
	# Add the combinations that are trivial
	# for i in range(1, n):
		# for s in safeCombinations
	
	# optimalPlaces[n] = copy.deepcopy(combis)
	# print("Found", len(combis))
	
	# guardar(n)