<<<<<<< HEAD
=======
'''
>>>>>>> parent of 0cb6d73 (Delete : "without deep learning server")
from konlpy.tag import Okt
from konlpy.tag import Kkma
import pickle

with open('ex_dict2.pickle', 'rb') as fw:
   dic = pickle.load(fw) #저장된 사전 불러오기

def translate(txt):
    txt_list = okt.pos(txt)  # 형태소 자르기
    res = []  # 결과

    size = len(txt_list)

    for tmp in txt_list:
        if tmp[1] == 'Noun' and tmp[0] in dic:  # 명사
            res.append(dic[tmp[0]])
        elif tmp[1] == 'Josa':  # 조사
            isJongseong = False
            if (ord(res[-1][-1]) - ord("가")) % 28 > 0:
                isJongseong = True

            if not isJongseong:
                if tmp[0] == '이':
                    res.append('가')
                elif tmp[0] == '을':
                    res.append('를')
                elif tmp[0] == '은':
                    res.append('는')
                else:
                    res.append(tmp[0])

            if isJongseong:
                if tmp[0] == '가':
                    res.append('이')
                elif tmp[0] == '를':
                    res.append('을')
                elif tmp[0] == '는':
                    res.append('은')
                else:
                    res.append(tmp[0])
            res.append(' ')
        else:
            res.append(tmp[0])

    res.append('\n')
<<<<<<< HEAD
    return "".join(res)
=======
    return "".join(res)
'''
>>>>>>> parent of 0cb6d73 (Delete : "without deep learning server")
