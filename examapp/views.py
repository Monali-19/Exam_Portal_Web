from django.db import connection
from django.shortcuts import render
from django.contrib.auth import logout

from .models import Questions, UserData , Result


# Create your views here.

                            # For Questions
def Home (request):
    return render(request ,'examapp/home.html')

def Give_Me_Questioncurd_Page(request):
    return render(request,'examapp/Questions/questioncurd.html')

def Give_Me_AddQuestion_Page(request):
    return render(request,'examapp/Questions/addquestion.html')

def Give_Me_ViewQuestion_Page(request):
    return render(request,'examapp/Questions/viewquestion.html')

def Give_Me_UpdateQuestion_Page(request):
    return render(request,'examapp/Questions/updatequestion.html')

def Give_Me_DeleteQuestion_Page(request):
    return render(request,'examapp/Questions/deletequestion.html')

def Give_Me_ShowAllQuestion_Page(request):
    qdata = Questions.objects.all()
    return render(request,'examapp/Questions/showallquestion.html',{'qdata':qdata})




def AddQuestions(request):
  if request.method == "POST":
    qno = request.POST['qno']
    qtext =request.POST['qtext']
    op1 =request.POST['op1']
    op2 =request.POST['op2']
    op3 =request.POST['op3']
    op4 =request.POST['op4']
    subject = request.POST['subject']
    answer = request.POST['answer']

    Questions.objects.create(qno = qno , qtext = qtext ,op1 = op1, op2 = op2, op3 = op3 , op4 = op4 , subject = subject, ans = answer)
    return render (request,'examapp/Questions/addquestion.html' ,{'message' : 'Question add Successfully'})

  else:
      return render(request, 'examapp/Questions/addquestion.html',{'message':'Someething wents Wrong'})
      

def View_Question(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'examapp/Questions/viewquestion.html' ,{'qdata' : qdata})

def View_Question_Update(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'examapp/Questions/updatequestion.html' ,{'qdata' : qdata})

def UpdateQuestion(request):
    qno = request.GET['qno']
    qdata = Questions.objects.filter(qno=qno)
    qdata.update(
        qtext = request.GET['qtext'],
        op1 =request.GET['op1'],
        op2 =request.GET['op2'],
        op4 =request.GET['op4'],
        subject = request.GET['subject'],
        ans = request.GET['answer']
    )
    return render (request,'examapp/Questions/updatequestion.html' ,{'message' : 'Question update Successfully'})

def View_Question_Delete(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'examapp/Questions/deletequestion.html' ,{'qdata' : qdata})

def DeleteQuestion(request):
    qno = request.GET['qno']
    subject = request.GET['subject']

    Questions.objects.filter(qno=qno, subject=subject).delete()
    return render (request,'examapp/Questions/deletequestion.html' ,{'message' : 'Question delete Successfully'})


                                # For Student 



# Create your views here.
def GiveMeRagisterPage(request):
    return render(request,'examapp/Student/ragister.html')


def Ragister(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password =passwd , mobno = mobno)
    return render(request,'examapp/Student/login.html',{'message': 'user ragister successfully'})

def GiveMeLoginPage(request):
    return render(request,'examapp/Student/login.html')


def Login(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    udata = UserData.objects.get(username = uname)

    if (udata.password == passwd):
        request.session['username'] = uname
        request.session['answer'] = {}
        request.session['score'] = 0
        request.session['qno'] = 0 
        return render(request,'examapp/Questions/subject.html')
    else :
        return render(request,'examapp/Student/login.html',{'message':'invalid password'})
    
def GiveMeUserCurdPage(request):
    return render(request,'examapp/Student/usercurd.html')


def GiveMeShowAllPage(request):
    udata = UserData.objects.all()
    return render(request,'examapp/Student/showall.html',{'udata':udata})
 

def AddUser(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password = passwd , mobno = mobno)
    return render(request,'examapp/Student/usercurd.html',{'message': 'user ragister successfully'})

def ShowUser(request):
    try : 
        uname = request.GET['username']
        udata = UserData.objects.get(username = uname)
        return render(request,'examapp/Student/usercurd.html',{'udata':udata})
    except :
         return render(request,'examapp/Student/usercurd.html',{'message': 'user not Found'})

def UpdateUser(request):
    uname = request.GET['username']
    udata = UserData.objects.filter(username = uname)
    udata.update(password = request.GET['password'], mobno = request.GET['mobno'])
    print(connection.queries)
    return render(request,'examapp/Student/usercurd.html',{'message': 'user update successfully'})

def DeleteUser(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    return render(request,'examapp/Student/usercurd.html',{'message': 'user delete successfully'})

def DeleteUserForShowAllPage(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    udata = UserData.objects.all()
    return render(request,'examapp/Student/showall.html',{'udata':udata})


def StartTest(request):
    subject = request.GET['subject']
    request.session['subject'] = subject
    question = Questions.objects.filter(subject = subject).values()

    # select * from questions where subject =  request.GET['subject']

    allquestions = list(question)
    request.session['allquestions']  = allquestions

    return render (request,'examapp/starttest.html',{'question':allquestions[0]})

def NextQuestion(request):
    allquestions = request.session['allquestions'] 
    questionindex = request.session['qno'] #0

    if 'op' in request.GET :
        allanswer = request.session['answer']  # {}
        allanswer[request.GET['qno']] = [request.GET['qno'],request.GET['qtext'], request.GET['op'], request.GET['answer']]

        # allquestions = {1 : [1, 2*2 , 4 ,4]}

        # d1 = {}
        # d1['name'] = 'pratik'
        # d1

    try : 
        if questionindex <= len(allquestions) :
            request.session['qno'] +=1 
            question = allquestions[request.session['qno']]
            return render (request,'examapp/starttest.html',{'question':question})
 
    except  Exception as e:
            return render (request,'examapp/starttest.html',{ "msg": "go to previous question", 'question': allquestions[-1]})


def PreviousQuestion(request):
    allquestions = request.session['allquestions'] 
    questionindex = request.session['qno']

    if 'op' in request.GET :
        allanswer = request.session['answer']  # {}
        allanswer[request.GET['qno']] = [request.GET['qno'],request.GET['qtext'], request.GET['op'], request.GET['answer']]

        # allquestions = {1 : [1, 2*2 , 4 ,4]}

    try : 
        if questionindex > 0 :
                request.session['qno'] -=1 
                question = allquestions[request.session['qno']]
                return render (request,'examapp/starttest.html',{'question':question}) 
    except  Exception as e:
            return render (request,'examapp/starttest.html',{ "msg": "go to previous question", 'question': allquestions[0]})


def EndTest(request):
    if 'op' in request.GET :
        allanswer = request.session['answer']  # {}
        allanswer[request.GET['qno']] = [request.GET['qno'],request.GET['qtext'], request.GET['op'], request.GET['answer']]
    response = request.session['answer'].values()
    print(response)
    for res in response:
        if res[2] == res[3]:
            request.session['score'] +=1

    fianalscore = request.session['score']

    uname = request.session['username']

    udb = UserData.objects.get(username = uname)

    Result.objects.create(
        username = udb ,
        subject = request.GET['subject'],
        score = fianalscore
    )
    return render (request, 'examapp/Result/score.html',{'response':response, 'finalscore':fianalscore})


def SHowallresult(request):
    rdb = Result.objects.all()
    return render (request,'examapp/Result/showallresult.html',{'rdb':rdb})

def LogoutUser(request):
    logout(request)
    return render(request,'examapp/Student/login.html')

def LogoutUser1(request):
    logout(request)
    return render(request,'examapp/home.html')


              # drf

from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .serializer import UserDataSerializer


@api_view(['GET'])
def Emp_info(request):
    return Response({"name":"Monali","Address":"pune"})

@api_view(['GET'])
def GetuserApi(request, username):
    userdb=UserData.objects.get(username=username)
    return Response({'username':userdb.username,'password':userdb.password,'mobile_no':userdb.mobno})

