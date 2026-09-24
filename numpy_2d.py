import numpy as np


subjects =np.array(['Maths','Physics','Chemistry','Biology','English'])
exams=np.array(['Midterm','Final'])

np.random.seed(0)
marks= np.random.randint(10,101,size=(len(exams),len(subjects)))
print("Subjects:", subjects)    
print("exams:", exams)
print("Marks:", marks)
print(np.mean(marks)) 