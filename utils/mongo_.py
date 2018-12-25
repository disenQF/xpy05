from pymongo import MongoClient

conn = MongoClient('10.12.155.80', 27017,
                   username="",
                   password="")
print('--连接成功!---')

db = conn.zhaopin

# jobs = db.jobs
#
# jobs.insert({'job':'python', 'salary': '10000'})
#
# for job in jobs.find():
#     print(job)