import multiprocessing
from konlpy.tag import Komoran
import subprocess
from multiprocessing import Process
from datetime import datetime



# print(komoran.morphs("\n".join(sentences[0].split())))
komoran = Komoran()
# print(komoran.pos("나는 밥을 먹었습니다."))
total_count_shell = subprocess.Popen('wc -l ./input/wiki_ko_preprocess.txt',
                                     stdout=subprocess.PIPE, shell=True)
output = total_count_shell.communicate()[0]
total_count = int(output.split()[0])

def remove_tagger(line):
    # print(line)
    # [('제임스', 'NNP'), ('얼', 'VV'), ('ㄹ', 'ETM'),...
    token_lst = []
    for i, each_token in enumerate(line):
        # print("token", each_token)
        # ('제임스', 'NNP')

        try:
            first_token = each_token[0]
            # print("first token", first_token)
            # '[제임스]'
            token_lst.append("".join(first_token))
        except:
            pass

    # print("token_lst", token_lst)

    result = " ".join(token_lst)
    raw_text = result.replace("[", '').replace("]", '').strip('"\'')
    return raw_text


def file_write(text):
    with open("tagging_remove_wiki_ko.txt",'w',encoding='utf-8') as fw:
        for line in text:
            fw.write("%s\n" % (line))



def process_generator(name):
    ''' Process one file: count number of lines and words '''
    line_count = 0
    # refined_lst = []

    with open("tagging_remove_wiki_ko.txt", 'w', encoding='utf-8') as fw:

        with open(name, 'r') as inp:
            for line in inp:
                line_count += 1
                pos_result = komoran.pos(line)

                # print(pos_result)
                refined_text = remove_tagger(pos_result)
                # refined_lst.append(refined_text)
                fw.write("%s\n" % (refined_text))
                if line_count % 10000 == 0:
                    print("-----progress bar (", line_count,"/",total_count,")-------", round(line_count / total_count * 100, 2), "%")
                    print(refined_text)
            print("---------Finish--------", )
            end_time = datetime.now()
            print('Duration: {}'.format(end_time - start_time))





if __name__ == '__main__':

    start_time = datetime.now()

    workers_count = multiprocessing.cpu_count()
    print("cpu worker number: ", workers_count)

    # workers = [Process(target=process_generator('./input/wiki_ko_preprocess.txt')) for _ in range(workers_count)]
    procs = []

    for _ in range(workers_count):
        proc = Process(target=process_generator('./input/wiki_ko_preprocess.txt'))
        procs.append(proc)
        proc.start()
    #
    #
    for proc in procs:
        proc.join()



    # for worker in workers:
    #     worker.start()
    #
    # for worker in workers:
    #     worker.join()

