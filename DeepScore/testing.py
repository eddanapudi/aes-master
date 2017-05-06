import EventIssuer
import progressbar
import numpy
import re
from scipy import spatial

bar = progressbar.ProgressBar()

def loadCompleteGloveModel(logfilename):
    global bar
    model = {}
    EventIssuer.issueMessage("Loading GLoVE Word Vectors. This will take a while.", logfilename)
    EventIssuer.issueSleep("Turning to sleep mode.", logfilename)
    f = open("/glove_vectors/glove.42B.300d.txt", 'r').readlines()
    for i in bar(range(len(f))):
        line = f[i]
        splitLine = line.split()
        word = splitLine[0]
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    EventIssuer.issueSuccess("Loaded GLoVE Word Vectors", logfilename)
    EventIssuer.issueMessage(len(model) + " words loaded.", logfilename)
    return model

def getWordVec(word, logfilename):
    word = word.strip().lower()
    # EventIssuer.issueMessage("Word2Vec - Lookup : " + word, logfilename)
    with open("/glove_vectors/glove.42B.300d.txt", 'r') as f:
        for line in f:
            if word[0] == line[0]:
                if word in line:
                    splitLine = line.split()
                    if word == splitLine[0]:
                        embedding = [float(val) for val in splitLine[1:]]
                        # EventIssuer.issueSuccess("Word2Vec - Found WordVec ! " + splitLine[0], logfilename)
                        return numpy.array(embedding)
    EventIssuer.issueWarning("Word2Vec - Primary loopkup failed. Trying advanced lookup : " + word, logfilename)
    word = re.sub('[^a-z]+', ' ', word)
    words = word.split()
    EventIssuer.issueMessage("Word2Vec - Advanced Lookup identifies the presence of these words in the clump : " + str(words), logfilename)
    EventIssuer.issueSharpAlert("Word2Vec - Returning a list of embedding vectors instead of just one: " + str(words), logfilename)
    wvecs = []
    for word in words:
        iffound = False
        # EventIssuer.issueMessage("Word2Vec - Lookup : " + word, logfilename)
        with open("/glove_vectors/glove.42B.300d.txt", 'r') as f:
            for line in f:
                if word[0] == line[0]:
                    if word in line:
                        splitLine = line.split()
                        if word == splitLine[0]:
                            embedding = [float(val) for val in splitLine[1:]]
                            # EventIssuer.issueSuccess("Word2Vec - Found WordVec ! " + splitLine[0], logfilename)
                            iffound = True
                            wvecs.append(numpy.array(embedding))
        if not iffound:
            EventIssuer.issueError("Word2Vec - Not found : " + word, logfilename)
            EventIssuer.issueError("Word2Vec - returning None", logfilename)
            wvecs.append(numpy.array([-0.0071971419, 0.038034291, 0.067505044, 0.090004129, -0.1862136, 0.0477487641, 0.6711488, -0.250773268, 0.075999694, 0.219727019, -0.148549504, -0.085121506, 0.0734719341, -0.07891803, 0.028762588, 0.095495766, 0.1527964985, -0.019069604, -0.000159386, -0.014289429, -0.020020568, -0.0305131702, -0.009426722, -0.047993677, -0.0303836513, 0.116149094, 0.003881902, 0.067539798, 0.065941054, 0.076046747, 0.1834477877, 0.006496807, 0.0050932692, 0.074967404, -0.00167740615, 0.0513104294, 0.033262528, 0.0552852064, -0.0307754428, 0.033744941, -0.0169357353, -0.073538496, 0.076556556, 0.0477559612, 0.030152536, -0.011619235, -0.076599137, 0.12030974, 0.120334391, -0.037826136, -0.000444319, -0.0265530467, 0.114825157, -0.0784206728, -0.000263432, 0.036910476, -0.08650113, -0.059461685, 0.048943902, 0.009627125, -0.0007149627, 0.0495817, 0.007380195, -0.070054098, 0.020593077, 0.014643805, -0.002186668, -0.08610112338, -0.017638128, 0.0062037199, 0.1401558776, -0.0838177376, -0.069796513, 0.0320815074, 0.048048583, 0.1172412428, -0.021675258, -0.1057215154, -0.016556235, 0.054823004, -0.0677215806, 0.303310216, -0.03984594, 0.095258791, -0.029040644, -0.10513797, -0.088345066, 0.003876219, -0.01790383, -0.003906333, 0.011204635, 0.1339004495, 0.013769692, 0.017227031, -0.045316618, 0.22964551, 0.58661061, 0.018802402, -0.087426098, -0.04114762, 0.05271822, -0.1029932545, -0.101448259, -0.0051680928, 0.024561747, 0.051917509, -0.06979360401, 0.029217429, -0.01423352, 0.0332625319, 0.051348392, -0.017232962, -0.087031422, -0.025480295, 0.17517301, -0.1112582922, -0.198503899, -0.080264611, -0.0794522566, -0.106146675059, 0.1042043764, 0.03419873, 0.02528134, 0.139665547, -0.054239325, 0.003317982, 0.01446093, 0.055904408, 0.050255285, 0.06597666, -0.0027891771, -0.057818754, 0.050512937, 0.057041066, -0.104284014, 0.048539121, 0.0032904533, 0.036437017, -0.0066634361, -0.393345841, -0.036858317, -0.085352637, -0.03096532, 0.0578057935, 0.050518039, 0.09720068, -0.074841093, 0.02024298, -0.208579942, -0.018347674, 0.0768829309, 0.12065572, 0.018917901, 0.036955241, -0.062720403, 0.120738583, 0.076060262, -0.017255595, 0.140659706, 0.088145097, -0.07723179, 0.033444682, 0.0279491986, 0.0655360962, -0.033268223, 0.073470189, 0.047171408, 0.0065063135, -0.0410798819, 0.11516255, 0.046581279, -0.011725516, 0.0240178502, 0.043832411, 0.069651211, -0.109000856, 0.0098593491, 0.0293464748, -0.05191695, 0.05985769819, 0.0525228829, -0.110554585, -0.04699427, 0.03103713, -0.039577866, 0.0780700909, -0.06267054, 0.02366544, -0.006737524, -0.031316164, -0.0893335936, 0.04499242, -0.143521181, 0.042565344, 0.024705433, 0.024808143, -0.0258511753, -0.068910291, -0.0437374949, 0.13817618, 0.0451180032, 0.050466407, 0.003336691, -0.036905905, -0.053389866, -0.0664220802, -0.0279904458, -0.032312093, -0.070309043, 0.0791351917, -0.035841839026, 0.053526364, 0.166534373, 0.042336844, 0.011465653, 0.03067487, -0.013652506, 0.0774865, 0.064194998, 0.018029728, 0.05811997, 0.005756151, 0.0738715066, -0.004128079, 0.641443, -0.141303355, 0.057028502, 0.0141146709, 0.0160510732, 0.007878947, -0.102036389, -0.004399322, -0.085377204, 0.001418835, -0.0204011879, -0.052716754, -0.0328608991, 0.009225341, 0.090273355, 0.11482565, 0.017034033, 0.002665617, 0.147449313, -0.130160577, 0.024268086, 0.06980359, -0.084313298, 0.09074731, 0.008108039, -0.040096544, 0.0449544492, 0.003846883, 0.0984588095, -0.037729444, 0.018308231, 0.00237747, -0.017060348, 0.05470805, -0.0540356221, -0.07514963, -0.055423828, 0.069639594, 0.04987485, 0.01293406, -0.0998535, -0.002467158, 0.066136769, 0.0424389575, -0.039217423, -0.044882082, 0.0171389597, 0.00599397584, 0.141697267, -0.043119298, -0.052225656, -0.029637929, -0.09230648, -0.0460420834, -0.056552451, 0.057469622, -0.26924903, 0.116421065, 0.038252634, -0.0685027012, 0.095659097, -0.02042877532, -0.038294187, -0.089739263, 0.049288919, 0.0753936915, -0.006005079, 0.00105016, 0.121543578, 0.08678938, -0.024602735, 0.0278206119, 0.025695247, 0.039601028, 0.00177882, 0.075987566]))
    return wvecs

def getGloveVector(model, word):
    return model[word]


random1 = getWordVec("half", "testing")
random2 = getWordVec("artery", "testing")
random3 = getWordVec("man", "testing")
random4 = getWordVec("mountain", "testing")
random5 = getWordVec("go", "testing")
random6 = getWordVec("sleeper", "testing")


student = getWordVec("student", "testing")
wfor = getWordVec("for", "testing")
wan = getWordVec("an", "testing")
answer = getWordVec("answer", "testing")

searched = getWordVec("searched", "testing")
looked = getWordVec("looked", "testing")
sought = getWordVec("sought", "testing")


sent_vect = (student + wfor + wan + answer)/4



print (1 - spatial.distance.cosine(searched, looked))
print (1 - spatial.distance.cosine(searched, sought))
print (1 - spatial.distance.cosine(searched, sent_vect))
print (1 - spatial.distance.cosine(random1, studfor))
print (1 - spatial.distance.cosine(random2, studfor))
print (1 - spatial.distance.cosine(random3, studfor))
print (1 - spatial.distance.cosine(random4, studfor))
print (1 - spatial.distance.cosine(random5, studfor))
