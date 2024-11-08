from django.shortcuts import redirect,render
from django.http import HttpResponse

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from myApp.models import *
from django.db.models import Q 


def homePage(req):
    
    current_user = req.user

    jobs = JobModel.objects.all()
    

    context = {
        'jobs':jobs,
    }

    return render(req, 'homepage.html',context)

def searchJob(req):

    query = req.GET.get('query')

    if query:
        jobs = JobModel.objects.filter(Q(title__icontains = query)
                                        |Q(skills__icontains = query))

    else:
        jobs = JobModel.objects.none()

    context = {
        'query': query,
        'jobs': jobs,
    }

    return render(req, 'search.html', context)


@login_required
def profilePage(req):

    current_user = req.user

    seeker_info = JobSeekerModel.objects.filter(user=current_user) 
    recruiter_info = RecruiterModel.objects.filter(user=current_user) 
    
    context = {
        'seeker_info':seeker_info,
        'recruiter_info': recruiter_info,
    }

    return render(req, 'profile.html', context)

@login_required
def editProfile(req):
    update_profile = req.user
    if req.method == 'POST':

        update_profile.username = req.POST.get('username')
        update_profile.first_name = req.POST.get('firstname')
        update_profile.last_name = req.POST.get('lastname')
        update_profile.email = req.POST.get('email')
        update_profile.user_type = req.POST.get('user_type')

        update_profile.save()
        messages.success(req, 'Profile update successfully!')
        return redirect('profilePage')

    
    return render(req,'edit_profile.html')


@login_required
def addSkill(req):

    current_user = req.user
    
    if req.method == 'POST':

        skills = JobSeekerModel.objects.get(user = current_user)
        skills.skills = req.POST.get('skills')
        skills.save()
        return redirect('profilePage')
    
    
    return render(req, 'add_skill.html')


@login_required
def editSkill(req, seeker_id):

    current_user = req.user

    seeker_profile = JobSeekerModel.objects.get(user=current_user)
    

    if req.method == 'POST':
        
        seeker_profile = JobSeekerModel.objects.get(user=current_user)
        
        seeker_profile.skills = req.POST.get('skills')

        seeker_profile.save()
        
        messages.success(req, 'Skill update successfully!')
        return redirect('profilePage')
    
    context = {
        'seeker_data':seeker_profile, 
    }
    return render(req, 'edit_skill.html',context)


@login_required
def addCompany(req):

    current_user = req.user
    
    if current_user.user_type == 'recruiter':
        if req.method == 'POST':

            company_instance = RecruiterModel.objects.get(user = current_user)
            company_instance.company_info = req.POST.get('company')
            
            company_instance.save()
            
            return redirect('profilePage')
    
        return render(req, 'add_company.html')
    else:
        return redirect('homePage')

@login_required
def editCompany(req):

    current_user = req.user

    if current_user.user_type == 'recruiter':
        recruiter_profile = RecruiterModel.objects.get(user=current_user)
    

        if req.method == 'POST':
            
            recruiter_profile = RecruiterModel.objects.get(user=current_user)
            
            recruiter_profile.company_info = req.POST.get('company')

            recruiter_profile.save()
            
            messages.success(req, 'Company update successfully!')
            return redirect('profilePage')
        
        context = {
            'recruiter_data': recruiter_profile, 
        }
        return render(req, 'edit_company.html',context)
    else:
        return render(req, 'edit_company.html')




@login_required
def skillMatchingPage(request):

    current_user = request.user

   
    if current_user.user_type == 'job_seeker':
        mySkill = current_user.JobSeeker.skills
        jobs = JobModel.objects.filter(skills=mySkill)
        
        context = {
            'jobs': jobs,
            'mySkill': mySkill,
        }

        print(mySkill)  

        return render(request, "skill_match.html", context)
    else:
        return redirect('homePage')


@login_required
def applyJob(req, job_id):

    job =  JobModel.objects.get(id=job_id)


    if req.method == 'POST':
        cover = req.POST.get('cover')
        skills = req.POST.get('skills')
        resume = req.FILES.get('resume')

        apply = jobApplyModel(
            user = req.user,
            job = job,
            cover = cover,
            skills = skills,
            resume = resume
        )
        
        
        apply.save()
        
        return redirect('appliedJob')
    
    applied_jobs = jobApplyModel.objects.filter(job=job, user=req.user)
    
    context = {
        'job':job,
        'applied_jobs': applied_jobs
    }

    return render(req, 'apply_job.html',context)

@login_required
def appliedJob(req):
    current_user = req.user
    jobs = jobApplyModel.objects.filter(user=current_user)
    
    print(jobs)
    
    context = {
        'jobs':jobs,
    }

    return render(req, 'applied_job.html', context)



def registerPage(req):

    if req.method == 'POST':
        user_name = req.POST.get('username')
        firstname = req.POST.get('firstname')
        lastname = req.POST.get('lastname')
        email = req.POST.get('email')
        user_type = req.POST.get('user_type')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if password == confirm_password:

            user = Custom_User.objects.create_user(
            username = user_name,
            first_name = firstname,
            last_name = lastname,
            email = email,
            user_type = user_type,
            password = confirm_password 
            )

            if user_type == 'recruiter':
                RecruiterModel.objects.create(user=user)

            elif user_type == 'job_seeker':
                JobSeekerModel.objects.create(user=user)
            
            messages.success(req,'Registration successful!')
            return redirect('loginPage')

        else: 
            messages.warning(req,'Both password must be same!')


    return render(req, 'common/register.html')

def loginPage(req):

    if req.method == "POST":
        user_name = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username = user_name, password = password)
        
        if user is not None:
            login(req,user)
            messages.success(req,'Login successful!')

            return redirect('homePage')
        else:
            messages.warning(req, 'Username/Password is incorrect!')
            return redirect('loginPage')

    return render(req, 'common/login.html')


def logoutPage(req):
    logout(req)
    messages.success(req, 'Logout successful!')
    return redirect('loginPage')




@login_required
def createdJob(req):

    jobs = JobModel.objects.filter(user=req.user)

    context = {
        'jobs':jobs
    }

    return render(req, 'created_job.html', context)

@login_required
def addJob(req):

    if req.method == 'POST':
        jobTitle = req.POST.get('jobTitle')
        numberOfOpenings = req.POST.get('numberOfOpenings')
        category = req.POST.get('category')
        description = req.POST.get('description')
        skills = req.POST.get('skills')
        companyLogo = req.FILES.get('companyLogo')
        
        job = JobModel(
            user = req.user,
            title = jobTitle,
            num_of_openings = numberOfOpenings,
            category = category,
            description = description,
            skills = skills,
            company_logo = companyLogo
        )
        job.save()
        return redirect('createdJob')


    return render(req, 'add_job.html')


@login_required
def deleteJob(req,job_id):

    JobModel.objects.filter(id=job_id).delete()

    return redirect('createdJob')

@login_required
def editJob(req, job_id):

    if req.user.user_type == 'recruiter':
        jobs = JobModel.objects.get(id=job_id)

        context = {
            'jobs':jobs
        }

        if req.method == 'POST':
            jobId = req.POST.get('jobId')
            jobTitle = req.POST.get('jobTitle')
            numberOfOpenings = req.POST.get('numberOfOpenings')
            category = req.POST.get('category')
            description = req.POST.get('description')
            skills = req.POST.get('skills')

            if req.FILES.get('companyLogo'):
                company_logo = req.FILES.get('companyLogo')
            else:
                company_logo = jobs.company_logo

            
            job = JobModel(
                id = jobId,
                user = req.user,
                title = jobTitle,
                num_of_openings = numberOfOpenings,
                category = category,
                description = description,
                skills = skills,
                company_logo = company_logo

            )
            job.save()
            return redirect('createdJob')


        return render(req, 'edit_job.html', context)
    else:
        return render(req, 'edit_job.html')

    

@login_required
def viewJob(req, job_id):


    job = JobModel.objects.get(id=job_id)

    context = {
        'job':job
    }

    return render(req, 'view_job.html', context)