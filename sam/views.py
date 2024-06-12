from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import F, Sum
from .models import Software, Staff, Contract,  UserAllocation
from .forms import SoftwareForm, StaffForm, ContractForm, UserAllocationForm
from uuid import uuid4
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
import datetime
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, "sam/index.html")

def staff(request):
    return render(request, "sam/staff.html", {
        "staff": Staff.objects.all(),

    })


def staff_view(request, employee_id):
    staff = Staff.objects.get(employee_id=employee_id)
    user_allocations = UserAllocation.objects.filter(user__employee_id=employee_id)
    softwares = [ua.software for ua in user_allocations]

    return render(request, "sam/staff_view.html", {
        "staff": staff,
        "softwares": softwares
    })


def add_staff(request):
    form = StaffForm
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']

            if Staff.objects.filter(employee_id=employee_id).exists():
                messages.success(request, f'User already Added')
                return redirect('software')
            else:
                form.save()
                messages.success(request, 'New staff added')
                return redirect("staff")

    # context = {'form': form}
    return render(request, "sam/add_staff.html", {
        'form': form
    })

def edit_staff(request, employee_id):
    employee = Staff.objects.get(employee_id=employee_id)
    form = StaffForm(instance=employee)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"{employee.first_name} edited")
            return redirect('staff')

    context = {'form': form,
}
    return render(request, 'sam/edit_staff.html', context)

def delete_staff(request, employee_id):
    employee = Staff.objects.get( employee_id=employee_id)
    employee.delete()
    messages.success(request, f'Employee Removed')
    return redirect('staff')



def software(request):
    contract_values = Software.objects.aggregate(Sum('contract_value'))
    keys = []
    values =[]
    contracts_list= []
    total = contract_values
    softwares = Software.objects.all()
    contracts_list.append(contract_values)
    software_id = Software.objects.all().values("software_id")
    software_names = Software.objects.all().values("software_name")


    return render(request, "sam/software.html", {
        "software": Software.objects.all(),
        "total_contracts": contracts_list[0]['contract_value__sum'],




    })

def insights(request):
    # Retrieve data
    max_users = Staff.objects.all().count() + 1
    software_data = Software.objects.all()
    software_number_of_users_list = [software.number_of_users for software in software_data]
    software_names_list = [software.software_name for software in software_data]

    # Prepare data for the bar chart
    keys = software_names_list
    user_count_values = software_number_of_users_list

    # Prepare data for the pie chart
    labels = [software.software_name for software in software_data]
    values = [software.contract_value for software in software_data]

    # Create the pie chart using Plotly
    pie_fig = px.pie(
        names=labels,
        values=values,
        title='Software Contract Value Distribution'
    )
    pie_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    pie_chart = pie_fig.to_html(full_html=False)

    # Define colors for the bar chart
    colors = px.colors.qualitative.Plotly  # You can choose a different color sequence or define your own list

    # Create the bar chart using Plotly
    bar_fig = go.Figure(data=[
        go.Bar(x=keys, y=user_count_values, marker_color=colors[:len(keys)])
    ])
    bar_fig.update_layout(
        title='Allocated Users for Each Software',
        xaxis_title='Software Names',
        yaxis_title='Allocated Users',
        yaxis=dict(range=[0, int(max_users)]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    bar_chart = bar_fig.to_html(full_html=False)

    # Pass the charts to the template
    context = {'pie_chart': pie_chart, 'bar_chart': bar_chart}

    # Render the template with the charts
    return render(request, 'sam/insights.html', context)

def software_view(request,software_id):
    software_id = str(software_id)
    contract_value = Software.objects.get(software_id=software_id).contract_value
    software = Software.objects.get(software_id=software_id)
    software_id_value  = Software.objects.get(software_id=software_id).software_id
    software_contract = Contract.objects.all().filter(software_id=software_id)
    users = get_number_of_users(software_id)

    if users != 0 and contract_value is not  None:
        number_of_licenses = Software.objects.get(software_id=software_id).number_of_licenses
        utilization = float(users) / float(number_of_licenses) * 100
        cost_per_user = float(contract_value) / float(users)
        return render(request, "sam/software_view.html", {
            "software": software,
            "soft": software_id_value,
            "software_contract": software_contract,
            "users": users,
            "contract_value": contract_value,
        "cost_per_user": round(cost_per_user, 2),
        "utilization": round(utilization, 2)})





    return render(request, "sam/software_view.html", {
        "software": software,
        "soft": software_id_value,
        "software_contract": software_contract,
        "users": users,
        "contract_value": contract_value



    })

def add_software(request):
    form = SoftwareForm(initial={'software_id':  str(uuid4()).split('-')[2]})
    if request.method == "POST":
        new_software = SoftwareForm(request.POST)
        if new_software.is_valid():
            new_software.save()
            messages.success(request, 'New software added')
            return redirect("software")
        else:
            messages.success(request, 'Software not added')
            return redirect("software")

    # context = {'form': form}
    return render(request, "sam/add_software.html", {
        'form': form
    })

def edit_software(request, software_id):
    software = Software.objects.get(software_id=software_id)
    form = SoftwareForm(instance=software)
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
            messages.success(request, f"{Software.objects.get(software_id=software_id)} edited")
            return redirect('software')

    context = {'form': form,
}
    return render(request, 'sam/edit_software.html', context)

def delete_software(request, software_id):
    software = Software.objects.get(software_id=software_id)
    software.delete()
    return redirect('index')


def get_user_list(users, software):
    user_list = []
    allocated_user_ids = UserAllocation.objects.filter(software_id=software).values_list('user_id', flat=True)

    for user in users:
        if user.employee_id not in allocated_user_ids:
            user_list.append(user)

    return user_list

def get_number_of_users(software_id):
    number_of_users = UserAllocation.objects.filter(software_id=software_id).count()
    if number_of_users is None:
        return 0
    return int(number_of_users)

def add_users(request, software_id):
    software_instance = get_object_or_404(Software, software_id=software_id)
    if request.method == "POST":
        user_form = UserAllocationForm(request.POST, software_instance=software_instance)
        if user_form.is_valid():
            users = user_form.cleaned_data['users']
            current_number_of_users = get_number_of_users(software_instance.software_id)
            user_list = get_user_list(users, software_instance)

            # Bulk upload to UserAllocation
            software_users = []
            for user in user_list:

                software_user = UserAllocation(
                    user=user,
                    software=software_instance,  # Use the software instance here
                    assigned=datetime.datetime.now(),
                )
                software_users.append(software_user)

            # Bulk create
            UserAllocation.objects.bulk_create(software_users)
            new_number_of_users = current_number_of_users + len(user_list)
            Software.objects.filter(software_id=software_id).update(number_of_users=new_number_of_users)

            messages.success(request, f'Users {list(user_list)} allocated to {software_instance}')
            return redirect('software_view', software_id=software_id)
    else:
        user_form = UserAllocationForm(initial={'software': software_instance}, software_instance=software_instance)

    return render(request, "sam/add_users.html", {
        'form': user_form,
        'software': software_instance
    })
def add_contract(request, software_id):
    contract = ContractForm(initial={'software_id': software_id, 'contract_id':  str(uuid4()).split('-')[2]})
    if request.method == "POST":
        contract = ContractForm(request.POST)
        if contract.is_valid():
            software_id = contract.cleaned_data['software_id']

            if Contract.objects.filter(software_id=software_id).exists():
                messages.success(request, f'{Software.objects.get(software_id=software_id)} Contract already Exists')
                return redirect('software')

            else:

                contract.save()
                messages.success(request, f'contract details for {Software.objects.get(software_id=software_id)} added ')
                return redirect('software_view', software_id=software_id)
    return render(request, "sam/add_contract.html", {
        'form': contract,
        'software': Software.objects.get(software_id=software_id)

    })





def users_view(request, software_id):

    software = Software.objects.get(software_id=software_id)
    allocated_users = UserAllocation.objects.filter(software_id=software_id)
    return render(request, "sam/users_view.html", {
        "software": software,
        "allocated_user": allocated_users
    })

def user_allocated_view(request, software_id, employee_id):
    user = UserAllocation.objects.get(software_id=software_id, user_id=employee_id)
    software = Software.objects.get(software_id=software_id)
    return render(request, "sam/user_allocated_view.html", {
        "user": user,
        "software": software

    })
def delete_user(request, software_id, id):
    user = UserAllocation.objects.get(software_id=software_id, id=id)
    current_number_of_users = get_number_of_users(software_id)
    user.delete()
    new_number_of_users = current_number_of_users - 1
    Software.objects.filter(software_id=software_id).update(number_of_users=new_number_of_users)
    messages.success(request, f'User {user} unassigned from {Software.objects.get(software_id=software_id)}')
    return redirect('software_view', software_id=software_id)
# def individual_user_allocated_view(request, software_id,employee_id):
#     user = UserAllocation.objects.get(software_id=software_id).values('username')
#     user_list = UserAllocation.objects.filter(software_id=software_id, ).values('username')
#     id_list = []
#     increase = 0
#     for u in user_list:
#         u = Staff.objects.filter.get(employee_id=user_list[increase]['username'])[0]
#         increase += 1
#
#         id_list.append(u)
#     return render(request, "sam/individual_user_allocated_view.html", {
#         "user": user_list,
#         "indiviual": id_list
#     })

def contract_view(request, software_id, id):
    contract = Contract.objects.get(id=id, software_id=software_id   )
    return render(request, "sam/contract_view.html", {
        "contract": contract,

    })

def delete_contract(request, software_id, id):
    contract = Contract.objects.get(id=id, software_id=software_id)
    contract.delete()
    messages.success(request, f'Contract Deleted')
    return redirect('software')

def edit_contract(request, software_id, id):
    contract = Contract.objects.get(software_id=software_id, id=id)
    if contract:
        form = ContractForm(instance=contract)
        if request.method == "POST":
            form = ContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                messages.success(request, f'{Software.objects.get(software_id=software_id)} Contract details Edited')
                return redirect('software')
            else:

                messages.success(request, f'{form.errors}Contract Not Edited')
                return redirect('software')


        return render(request, 'sam/edit_contract.html', {'form': form})
    else:
        # Handle the case where no employee with the given ID is found
        # You might want to redirect to an error page or display a message
        return HttpResponse("Contract not found")





#
# def add_users(request, software_id):
#     user = UserAllocationForm(initial={'software_id': software_id})
#     if request.method == "POST":
#         user = UserAllocationForm(request.POST)
#         if user.is_valid():
#             software = user.cleaned_data['software_id']
#             users = user.cleaned_data['users']
#             allocated_user = AllocatedUsers.objects.filter(save_id__software_id=software_id)
#             user_allocation = []
#             user_allocation = UserAllocation(
#                 software_id=software,
#                 assigned=timezone.now(),  # Use Django's timezone utilities
#             )
#             user_allocation.save()  # Save the UserAllocation instance first
#
#             # Add users to the many-to-many relationship
#             for u in add_users_list(users, software):
#                 AllocatedUsers.objects.create(user=u, save=user_allocation)
#
#
#             # user_allocation = UserAllocation(
#             #     software_id=software,
#             #     assigned= datetime.datetime.today().now(),
#             #     users=add_users_list(users, software),
#             #
#             # )
#
#
#             # Bulk create TimeSheets objects
#             # UserAllocation.objects.bulk_create(user_allocation)
#
#             # allocated_list = []
#             # increase = 0
#             # for u in allocated_user:
#             #     u = allocated_user[increase]
#             #     allocated_list.append(str(u))
#             #     increase += 1
#             #
#             # user_list = []
#             # count = 0
#             # for u in users:
#             #     u = users[count]
#             #     user_list.append(str(u))
#             #     count += 1
#             # # user_list = [u['Allocated'] for u in users]
#             # allocated_set = set(allocated_list)
#             # user_set = set(user_list)
#             #
#             # common_elements = allocated_set.intersection(user_set)
#             #
#             # if common_elements:
#             #     messages.success(request, f"Some users {common_elements} are already allocated to {Software.objects.get(software_id=software_id)}.")
#             #     return redirect('software')
#             # else:
#             #
#             #     user.save()
#                 messages.success(request,
#                                  f' allocated to {Software.objects.get(software_id=software_id)}')
#                 return redirect('software')