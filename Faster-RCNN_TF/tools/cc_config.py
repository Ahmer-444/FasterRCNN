import sys
PY_VER = sys.version_info[0];

CLASSES = ['__background__', 'amazoncolorcard'];

#INPUT_DIR = '/home/ghazanfar/REPOS/Faster-RCNN_TF_all/data/BP_TestBench/input_original_test_data';

INPUT_DIR = '/home/ahmer/ColorCardTraining/Faster-RCNN_TF/data/colorcard/JPEGImages';

#INPUT_DIR = '/home/ghazanfar/Desktop/bp/ProvidedData/Data_070617/WS/all';
#INPUT_DIR = '/home/ghazanfar/Desktop/bp/ProvidedData/Data_030617_WS/WS_Run2/angle1'
#INPUT_DIR = '/home/ghazanfar/Desktop/bp/ProvidedData/Test_Data_010617/All';



OUTPUT_DIR = '/home/ahmer/ColorCardTraining/Faster-RCNN_TF/data/colorcard/output3';
MODEL = '/home/ahmer/ColorCardTraining/Faster-RCNN_TF/output/colorcard_output/colorcard_train/VGGnet_fast_rcnn_iter_10000.ckpt';
TESTING_NETWORK_NAME = 'VGGnet_test';



#CV Correct = (1 - 1363)
#CV ATF = (1364 - 2973)
#SV Correct = (2974 - 4336)
#SV ATF = (4337 - 5946)
#TV Correct = (5947 - 7309)
#TV ATF = (7310 - 8919)
#TV TH = (8920 - 10431)
#TV TL = (10432 - 11855)
#TV Cross = (11856 - 12433)
#HV Cross = (12434 - 12607)
#DV Cross = (12608 - 12798)

#A1 Correct = (12799 - 14208)
#A1 ATF = (14209 - 15191)
#A1 TH = (15192 - 16176)
#A1 TL = (16177 - 17312)

#A2 Correct = (17313 - 18721)
#A2 ATF = (18722 - 19703)
#A2 TH = (19704 - 20688)
#A2 TL = (20689 - 21824)

#A3 Correct = (21825 - 23234)
#A3 ATF = (23235 - 24294)
#A3 TH = (24295 - 25279)
#A3 TL = (25280 - 26415)
#A3 Cross = (26416 - 27551)


######

#A0_2505 Cross = (27552 - 28193)

#A3_2505 ATF = (28194 - 29033)
#A3_2505 Correct = (29034 - 30002)
#A3_2505 Cross = (30003 - 30883)
#A3_2505 Too High = (30884 - 31651)
#A3_2505 Too Low = (31652 - 32849)

#A4_2505 Cross = (32850 - 33734)

#A7_2505 ATF = (33735 - 34337)
#A7_2505 Correct = (34338 - 35310)
#A7_2505 Cross = (35311 - 36196)
#A7_2505 Too High = (36197 - 36964)
#A7_2505 Too Low = (36965 - 38162)

#A12_2505 ATF = (38163 - 38769)
#A12_2505 Correct = (38770 - 39742)
#A12_2505 Too High = (39743 - 40510)
#A12_2505 Too Low = (40511 - 41708)

#######

#A3_3005 ATF = (41709 - 42321)
#A3_3005 Correct = (42322 - 42790)
#A3_3005 Cross = (42791 - 43666)
#A3_3005 Too High = (43667 - 44515)
#A3_3005 Too Low = (44516 - 45098)

#A7_3005 ATF = (45099 - 45713)
#A7_3005 Correct = (45714 - 46186)
#A7_3005 Cross = (46187 - 47059)
#A7_3005 Too High = (47060 - 47883)
#A7_3005 Too Low = (47884 - 48442)

#A12_3005 ATF = (48443 - 49053)
#A12_3005 Correct = (49054 - 49530)
#A12_3005 Too High = (49531 - 50346)
#A12_3005 Too Low = (50347 - 50905)


correct_range = list(range(1   , 1364)) + list(range(2974, 4337)) + list(range(5947, 7310)) + list(range(12799, 14208)) + list(range(17313, 18722)) + list(range(21825, 23235));

atf_range = list(range(1364, 2974)) + list(range(4337, 5947)) + list(range(7310, 8920)) + list(range(14208, 15192)) + list(range(18722, 19704)) + list(range(23235, 24295));

th_range = list(range(8920, 10432)) + list(range(15192, 16177)) + list(range(19704, 20689)) + list(range(24295, 25280));

tl_range = list(range(10432, 11856)) + list(range(16177, 17313)) + list(range(20689, 21825)) + list(range(25280, 26416));

cross_range = list(range(11856,12434)) + list(range(12434, 12608)) + list(range(12608,12799)) + list(range(26416, 27552));

#23 & 25th May dataset ranges
cross_range += 		list(range(27552, 28194));

atf_range += 		list(range(28194, 29034));
correct_range += 	list(range(29034, 30003));
cross_range += 		list(range(30003, 30884));
th_range += 		list(range(30884, 31652));
tl_range += 		list(range(31652, 32850));

cross_range +=		list(range(32850, 33735));

atf_range += 		list(range(33735, 34338));
correct_range +=	list(range(34338, 35311));
cross_range += 		list(range(35311, 36197));
th_range +=			list(range(36197, 36965));
tl_range +=			list(range(36965, 38163));

atf_range +=		list(range(38163, 38770));
correct_range +=	list(range(38770, 39743));
th_range +=			list(range(39743, 40511));
tl_range +=			list(range(40511, 41709));

#30th May dataset ranges
atf_range += 		list(range(41709, 42322))
correct_range += 	list(range(42322, 42791))
cross_range += 		list(range(42791, 43667))
th_range += 		list(range(43667, 44516))
tl_range += 		list(range(44516, 45099))

atf_range += 		list(range(45099, 45714));
correct_range += 	list(range(45714, 46187));
cross_range += 		list(range(46187, 47060));
th_range += 		list(range(47060, 47884));
tl_range += 		list(range(47884, 48443));

atf_range += 		list(range(48443, 49054));
correct_range +=	list(range(49054, 49531));
th_range += 		list(range(49531, 50347));
tl_range +=			list(range(50347, 50906));


#WS0306_a1 = 57271 - 57570
#WS0306_a3 = 57571 - 57870
#WS0306_a6 = 57871 - 58170

#WS0306_r2_a1 = 58171 - 58942
#WS0306_r2_a3 = 58943 - 59718
#WS0306_r2_a6 = 59719 - 60493

#WS0306_r3_a1 = 60494 - 60958
#WS0306_r3_a2 = 60959 - 61419
#WS0306_r3_a8 = 61420 - 61869


ws_range = 	list(range(57271, 57571)) + list(range(57571, 57871)) + list(range(57871, 58171));
ws_range += list(range(58171, 58943)) + list(range(58943, 59719)) + list(range(59719, 60494));
ws_range += list(range(60494, 60959)) + list(range(60959, 61420)) + list(range(61420, 61870));
ws_range += list(range(100000, 110000))


ranges = [ correct_range, atf_range, th_range, tl_range, cross_range ];

ranges_test = [ range(1,873), range(873, 2517), range(2517, 3061), range(3061, 3893) ];

ranges_test_0106 = [ range(1,181), range(181, 487), range(487, 790), range(790, 1249), range(1249, 1443) ];

#ranges = ranges_test_0106;

ranges.append(ws_range);

ground_truth = dict();
ground_truth['correct'] 			= ranges[0];
ground_truth['incorrectarmtoofar'] 	= ranges[1];
ground_truth['incorrecttoohigh'] 	= ranges[2];
ground_truth['incorrecttoolow'] 	= ranges[3];
ground_truth['crosslegs'] 			= ranges[4];
ground_truth['weighingmachine'] 	= ranges[5];

class_indices = dict();
class_indices['correct'] 			= 0;
class_indices['incorrectarmtoofar'] = 1;
class_indices['incorrecttoohigh'] 	= 2;
class_indices['incorrecttoolow'] 	= 3;
class_indices['crosslegs'] 			= 4;
class_indices['weighingmachine'] 	= 5;


class_indices_inv = dict();

if PY_VER == 3:
	class_indices_inv = { v: k for k, v in class_indices.items()}
else:
	class_indices_inv = { v: k for k, v in class_indices.iteritems()}
