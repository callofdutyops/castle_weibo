#!/usr/bin/python

# Import relation data into Neo4j Graph database
import csv
import re

FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/weibo_dc_parse2015_link_filter'
TEST_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/relationshiptest.txt'


# Data importer
# def out_degree_calc():
#     weibo_relation_out_degree_dict = defaultdict(int)
#     # progress indicator
#     index = 0
#     sep = re.compile('\001|\t')
#     with open(FILE_PATH, 'r') as myfile:
#         for l in myfile.readlines():
#             arr = sep.split(l.strip())
#             blogger = int(arr[0])
#             index += 1
#             # print per 100000 steps
#             if index % 100000 == 0:
#                 print(index)
#             weibo_relation_out_degree_dict[blogger] = len(arr) - 1
#     with open('weibo_relation_out_degree_dict.pickle', 'wb') as handle:
#         pickle.dump(weibo_relation_out_degree_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#
# def in_degree_calc():
#     weibo_relation_in_degree_dict = defaultdict(int)
#     index = 0
#     sep = re.compile('\001|\t')
#     blogger = []
#     c = Counter([])
#     with open(FILE_PATH, 'r') as myfile:
#         for l in myfile.readlines():
#             arr = sep.split(l.strip())
#             blogger.append(arr[0])
#         blogger = list(map(int, blogger))
#         print('Bloggers have been imported, the length is %d' % len(blogger))
#         print('Now importe in_degreee...')
#     with open(FILE_PATH, 'r') as myfile:
#         for l in myfile.readlines():
#             arr = sep.split(l.strip())
#             arr = list(map(int, arr[1:]))
#             c += Counter(arr)
#             index += 1
#             if index % 10000 == 0:
#                 print(index)
#                 with open('counter.pickle', 'wb') as handle:
#                     pickle.dump(c, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     for i in range(len(blogger)):
#         weibo_relation_in_degree_dict[blogger[i]] = c[blogger[i]]
#     print(weibo_relation_in_degree_dict[4534517])
#     with open('weibo_relation_in_degree_dict.pickle', 'wb') as handle:
#         pickle.dump(weibo_relation_in_degree_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def import_relation_into_neo4j():
#     driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "huangpu"))
#     session = driver.session()
#     # progress indicator
#     index = 0
#     sep = re.compile('\001|\t')
#     with open(FILE_PATH, 'r') as myfile:
#         for l in myfile.readlines():
#             arr = sep.split(l.strip())
#             follower = arr[0]
#             session.run("MERGE (follower:Person {name:{follower}})", {"follower": follower})
#             for followed in arr[1:]:
#                 session.run("MATCH (a:Person {name:{name}}) MERGE (a)-[:FOLLOWS]->(x:Person {name:{n}})",
#                             {"name": follower, "n": followed})
#             index += 1
#             # print per 100000 steps
#             print(index)

def convert_to_csv():
    # progress indicator
    index = 0
    sep = re.compile('\001|\t')
    with open('relationshiptest.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        with open(FILE_PATH, 'r') as myfile:
            for l in myfile.readlines():
                arr = sep.split(l.strip())
                writer.writerow(arr)
                index += 1
                # print per 100000 steps
                if index % 100000 == 0:
                    print(index)


def main():
    convert_to_csv()


if __name__ == '__main__':
    main()
